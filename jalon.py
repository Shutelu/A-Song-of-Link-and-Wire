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

#Question 5 : 
#find the shortest way from A to B, graph = dictonary
def plus_court_chemin(graph, source, target) -> list:

    nodes_to_visite = [source]
    parent = {source: None} # store nodes' parent to recover the shortest way
    
    while nodes_to_visite:
        node = nodes_to_visite.pop(0) # get the first element 

        # if we find the 'end' node
        if node == target: 
            chemin = []

            while node: # stop until node start which has a parent = None
                chemin.append(node)
                node = parent[node]

            chemin.reverse() # put 'chemin' in right order
            return chemin

        if len(graph.get(node, [])) == 0: # if empty node, the links doesn't have any values
            continue

        #search the values from the key 'node'
        for voisin in graph[node]:
            #if not already visited
            if voisin not in parent:
                parent[voisin] = node
                nodes_to_visite.append(voisin)
    
    return None # there is no path 

#Question 6
#cherche le chemin de pois minimal
def pcc_voyelles(graph, source, target) -> list:

    nodes_to_visite = [source]
    nodes_weight = {source: 0}
    parent = {source: None}
    min_path_to_return = []

    #we stop until nodes_to_visite is empty to find the shortest path
    #this 'while' loop will setup the optimal way to find the target 
    while nodes_to_visite:
        node = nodes_to_visite.pop()

        if (len(graph.get(node, [])) == 0) or (node == target): # empty node or target node we can continue
            continue
        
        #define the weight of each nodes
        for neighbour in graph[node]:

            cost = nodes_weight[node] + len(neighbour) + nb_voyelles(neighbour)

            #if the neighbour already has a weight we can compare
            if neighbour in nodes_weight:
                # cost > n
                if cost > nodes_weight[neighbour]:
                    continue
                
            # cost < n or not in distances
            if neighbour not in nodes_to_visite:
                nodes_to_visite.append(neighbour) #add to the parcours
            nodes_weight[neighbour] = cost # add the distance
            parent[neighbour] = node

    #set our path from source to target with the min weight
    while target is not None:
        min_path_to_return.append(target)
        target = parent[target]
    min_path_to_return.reverse()
  
    return min_path_to_return

#Q6 private method : return the number of vowels of n
def nb_voyelles(n) -> int:
    nb = 0
    for v in n:
        if v in 'aeiouyAEIOUY':
            nb += 1
    return nb

#================================#
#=====INCESTE ET DESCENDANCE=====#
#================================#

#Question 7
#we're going to look for all the characters form Category:Characters page to create our graph and put into a file named characters_list
def graph_of_characters() -> None:

    list_of_dico = []
    list_of_characters = getListOfCharacters()

    #for every characters in our list
    for char in list_of_characters:
        list_of_dico.append(getDicoFromCharacter(char))
    
    #write into files
    with open("characters_list.txt", "a") as f:
        
        #write for every element of the list 
        for dico in list_of_dico:
            #sibling -> sibling
            #fmc -> [parent],[children]
            #love -> spouse/lover
            f.write(f"{dico['name']}:'siblings':{dico['siblings']}| 'fmc':{dico['fmc']}| 'love':{dico['love']}\n")

#Q7 private method : search the all characters in category and return the list of all the characters
def getListOfCharacters() -> list:
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    list_of_characters = [] 

    for alp in alphabet:
        adress = requests.get("https://iceandfire.fandom.com/wiki/Category:Characters?from=" + alp)
        soup = BeautifulSoup(adress.text, 'html.parser')

        #add to the dictonary
        for a in soup.find_all('a',class_="category-page__member-link"):
            key = a.get('href').replace("/wiki/",'')
            list_of_characters.append(key)

    return list_of_characters

#Q7 private method : return a dictionary with all the relation of the character
def getDicoFromCharacter(character) -> dict:
    adress = requests.get("https://iceandfire.fandom.com/wiki/" + character)
    soup = BeautifulSoup(adress.text, 'html.parser')

    dico_to_return = {
        'name': character,
        'siblings': [],
        'fmc': [],#parent/child
        'love': []
    }

    dico_to_return['siblings'] = getRelationAsList(soup, ['siblings'])
    # dico_to_return['fmc'] = getRelationAsList(soup, ['father', 'mother', 'children'])
    dico_to_return['fmc'].append(getRelationAsList(soup, ['father', 'mother']))
    dico_to_return['fmc'].append(getRelationAsList(soup, ['children']))
    dico_to_return['love'] = getRelationAsList(soup, ['spouse', 'lover'])
    
    return dico_to_return

#Q7 private method : return relationship as a list  
def getRelationAsList(soup, source:list) -> list:
    list_to_return = []
    for s in source:
        search = soup.find('div',{'data-source':s})
        if search is not None:# so there's at least a link
            search = search.find_all('a')
            for src in search:
                list_to_return.append(src.get('href').replace('/wiki/',''))
    return list_to_return

#Question 8
#We print the list of incestuous couples + list_of_couple file
def incestuousCouple(file):
    list_of_couple = []

    with open(file, 'r') as f:

        for line in f:

            line = line.strip()#remove escape from start and end if exist
            if not line: # ignore empty lines
                continue  

            key, value = line.split(':', 1)#split from ':' 1 time and recover in 2 var

            siblings = []
            fmc = [] #[parent], [children]
            love = [] #spouse/lover

            #acquire the info
            splited_value = value.replace("'","").split("| ")
            
            #process the info
            for info in splited_value:

                #obtaining the key and value of info
                info_key, info_value = info.split(':',1)

                print("1-info value:", info_value)
                print("key :",info_key)
                processed_info_value = info_value.replace('[','').replace(']','')
                print("2-process :", processed_info_value)
                if len(processed_info_value) < 1:
                    continue
                if info_key == 'siblings':
                    siblings = processed_info_value.split(", ")
                if info_key == 'fmc':
                    fmc = processed_info_value.split(", ")
                if info_key == 'love':
                    love = processed_info_value.split(", ")
                print("3-sib:",siblings)
                print("4-fmc:",fmc)
                print("5-love:",love)
                print("")
            #check the relation
            for sib in siblings:
                if sib in love:
                    list_of_couple.append((key,sib))
            for f in fmc:
                if f in love:
                    list_of_couple.append((key,f))

            # print("ligne : ", line)

    with open("list_of_couple.txt","w") as f:

        for i in list_of_couple:
            print(i)
            f.write(f"{i}\n")

# #Question 9
# def graph_of_ancesters(file):
#     list_of_characters = []
#     dico_of_ancesters = {}
    
#     with open(file, "r") as f:
        
#         for line in f:
#             line = line.strip()#remove escape from start and end if exist
#             if not line: # ignore empty lines
#                 continue  

            


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
# test = chg_dico("f1.txt")
# chemin = plus_court_chemin(test,"Dorne", "Rhaego")
# print(chemin)

#test Q6
# dico = chg_dico("f1.txt")
# path = pcc_voyelles(dico, "Dorne", "Rhaego")
# print(path)

#test Q7
# graph_of_characters()

#test Q8
incestuousCouple('characters_list.txt')

#test Q9