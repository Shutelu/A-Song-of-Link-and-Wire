from bs4 import BeautifulSoup
import requests

# tupel = [('A',1),('B',2),('C',3)]
# t = tupel[1]
# cible, poids = t
# print(cible)
# print(poids)

def nb_voyelles(n):
    nb = 0
    for v in n:
        if v in 'aeiouyAEIOUY':
            nb += 1
    return nb

def test():

    adress = requests.get("https://iceandfire.fandom.com/wiki/Cersei_Lannister")
    soup = BeautifulSoup(adress.text, 'html.parser')

    dico = {
        'name': "Cersei_Lannister",
        'siblings': [],
        'fmc': [],#parent/child
        'love': []
    }

    dico['siblings'] = getRelationAsList(soup, ['siblings'])
    dico['fmc'] = getRelationAsList(soup, ['father', 'mother', 'children'])
    dico['love'] = getRelationAsList(soup, ['spouse', 'lover'])
    
    print(dico)

def getRelationAsList(soup, source:list) -> list:
    list_to_return = []
    for s in source:
        search = soup.find('div',{'data-source':s})
        if search is not None:# so there's at least a link
            search = search.find_all('a')
            for src in search:
                list_to_return.append(src.get('href').replace('/wiki/',''))
    return list_to_return

test()