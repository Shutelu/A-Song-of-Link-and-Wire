from bs4 import BeautifulSoup
import requests

#Question 1:
#return all the links of the page in a list
def liste_liens(page) -> list:

    adress = requests.get("https://iceandfire.fandom.com/wiki/" + page)
    soup = BeautifulSoup(adress.text, 'html.parser')
    links_to_return = []

    #search links in the main div
    main_div_to_research = soup.find('div', class_="mw-parser-output")

    #add the link 'a' in our list 
    for a in main_div_to_research.find_all('a'):#find_all return a list

        a_class = a.get('class')
        forbidden_class = ['image','image-thumbnail']

        #autorize links without class and exclude links that has a class in forbidden_class
        if (not a_class) or (len(a_class) > 0 and a_class[0] not in forbidden_class) or (len(a_class) > 1 and a_class[1] not in forbidden_class):

            #exlude links starting with '#' (anchor) and 'https:' or 'http:' or links with ':' (other website redirection)
            if (not a.get('href').startswith('#') and not ":" in a.get('href')):
                link_without_wiki = a.get('href').replace("/wiki/",'')#remove the '/wiki/' before the link
                links_to_return.append(link_without_wiki)

    return links_to_return

#Question 2:
#save a dico into the file
def svg_dico(dico, file) -> None:

    with open(file, "a") as f:#auto close syntax, create if not exist or append 

        #if the dico exist
        if len(dico) > 0:
            f.write(f"{list(dico.keys())[0]}:{list(dico.values())[0]}\n")#take index 0 of key/value, because it only exist on index 0
        else:
            f.write("Empty dictionary\n")

#Question 3 
#use the file to creation a new dico
def chg_dico(file) -> dict:
    newdico = {}#dico to return 

    with open(file, 'r') as f:#only read 
        #for each line, add it to dico if exist
        for line in f:
            line = line.strip()#remove first/last space and "\n"

            if not line:
                continue  # ignore empty lines

            key, value = line.split(':', 1)#split from ':' 1 time and recover in 2 var

            #before add the key and value, transform value into list 
            value_no_bracket = value.replace("[","").replace("]","").replace("'","").replace(" ","") #remove '[' and ']' and " ' " and space
            value_splited = value_no_bracket.split(",") #transform to list
            newdico[key] = value_splited

    return newdico

#Question 4
def graph_path() -> None: 
    file_name = "f1.txt"
    links_visited = []
    links_to_visite = ['Petyr_Baelish']

    #we visite links until there is nothing left
    while links_to_visite :

        first_elem = links_to_visite.pop(0) # recover the first element 

        if first_elem in links_visited: # we leave if it's already visited
            continue 

        #test
        # with open('test.txt','a') as f:
        #     links_visited.append(first_elem)
        #     f.write(f"first element {first_elem} \n")
        #     f.write(f"to visite {links_to_visite} \n")
        #     f.write(f"visited {links_visited}\n")
        #     links = liste_liens(first_elem)
        #     f.write(f"all : {first_elem}:{links}\n")
        #     f.write("\n")

        links_visited.append(first_elem)
        links = liste_liens(first_elem)
        svg_dico({first_elem:links},file_name) #write into the file
        
        for link in links:
            # if link in links_visited:
            #     continue
            links_to_visite.append(link)
        
#Question 5
def plus_court_chemin(file, start, end):
    with open(file,"r") as f:
        #on reccupere les donnees dans un dictionnaire
        dico = chg_dico(file)

        page_to_visit = [start]
        visited = {start:0} #cle = page name, value = distance 

        while page_to_visit:
            current_page = page_to_visit.pop(0)

            
        

#==================================#
#===============TEST===============#
#==================================#

#test Q1
print(liste_liens("Petyr_Baelish")) #test

# test Q2
# svg_dico({
#     "Petyr_Baelish": liste_liens("Petyr_Baelish")
# },"f1.txt")

#test Q3
# testdico = chg_dico("f2.txt")
# print(testdico)
# print(testdico['Aenys_I'])

#test Q4
# graph_path()




#Q3 alternative research
# str = "Aegonfort,Dragonstone,King_of_the_Andals,_the_Rhoynar,_and_the_First_Men,Lord_of_the_Seven_Kingdoms"
# l = []
# mot = ""
# for i in str:
#     if not ("," in str):
#         break
#     firstocc = str.find(",")
#     if str[firstocc+1] == "_":
#         mot += str[:firstocc+1]
#         str = str[firstocc+1:]
#     else :
#         if len(mot) > 0:
#             mot += str[:firstocc]
#         else:
#             mot = str[:firstocc]
#         l.append(mot)
#         mot = ""
#         str = str[firstocc+1:]
#         print(mot)
#     print("apres traitement : ",str)
# if str:
#     l.append(str)
# print(l)