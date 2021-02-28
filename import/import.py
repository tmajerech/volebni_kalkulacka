from Logic.consts import *
from Logic.DbManager import DbManager
import sys, os
from pathlib import Path



# set up working directory
cwd = Path(__file__).parent.absolute()

TEMP_PATH = os.path.join(cwd, 'TMP')


def main(argv):

    # Initialize MySQL Manager
    dbmanager = DbManager()

    for tablename, filename in FILE_NAMES.items():
        print(f"\n\nimporting {tablename}")
        dbmanager.truncateTable(tablename)
        counter = 0
        data_to_insert = []
        filepath = f"import_files/{filename}{FILE_EXTENSION}"
        filepath = os.path.join(cwd, filepath)
        with open(filepath, 'r') as file:
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
        print(f"Files inserted {count}")

if __name__ == "__main__":
    main(sys.argv[1:])