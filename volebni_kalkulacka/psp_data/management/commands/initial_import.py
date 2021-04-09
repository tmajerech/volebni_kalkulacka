import os
import pandas as pd
import numpy as np
import environ
import psycopg2
import logging
import glob

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection

from volebni_kalkulacka.psp_data.models import *
from dataImport.Logic.consts import *
from dataImport.dataImport import scrapeLinks, downloadZip
from dataImport.Logic.DbManager import DbManager

env = environ.Env()

TMP_PATH = "./dataImport/TMP/"

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        dbmanager = DbManager()
        conn = connection


        #download files
        file_links = scrapeLinks('#main-content table:first-of-type tr td:first-child a')
        for link in file_links:
            downloadZip(link)

        #loop through all files and remove last delimiter
        for tablename, filename in INITIAL_FILE_NAMES.items():
            filename=f"{filename}{FILE_EXTENSION}"
            filepath = os.path.join(TMP_PATH, filename)
            filepath_formatted= f"{filepath}_formatted"

            try:
                ff = open(filepath_formatted, 'w', encoding="cp1250", errors='replace')
            except Exception as e:
                logger.exception('Error opening formated file')

            with open(filepath, 'r', encoding="cp1250", errors='replace') as f:
                for line in f:
                    ff.write(line[:line.rindex('|')].strip() + '\n')

            ff.close()

        for tablename, filename in INITIAL_FILE_NAMES.items():
            dbmanager.truncateTable(tablename)
            headers = TABLE_HEADERS.get(filename)
            filename=f"{filename}{FILE_EXTENSION}"
            filepath = os.path.join(TMP_PATH, filename)
            filepath_formatted= f"{filepath}_formatted"
            real_tablename = f"{APP_PREFIX}{tablename}"

            print(filename)

            with open(filepath_formatted, 'r') as ff:
                with conn.cursor() as cursor:
                    cursor.execute(f"ALTER TABLE {real_tablename} DISABLE TRIGGER ALL;")
                    cursor.copy_from(ff, real_tablename, sep='|', null="", columns=headers)
                    logger.info(f" rowcount = {cursor.rowcount}")
                    cursor.execute(f"ALTER TABLE {real_tablename} ENABLE TRIGGER ALL;")
                    conn.commit()

        # time for hl_hlasovani accross all periods
        logger.info('importing hl_hlasovani')
        counter = 0
        dbmanager.truncateTable(HL_HLASOVANI)
        files_hl_hlasovani = glob.glob(os.path.join(TMP_PATH, 'hl[1-2][0-9][0-9][0-9]s.unl'))
        for filepath in files_hl_hlasovani:
            counter += 1
            logger.info(f"File {counter} of {len(files_hl_hlasovani)}")

            filepath_formatted = f"{filepath}_formatted"

            try:
                ff = open(filepath_formatted, 'w', encoding="cp1250", errors='replace')
            except Exception as e:
                logger.exception('Error opening formated file')

            with open(filepath, 'r', encoding="cp1250", errors='replace') as f:
                for line in f:
                    ff.write(line[:line.rindex('|')].strip() + '\n')
            ff.close()

            headers = TABLE_HEADERS.get(HL_HLASOVANI)

            real_tablename = f"{APP_PREFIX}{HL_HLASOVANI}"

            with open(filepath_formatted, 'r') as ff:
                with conn.cursor() as cursor:
                    cursor.execute(f"ALTER TABLE {real_tablename} DISABLE TRIGGER ALL;")
                    cursor.copy_from(ff, real_tablename, sep='|', null="", columns=headers)
                    logger.info(f" rowcount = {cursor.rowcount}")
                    cursor.execute(f"ALTER TABLE {real_tablename} ENABLE TRIGGER ALL;")
                    conn.commit()

        # time for hl_poslanec accross all periods
        logger.info('importing hl_poslanec')
        counter = 0
        dbmanager.truncateTable(HL_POSLANEC)
        files_hl_poslanec = glob.glob(os.path.join(TMP_PATH, 'hl[1-2][0-9][0-9][0-9]h[0-9].unl'))
        for filepath in files_hl_poslanec:
            counter += 1
            logger.info(f"File {counter} of {len(files_hl_poslanec)}")

            filepath_formatted = f"{filepath}_formatted"

            try:
                ff = open(filepath_formatted, 'w', encoding="cp1250", errors='replace')
            except Exception as e:
                logger.exception('Error opening formated file')

            with open(filepath, 'r', encoding="cp1250", errors='replace') as f:
                for line in f:
                    ff.write(line[:line.rindex('|')].strip() + '\n')
            ff.close()

            headers = TABLE_HEADERS.get(HL_POSLANEC)

            real_tablename = f"{APP_PREFIX}{HL_POSLANEC}"

            with open(filepath_formatted, 'r') as ff:
                with conn.cursor() as cursor:
                    cursor.execute(f"ALTER TABLE {real_tablename} DISABLE TRIGGER ALL;")
                    cursor.copy_from(ff, real_tablename, sep='|', null="", columns=headers)
                    logger.info(f" rowcount = {cursor.rowcount}")
                    cursor.execute(f"ALTER TABLE {real_tablename} ENABLE TRIGGER ALL;")
                    conn.commit()

        #hist for some reason needs to be executed separately
        dbmanager.truncateTable(HIST)
        headers = TABLE_HEADERS.get(HIST)
        with open("./dataImport/TMP/hist.unl_formatted", 'r') as ff:
            with conn.cursor() as cursor:
                cursor.execute(f"ALTER TABLE psp_data_hist DISABLE TRIGGER ALL;")
                cursor.copy_from(ff, "psp_data_hist", sep='|', null="", columns=headers)
                logger.info(f" rowcount = {cursor.rowcount}")
                cursor.execute(f"ALTER TABLE psp_data_hist ENABLE TRIGGER ALL;")
                conn.commit()

        # remove zmatecne hlasovani
        logger.info("Removing zmatecne hlasovani")
        dbmanager.removeZmatecneHlasovani()
        logger.info("Zmatecne hlasovani removed")

        # fill ratings table with calculations
        logger.info('Calculating hlasovani differences')
        dbmanager.calculateHlasovaniRatings()
        logger.info('Hlasovani differences calculated')

        # replace weird characters in hlasovani names
        logger.info('Replacing weird characters')
        dbmanager.replaceWeirdCharacters()
        logger.info('Replace complete')