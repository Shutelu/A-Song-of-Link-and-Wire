from bs4 import BeautifulSoup
import requests

#==================================#
#=========LISTER LES LIENS=========#
#==================================#

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

#==================================#
#======CONSTRUCTION DU GRAPHE======#
#==================================#

#Question 2:
#save a dictionary into a file
def svg_dico(dico, file) -> None:

    with open(file, "a") as f:#auto close syntax, create if not exist or append 

        #if the dico exist
        if len(dico) > 0:
            f.write(f"{list(dico.keys())[0]}:{list(dico.values())[0]}\n")#take index 0 of key/value, because it only exist on index 0
        else:
            f.write("Empty dictionary\n")

#Question 3 
#use the file to create a new dictionary and return it
def chg_dico(file) -> dict:
    dico_to_return = {}

    with open(file, 'r') as f:

        #for each line, add it to dico if exist
        for line in f:

            line = line.strip()#remove escape from start and end if exist

            if not line: # ignore empty lines
                continue  

            key, value = line.split(':', 1)#split from ':' 1 time and recover in 2 var

            #replacement
            value_no_bracket = value.replace("[","").replace("]","").replace("'","").replace("\"","") #remove '[' and ']' and " ' "
            liste = value_no_bracket.split(", ")
            
            dico_to_return[key] = liste

    return dico_to_return

#Question 4
#add all links into a file with svg_dico
def graph_path() -> None: 
    file_name = "f1.txt"
    links_visited = []
    links_to_visite = ['Petyr_Baelish']

    #we visite links until there is nothing left
    while links_to_visite :
        first_elem = links_to_visite.pop(0) # get the first element 

        if first_elem in links_visited: # we leave if it's already visited
            continue 

        links_visited.append(first_elem)
        links = liste_liens(first_elem)
        svg_dico({first_elem:links},file_name) #write into the file
        
        for link in links:
            links_to_visite.append(link)
        
#=============================================#
#=VARIATION SUR LE THEME DU PLUS COURS CHEMIN=#
#=============================================#

#Question 5
#find the shortest way from A to B, graph = dictonary
def plus_court_chemin(graph, start, end):

    node_to_visite = [start]
    distances = {start: 0} # store visited nodes and their distances from 'start'
    parent = {start: None} # store nodes' parent to recover the shortest way
    
    while node_to_visite:
        node = node_to_visite.pop(0) # get the first element 

        if len(graph.get(node, [])) == 0: # if empty node, the links doesn't have any values
            continue

        # if we find the 'end' node
        if node == end: 
            chemin = []

            while node: # stop until node start which has a parent = None
                chemin.append(node)
                node = parent[node]

            chemin.reverse() # put 'chemin' in right order
            return chemin

        #search the values from the key 'node'
        for voisin in graph[node]:
            #if not already visited
            if voisin not in distances:
                distances[voisin] = distances[node] + 1 # new key 'voisin'
                parent[voisin] = node
                node_to_visite.append(voisin)
    
    return None # there is no path 



            
        

#==================================#
#===============TEST===============#
#==================================#

#test Q1
# print(liste_liens("Petyr_Baelish")) #test

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

#test Q5
test = chg_dico("f1.txt")

chemin = plus_court_chemin(test,"Dorne", "Rhaego")
print(chemin)




#Q3 alternative research O(n^2)
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