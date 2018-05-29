# GDPR Redact
Redact emails, phone numbers and cookies contained within a CSV for the purposes of GDPR compliance.

# Requirements
1. Python 3
2. Requests Library (`pip install requests`)
3. Zaius API Key (Private, v3)

# CSV Format
1. Filename may be whatever you choose, you must supply the filename as an argument to the script and it must be in the same directory as the script
2. CSV only supports the following columns (email, vuid, phone). Any other columns will be rejected and logged to file so you can fix to re-run.

# Script Arguments
```
usage: gdpr.py [-h] [-l LOGLEVEL] -r REQUESTER -f FILE -a AUTH

A script to redact all identifiers stored in a CSV for a given Zaius account.

optional arguments:
  -h, --help            show this help message and exit
  -l LOGLEVEL, --log LOGLEVEL
                        Supply your desired logging level. Default is ERROR.
                        Supported levels are: DEBUG, INFO, WARN, ERROR.
  -r REQUESTER, --requester REQUESTER
                        Supply the email of the employee running this script
                        for audit purposes.
  -f FILE, --file FILE  Supply the name of the file with the identifiers to
                        process. Supported columns are: email, vuid, phone
  -a AUTH, --auth AUTH  Supply the authentication token for the account that
                        contains the identifiers to be processed
```

# Log Format
```
ERROR:root:REQUEST FAILED FOR EMAIL:tyler@gmail.com
ERROR:root:REQUEST FAILED FOR PHONE:123456
ERROR:root:MISSING OR INVALID COLUMN HEADER:bob@msn.com
```
