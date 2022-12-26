# Cardmarket Price Checker

A tool for analysing a cardmarket account's offerings and comparing them to the lowest market offer for a given card.

### Quickstart

1. Create a python virtual environment and install the requirements.
```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

2. Run the program.
```
$ python -m src --user <YOUR_CARDMARKET_USERNAME>
```

### Optional Args:
```
-h, --help
        show this help message and exit
-u USER, --user USER
-d, --debug
-n PAGES, --pages PAGES
-m MIN_PRICE, --min_price MIN_PRICE
```
### Example usage:

Analysing all cards being sold by 'Extasia1'
```
$ python -m src Extasia1
```

Analsying the single cards being sold by 'Extasia1' for 5 euros or more.
```
$ python -m src --user Extasia1 --min_price 5
``` 