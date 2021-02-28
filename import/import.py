from Logic.consts import *
from Logic.DbManager import DbManager
import sys, os, logging, requests, zipfile, shutil, datetime, io
from pathlib import Path

# start time counter
begin_time = datetime.datetime.now()

# set up working directory
cwd = Path(__file__).parent.absolute()

#temporary storage for downloaded files
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

logger.info(f"""
\n\n\n==============IMPORT.PY STARTED==============""")


def main(argv):

    for file_to_download in PSP_FILES_TO_DOWNLOAD:
        # Downloads zip
        try:
            r = requests.get(file_to_download)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(TEMP_PATH)
            logger.info(f'File {file_to_download} downloaded')
        except:
            logger.exception('Error downloading zip')
            sys.exit()

    # Initialize DB Manager
    dbmanager = DbManager()

    for tablename, filename in FILE_NAMES.items():
        logger.info(f"\n\nimporting {tablename}")
        dbmanager.truncateTable(tablename)
        counter = 0
        data_to_insert = []
        filepath = f"{TEMP_PATH}/{filename}{FILE_EXTENSION}"
        filepath = os.path.join(cwd, filepath)
        with open(filepath, 'r', encoding="cp1250", errors='replace') as file:
            for line in file.readlines():
                counter += 1
                data_to_insert.append(tuple(x if x != '' else None for x in line.split("|")[
                                        :len(TABLE_HEADERS.get(tablename))]))
                # split data into pieces
                # if counter == 10:
                #     count = dbmanager.batch_insert_data(
                #         tablename, data_to_insert)
                #     print(f"Files inserted {count}")
                #     counter = 0
                #     data_to_insert = []
                #     break

        # insert remaining or small batch
        count = dbmanager.batch_insert_data(tablename, data_to_insert)
        logger.info(f"Files inserted {count}")


    # close connection to database
    dbmanager.close_db_connection()

    # remove tmp files
    try:
        shutil.rmtree(TEMP_PATH)
        logger.info('tmp folder removed')
    except:
        logger.exception('Error removing tmp folder')

    # print total execution time
    logger.info(f"Execution time: {datetime.datetime.now() - begin_time}")

if __name__ == "__main__":
    main(sys.argv[1:])