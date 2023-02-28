from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import argparse

DATABASE_URL = "sqlite:///darbo_skelbimai.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class DarboSkelbimai(Base):
    __tablename__ = "darbo_skelbimai"
    id = Column(Integer, primary_key=True, index=True)
    profesija = Column(String(255))
    imone = Column(String(255))
    atlyginimas = Column(String(255))
    atlyginimo_didis = Column(String(255))
    miestas = Column(String(255))
    data = Column(Text)

try:
    source = requests.get('https://www.cvbankas.lt/').text
    soup = BeautifulSoup(source, 'html.parser')
    blokas = soup.find_all('div', class_="list_a_wrapper")
except requests.exceptions.RequestException as klaida:
    print("Klaida pasiekiant svetainę: ", klaida)
    print("Prašome patikrinti savo interneto ryšį ir bandyti dar kartą vėliau.")
    exit()

Base.metadata.create_all(bind=engine)

for blokai in blokas:
    try:
        profesija = blokai.find('h3', class_="list_h3", lang="lt").text.strip()
        imone = blokai.find('span', class_="dib mt5").text.strip()
        atlyginimas = blokai.find('span', class_="salary_amount").text.strip()
        atlyginimo_didis = blokai.find('span', class_="salary_calculation").text.strip()
        miestas = blokai.find('span', class_="list_city").text.strip()
        data = blokai.find('span', class_="txt_list_2").text.strip()

        darbo_skelbimas = DarboSkelbimai(profesija=profesija, imone=imone,
                                         atlyginimas=atlyginimas, atlyginimo_didis=atlyginimo_didis,
                                         miestas=miestas, data=data)
        session.add(darbo_skelbimas)
    except:
        pass



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





