# BS Generator

This program get airtable and pappers data then generate pfd from html template.

## Setup

### Linux

Install python dependancies :
```
python3 -m pip install -r requirements.txt
```

### Mac

Give execution wright to mac-setup.sh script :
```
chmod +x mac-setup.sh
```
Run mac-setup.sh script :
```
./mac-setup.sh
```

## Usage

You need an .env file for airtable api :

```
API_KEY =
BASE_ID =
TABLE_NAME =
TABLE_TARGET =
```

Run the program :

```
usage: bs_generator.py [-h] [--docx] [--bsa-air] structure

positional arguments:
  structure   structure name

options:
  -h, --help  show this help message and exit
  --docx      generate docx
  --bsa-air   generate bsa air bs
```