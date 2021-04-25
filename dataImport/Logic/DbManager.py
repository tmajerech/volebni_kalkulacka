import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
import pandas as pd
import os
import sys
from decouple import config
import logging
from .consts import *
import logging

from django.db import connections

logger = logging.getLogger(__name__)


class DbManager(object):

    def __init__(self):
        self.connection = connections['default']

    def batch_insert_data(self, table_name, data):
        """
        Method that inserts list of tuples into database

        :param data [tuple] list of tuples to insert
        """
        try:
            with self.connection.cursor() as cursor:

                cursor.execute("BEGIN")
                cursor.execute(f"ALTER TABLE {APP_PREFIX}{table_name} DISABLE TRIGGER ALL;")

                headers = ", ".join(TABLE_HEADERS.get(table_name))

                values = "%s"
                for i in range(len(TABLE_HEADERS.get(table_name))-1):
                    values = values + ", %s"

                # prepare DB query
                query = f'INSERT INTO {APP_PREFIX}{table_name}({headers}) VALUES %s'

                psycopg2.extras.execute_values(
                    cursor, query, data, template=None, page_size=100
                )


                cursor.execute(f"ALTER TABLE {APP_PREFIX}{table_name} ENABLE TRIGGER ALL;")

                cursor.execute("END")
            return

        except Exception as e:
            logger.exception('error batch inserting data')
            sys.exit()

    def truncateTable(self, tablename):
        """
        Function clears all data from table with given name
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"TRUNCATE TABLE {APP_PREFIX}{tablename} RESTART IDENTITY CASCADE")

        except Exception as e:
            logger.exception("Error truncating table")
            sys.exit()
        logger.info(f"table {tablename} truncated")

    def removeZmatecneHlasovani(self):
        """
        Completely removes zmatecne hlasovani from hlasovani
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""
                DELETE FROM {APP_PREFIX}hl_hlasovani_rating
                WHERE id_hlasovani IN(
                    SELECT id_hlasovani
                    FROM {APP_PREFIX}{ZMATECNE}
                );

                DELETE FROM {APP_PREFIX}{HIST}
                WHERE id_hlas IN(
                    SELECT id_hlasovani
                    FROM {APP_PREFIX}{ZMATECNE}
                );

                DELETE FROM {APP_PREFIX}{HL_POSLANEC}
                WHERE id_hlasovani IN(
                    SELECT id_hlasovani
                    FROM {APP_PREFIX}{ZMATECNE}
                );
                
                DELETE FROM {APP_PREFIX}{HL_HLASOVANI}
                WHERE id_hlasovani IN(
                    SELECT id_hlasovani
                    FROM {APP_PREFIX}{ZMATECNE}
                );
                """)
        except Exception as e:
            logger.exception('Error deleting zmatecne')

    def calculateHlasovaniRatings(self):
        """
        Calculates rating for all hlasovani in hist and addes them to hl_hlasovani_rating table
        """
        try:
            with self.connection.cursor() as cursor:

                #get all hl_hlasovani from hist from last 2 election periods
                query = f"""
                SELECT * 
                FROM 
                    psp_data_hl_hlasovani as hh

                    INNER JOIN psp_data_hist as h
                    ON h.id_hlas = hh.id_hlasovani

                WHERE 
                    hh.id_organ IN (
                        --last 2 election periods
                        select 
                            id_organ from psp_data_organy 
                        where 
                            organ_id_organ is null
                            and id_typ_organu = 11 --poslanecka snemovna
                        union
                        select id_organ-1 from psp_data_organy 
                        where 
                            organ_id_organ is null
                            and id_typ_organu = 11 --poslanecka snemovna
                    )
                """
                cursor.execute(query)
                columns = [x.name for x in cursor.description]
                interesting_hlasovani = []
                for row in cursor.fetchall():
                    row = dict(zip(columns, row))
                    interesting_hlasovani.append(row)

                data_values = []
                i = 0
                # loop through every hlasovani
                for hlasovani in interesting_hlasovani:
                    i=i+1
                    print(f'{i}/{len(interesting_hlasovani)}')
                    # query for all voters votes and parties
                    SQL_Query = pd.read_sql_query(
                    f'''
                    SELECT 
                        zkratka,vysledek
                    FROM 
                        psp_data_hl_poslanec AS hp 

                        INNER JOIN psp_data_poslanec AS p 
                        ON hp.id_poslanec = p.id_poslanec 
                        
                        INNER JOIN psp_data_zarazeni AS z
                        ON p.id_osoba = z.id_osoba
                        
                        INNER JOIN psp_data_organy as o
                        ON z.id_of = o.id_organ
                        
                        INNER JOIN psp_data_osoby as os
                        ON os.id_osoba = p.id_osoba                     
                    WHERE 
                        hp.id_hlasovani = {hlasovani['id_hlasovani']}
                        AND z.cl_funkce = 0 --clenstvi
                        AND o.organ_id_organ = {hlasovani['id_organ']} --ID election period 
                        AND o.id_typ_organu = 1 --Klub
                        AND ( --either member ship is active (null) or membership ended together with election period
                            TO_DATE(z.do_o, 'YYYY-MM-DD') = TO_DATE(o.do_organ,'DD.MM.YYYY')
                            OR 
                            z.do_o IS null
                            )
                    ''', self.connection)
                    df = pd.DataFrame(SQL_Query)

                    total_difference = 0
                    for party in df['zkratka'].unique():
                        pro_df = df.query(f'zkratka=="{party}" & vysledek == "A"')
                        proti_df = df.query(f'zkratka=="{party}" & (vysledek == "B" | vysledek == "N" )').count()
                        members_count = len(
                            df.query(f'zkratka=="{party}" & (vysledek == "A" | vysledek == "B" | vysledek == "N" ) ').index)

                        if(members_count == 0):
                            # no party members present for this hlasovani
                            break

                        pro_percentage = len(pro_df.index)/members_count
                        proti_percentage = len(proti_df.index)/members_count
                        party_difference = 1 - abs(pro_percentage-proti_percentage)

                        total_difference += party_difference * (members_count/len(df.index)) * 100

                    data_values.append((hlasovani['id_hlasovani'], round(
                        total_difference, 2), round(total_difference, 2), 0, 0))
                    logger.debug(f"Calculated differences for {hlasovani['id_hlasovani']}")

                logger.info('Calculation complete, inserting to DB')

                # prepare DB query
                query = f"""
                INSERT INTO psp_data_hl_hlasovani_rating(id_hlasovani, difference, rating, user_rating_down, user_rating_up) VALUES %s
                ON CONFLICT (id_hlasovani)
                DO
                    UPDATE SET 
                        difference = EXCLUDED.difference,
                        rating = EXCLUDED.rating,
                        user_rating_down = EXCLUDED.user_rating_down,
                        user_rating_up = EXCLUDED.user_rating_up
                """

                psycopg2.extras.execute_values(
                    cursor, query, data_values, template=None, page_size=100
                )

        except Exception as e:
            logger.exception('Error rating hlasovani')

    def replaceWeirdCharacters(self):
        try:
            with self.connection.cursor() as cursor:
                for (weird,normal) in weirdChars:
                    sql = f"""
                    UPDATE psp_data_hl_hlasovani
                    SET 
                        nazev_dlouhy = REPLACE(nazev_dlouhy,
                            '{weird}',
                            '{normal}')
                    WHERE
                        nazev_dlouhy LIKE '%{weird}%';
                    """
                    cursor.execute(sql)

        except Exception as e:
            logger.exception('Error replaceWeirdCharacters')
