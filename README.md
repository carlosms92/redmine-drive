# redmine-spreadsheet

Get issues from Redmine and update google sheets.

## Installation

### 1. Install lib "python-redmine"
```
$ pip install python-redmine
```

### 2. Enable google sheets api and install google client lib

https://developers.google.com/sheets/api/quickstart/python

## Usage

### Shell script:
```
$ python main.py --help
```
```
usage: main.py [-h] [-u USERNAME] [-p [PASSWORD]]

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Redmine user
  -p [PASSWORD], --password [PASSWORD]
                        Redmine password
```

### Crontab
```
$ crontab -e
```
Add shell script.
Example: Execution at 9:00 Monday-Friday
```
0 9 * * 1-5 /usr/bin/python [path-to-project]/redmine-spreadsheet/main.py -u [redmine username] -p [redmine password] > /tmp/resultCron.log 2>&1
```
