# import os
# import pandas as pd
# import numpy as np
# import environ
# import psycopg2
# import logging
# import glob

# from django.core.management.base import BaseCommand
# from django.conf import settings
# from django.db import connection

# from volebni_kalkulacka.psp_data.models import *
# from dataImport.Logic.consts import *
# from dataImport.dataImport import scrapeLinks, downloadZip
# from dataImport.Logic.DbManager import DbManager

# env = environ.Env()

# TMP_PATH = "./dataImport/TMP/"

# logger = logging.getLogger(__name__)


# class Command(BaseCommand):

#     def handle(self, *args, **kwargs):

#         dbmanager = DbManager()
#         conn = connection


#         dbmanager.