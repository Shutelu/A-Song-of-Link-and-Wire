from bs4 import BeautifulSoup
import requests

#Question 1:
def liste_liens(page) -> list:

    adresse = requests.get("https://iceandfire.fandom.com/wiki/" + page)
    soup = BeautifulSoup(adresse.text, 'html.parser')
    links_from_div = []

    #div principe ou on va chercher le main div
    main_div_to_research = soup.find('div', class_="mw-parser-output")

    #on reccupere les a du main_div_to_research, abreviation main('a')
    for a in main_div_to_research.find_all('a'):#find all return a list
        #on veut pas le liens de image d'affichage
        if not a.get('class') or (a.get('class')[0] not in ['image','image-thumbnail']):
            #on veut pas les ancres cad les liens '#'
            if not a.get('href').startswith('#'):
                # print(a.get('href'))
                links_from_div.append(a.get('href'))
    
    return links_from_div

#Question 2:
def svg_dico(dico, fichier) -> None:
    #auto close syntax
    with open(fichier, "a") as file:
        #prendre l'indice 0 de la list des clef et valeurs
        file.write("{}:{}\n".format(list(dico.keys())[0], list(dico.values())[0]))
    # print(list(dico.keys())[0])

    
#test Q2
# svg_dico({
#     "Petyr_Baelish": liste_liens("Petyr_Baelish")
# },"f1.txt")

#test Q1
# liste_liens("Petyr_Baelish") #test