from bs4 import BeautifulSoup
import requests

r = requests.get(
    "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_index_number_(Generation_III)")

soup = BeautifulSoup(r.text, features="lxml")

table_info = soup.find_all("table")[0]
table_info = table_info.find_all("tr")

pokemon = {}
for i in range(3, len(table_info)):
    tr = table_info[i]
    tds = tr.find_all("td")
    #############
    hex_value = tds[0].text.strip()
    dec_value = tds[1].text.strip()
    img = tds[2].find("img")['src'].strip()
    name = tds[3].text.strip()
    type1 = tds[4].text.strip()
    type2 = tds[5].text.strip()
    #############
    pokemon[dec_value] = {"hex_value": hex_value, "dec_value": dec_value,
                          "img": img, "name": name, "type1": type1, "type2": type2}


with open('pokemons.csv', 'w', encoding='utf-8') as f:
    for key in pokemon.keys():
        values = pokemon[key]
        line = ""
        for vals in values:
            val = values[vals]
            line += val + ";"
        line += "\n"
        f.write(line)
