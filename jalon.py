from bs4 import BeautifulSoup
import requests

#Question 1:
def liste_liens(page) -> list:

    adresse = requests.get("https://iceandfire.fandom.com/wiki/" + page)
    soup = BeautifulSoup(adresse.text, 'html.parser')
    links_from_div = []

    main_div_to_research = soup.find('div', class_="mw-parser-output")

    #abreviation main('a')
    for a in main_div_to_research.find_all('a'):#find_all return a list

        #aide explication
        # if a.get('class'):
        #     print(a.get('class')[0])
        #     if(len(a.get('class')) > 1):
        #         print(a.get('class')[1])
        #on veut pas le liens de image d'affichage

        class_a = a.get('class')
        forbid = ['image','image-thumbnail']

        # if not a.get('class') or (len(a.get('class')) > 0 and a.get('class')[0] not in ['image','image-thumbnail']):#old
        if not class_a or len(class_a) > 0 and class_a[0] not in forbid or len(class_a) > 1 and class_a[1] not in forbid:#new

            if not a.get('href').startswith('#'):
                links_from_div.append(a.get('href'))
                # print(a.get('href'))

    return links_from_div

#Question 2:
def svg_dico(dico, fichier) -> None:

    #auto close syntax
    with open(fichier, "a") as file:

        #prendre l'indice 0 de la list des clef et valeurs
        # file.write("{}:{}\n".format(list(dico.keys())[0], list(dico.values())[0]))#old
        file.write(f"{list(dico.keys())[0]}:{list(dico.values())[0]}\n")#new

    
# test Q2
svg_dico({
    "Petyr_Baelish": liste_liens("Petyr_Baelish")
},"f1.txt")

#test Q1
liste_liens("Petyr_Baelish") #test