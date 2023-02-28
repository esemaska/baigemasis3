import argparse
from parser import *


def perziureti_skelbimus():
    result = session.query(DarboSkelbimai).all()
    for row in result:
        print(
            f"{row.id} - {row.profesija} - {row.imone} - {row.atlyginimas} - {row.atlyginimo_didis} - {row.miestas} - {row.data}")

parser = argparse.ArgumentParser(description="Peržiūrėti duomenis iš darbo_skelbimai lentelės")
parser.add_argument("--view", help="Peržiūrėti duomenis")
parser.add_argument("--add", help="Pridėti naujus skelbimus")

args = parser.parse_args()

if args.view:
    perziureti_skelbimus()
    input("Spauskite ENTER, kad tęsti. " )
    pasirinkimas = input("Ar norite išsaugoti skelbimus į duomenų bazę? (taip/ne): ")
    if pasirinkimas.lower() == "taip":
        session.commit()
        print("Skelbimai išsaugoti.")
    elif pasirinkimas.lower() == "ne":
        session.rollback()
        print("Skelbimai nebuvo išsaugoti.")
    else:
        session.rollback()
        print("Pasirinkimas netinkamas.")


