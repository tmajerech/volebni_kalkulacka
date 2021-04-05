from .Logic.consts import *
from .Logic.DbManager import DbManager
import sys
import os
import logging
import requests
import zipfile
import shutil
import datetime
import io
from pathlib import Path
from bs4 import BeautifulSoup
import requests

# start time counter
begin_time = datetime.datetime.now()

# set up working directory
cwd = Path(__file__).parent.absolute()

# temporary storage for downloaded files
TEMP_PATH = os.path.join(cwd, 'TMP')

# set up logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    handlers=[
        #logging.FileHandler(os.path.join("/var/log", 'volebnikalkulacka_import.log')),
        logging.FileHandler(os.path.join(cwd, 'volebnikalkulacka_import.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def runImport():

    logger.info(f"""
    \n\n\n==============IMPORT.PY STARTED==============""")

    # scrape links to files
    url = 'https://www.psp.cz/sqw/hp.sqw?k=1300'
    download_url = 'https://www.psp.cz'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    download_links = []

    for link in soup.select('#main-content table:first-of-type tr td:first-child a'):
        download_links.append(str(download_url + link.get('href').replace('..', '')))

    for link in download_links:
        try:
            r = requests.get(link)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(TEMP_PATH)
            logger.info(f'File {link} downloaded')
        except:
            logger.exception('Error downloading zip')
            sys.exit()

    # Initialize DB Manager
    dbmanager = DbManager()

    for tablename, filename in FILE_NAMES.items():
        logger.info(f"\n\nimporting {tablename}")
        dbmanager.truncateTable(tablename)
        counter = 0
        total_count = 0
        data_to_insert = []
        filepath = f"{TEMP_PATH}/{filename}{FILE_EXTENSION}"
        filepath = os.path.join(cwd, filepath)
        with open(filepath, 'r', encoding="cp1250", errors='replace') as file:
            for line in file.readlines():
                counter += 1
                total_count += 1
                data_to_insert.append(tuple(x if x != '' else None for x in line.split("|")[
                    :len(TABLE_HEADERS.get(tablename))]))
                # split data into pieces
                if counter == 100000:
                    dbmanager.batch_insert_data(
                        tablename, data_to_insert)
                    print(f"Rows inserted {total_count}")
                    data_to_insert = []
                    counter = 0

        # insert remaining or small batch
        dbmanager.batch_insert_data(tablename, data_to_insert)
        logger.info(f"Rows inserted {total_count}")

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

    # remove tmp files
    try:
        shutil.rmtree(TEMP_PATH)
        logger.info('tmp folder removed')
    except:
        logger.exception('Error removing tmp folder')

    # print total execution time
    logger.info(f"Execution time: {datetime.datetime.now() - begin_time}")
