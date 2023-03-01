from bs4 import BeautifulSoup
import requests

#Question 1:
def liste_liens(page) -> list:

    adresse = requests.get("https://iceandfire.fandom.com/wiki/" + page)
    soup = BeautifulSoup(adresse.text, 'html.parser')
    links_from_div = []

    main_div_to_research = soup.find('div', class_="mw-parser-output")

    #test if we can add the link a in our list links_from_div
    for a in main_div_to_research.find_all('a'):#find_all return a list

        #aide explication
        # if a.get('class'):
        #     print(a.get('class')[0])
        #     if(len(a.get('class')) > 1):
        #         print(a.get('class')[1])
        #on veut pas le liens de image d'affichage

        class_a = a.get('class')
        forbidden_class = ['image','image-thumbnail']

        #exclude forbidden class and alias
        # if not a.get('class') or (len(a.get('class')) > 0 and a.get('class')[0] not in ['image','image-thumbnail']):#old
        if not class_a or (len(class_a) > 0 and class_a[0] not in forbidden_class) or (len(class_a) > 1 and class_a[1] not in forbidden_class):#new

            if not a.get('href').startswith('#'):
                link_not_wiki = a.get('href').replace("/wiki/",'')
                # print("enelever :" + link_not_wiki)
                links_from_div.append(link_not_wiki)
                # print(a.get('href'))

    return links_from_div

#Question 2:
#save a dico into the file
def svg_dico(dico, file) -> None:

    #auto close syntax
    with open(file, "a") as f:

        #prendre l'indice 0 de la list des clef et valeurs
        # file.write("{}:{}\n".format(list(dico.keys())[0], list(dico.values())[0]))#old
        if len(dico) > 0:
            f.write(f"{list(dico.keys())[0]}:{list(dico.values())[0]}\n")
        else:
            f.write("Empty dictionary\n")

#Question 3 
#use the file to creation a new dico
def chg_dico(file) -> dict:
    newdico = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()#remove escape
            if not line:
                continue  # ignorer les lignes vides
            key, value = line.split(':', 1)#split from : 1 time
            newdico[key] = value
    return newdico

#Question 4
def graph_path(): 
    pass


#test Q1
liste_liens("Petyr_Baelish") #test
# test Q2
svg_dico({
    "Petyr_Baelish": liste_liens("Petyr_Baelish")
},"f1.txt")
#test Q3
testdico = chg_dico("f1.txt")

