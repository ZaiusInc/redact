import requests
import csv
import argparse
import logging
import time

class ZaiusGDPR():

    def __init__(self):
        
        parser = argparse.ArgumentParser(
            description='A script to redact all identifiers stored in a CSV for a given Zaius account.'
        )

        parser.add_argument('-l', '--log', dest='loglevel', required=False, help='Supply the name of the file with the identifiers to process. Supported columns are: email, vuid, phone')
        parser.add_argument('-r', '--requester', dest='requester', required=True, help='Supply the email of the employee running this script for audit purposes.')
        parser.add_argument('-f', '--file', dest='file', required=True, help='Supply the name of the file with the identifiers to process. Supported columns are: email, vuid, phone')
        parser.add_argument('-a', '--auth', dest='auth', required=True, help='Supply the authentication token for the account that contains the identifiers to be processed')

        args = parser.parse_args()

        self.requester = args.requester
        self.auth = args.auth
        self.file = args.file

        if args.loglevel != None:
            loglevel = args.loglevel
        else: 
            loglevel = "ERROR"

        numeric_level = getattr(logging, loglevel.upper(), None)
        
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        
        logging.basicConfig(filename='gdpr_redaction_'+str(int(time.time()))+'.log',level=numeric_level)

        self.redact()    

    def read_file(self):

        try:
            with open(self.file, 'r') as csvfile:
                file = csv.DictReader(csvfile)         
                for row in file:
                    yield row

        except FileNotFoundError as fe:
            print("Cannot find the file by the name you have provided. Ensure it is in the same directory as this script and you have included the extension if it exists.")

    def redact(self):

        row_number = 1

        for row in self.read_file():

            for column, field in row.items():

                redaction_metadata = {}
                redaction_headers = {
                    "x-api-key": self.auth
                }

                column = column.strip().lower()
                field = field.strip()

                if field != "":

                    if len(column) > 0 and column in ('email', 'phone', 'vuid'):
                        
                        redaction_metadata["requester"] = self.requester
                        redaction_metadata[column] = str(field)

                        logging.debug("REQUEST BODY:" + str(redaction_metadata))
                        logging.debug("REQUEST HEADER:" + str(redaction_headers))

                        try:
                            response = requests.post("https://api.zaius.com/v3/optout", json=redaction_metadata, headers=redaction_headers)
                            logging.debug("REQUEST BODY:" + str(redaction_metadata))

                            if response.status_code == 202:
                                logging.info("REDACTED " + column.upper() + ":" + field)
                            else:
                                logging.error("REQUEST FAILED FOR " + column.upper() + ":" + field)
                                logging.warn("REQUEST RESPONSE: " + str(response.status_code))

                        except Exception as e:
                            logging.error("REQUEST FAILED FOR " + column.upper() + ":" + field + " Message: " + str(e))
                            logging.warn("REQUEST EXCEPTION:" + str(e))

                    else:
                        if len(column) == 0:
                            logging.error("MISSING OR INVALID COLUMN HEADER:" + field)

                else:
                    logging.warn("EMPTY FIELD ON ROW:" + str(row_number) + " & COLUMN " + column)

            row_number += 1
            time.sleep(1)

ZaiusGDPR()
