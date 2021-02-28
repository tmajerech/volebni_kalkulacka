import psycopg2
import psycopg2.extras
import os
import sys
from decouple import config
import logging
from Logic.consts import *
import logging

logger = logging.getLogger(__name__)


class DbManager(object):

    def __init__(self):
        self.host = config('PG_HOST')
        self.database = config('PG_DB')
        self.user = config('PG_USER')
        self.password = config('PG_PASSWORD')
        self.connection = self.connect_to_db()


    def connect_to_db(self):

        connection = None
        try:
            connection = psycopg2.connect(
                database = self.database,
                user = self.user,
                password = self.password,
                )

        except Exception as e:
            logger.exception("Error while connecting to DB")
            sys.exit()

        return connection

    def batch_insert_data(self, table_name, data):
        """
        Method that inserts list of tuples into database

        :param data [tuple] list of tuples to insert
        """
        try:
            cursor = self.connection.cursor()

            #self refferenced table needs to be treated different
            #disable triggers
            if table_name in SELF_REFFERENCED:
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

            #self refferenced table needs to be treated different
            #reenable triggers
            if table_name in SELF_REFFERENCED:
                cursor.execute(f"ALTER TABLE {APP_PREFIX}{table_name} ENABLE TRIGGER ALL;")

            self.connection.commit()   # commit the changes
            
            rowcount = cursor.rowcount

            cursor.close()
            return rowcount

        except Exception as e:
            logger.exception('error batch inserting data')
            sys.exit()

    def close_db_connection(self):
        self.connection.close()
        logger.info("DB connection is closed")

    def truncateTable(self, tablename):
        """
        Function clears all data from table with given name
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"TRUNCATE TABLE {APP_PREFIX}{tablename} CASCADE")
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logger.exception("Error truncating table")
            sys.exit()
        logger.info(f"table {tablename} truncated")
