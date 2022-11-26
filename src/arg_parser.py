import argparse

parser = argparse.ArgumentParser(
    prog="Cardmarket Price Checker",
    description="Tool for analysing a cardmarket account's offerings and comparing them to the lowest market offer for a given card.",
    epilog=
    """Example usage:
    
    Analysing all cards being sold by 'Extasia1'
    $ python -m src Extasia1

    Analsying the single cards being sold by 'Extasia1' for 5 euros or more.
    $ python -m src --user Extasia1 --min_price 5
    """,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument("-u", "--user",
                    default="Extasia1")

parser.add_argument("-d", "--debug",
                    action="store_true")
                    
parser.add_argument("-n", "--pages",
                    default=None,
                    type=int)

parser.add_argument("-m", "--min_price",
                    default=None,
                    type=float)

args = parser.parse_args()

if args.debug and (args.pages is None):
    args.pages = 1
