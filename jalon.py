#Contributors : Changkai WANG 21980438, Liyam AIT OUAKLI 32013066
from bs4 import BeautifulSoup
import requests

#==================================#
#=========LISTER LES LIENS=========#
#==================================#

#Question 1:
#Desc : return all the links of a page in a list
#Args : page(str) = page of the wiki to find the links
def liste_liens(page) -> list:

    links_to_return = []

    #access to the related page and acquire its html source
    adress = requests.get("https://iceandfire.fandom.com/wiki/" + page)
    soup = BeautifulSoup(adress.text, 'html.parser')
    
    #acquire the div which contains all the userful links
    main_div_to_research = soup.find('div', class_="mw-parser-output")

    #processing every links from the div and adding to links_to_return
    for a in main_div_to_research.find_all('a'): # find_all() return a list

        #acquire the class of the link a to process it
        a_class = a.get('class')
        forbidden_class = ['image','image-thumbnail']

        #autorize the adding of the links without class and exclude links that has a class in forbidden_class
        if (not a_class) or (len(a_class) > 0 and a_class[0] not in forbidden_class) or (len(a_class) > 1 and a_class[1] not in forbidden_class):

            #exlude links starting with '#' (anchor) and 'https:' or 'http:' or links with ':' (other website redirection or categories)
            if (not a.get('href').startswith('#') and not ":" in a.get('href')):

                link_without_wiki = a.get('href').replace("/wiki/",'')#remove the '/wiki/' before the link

                if link_without_wiki not in links_to_return:
                    links_to_return.append(link_without_wiki)

    return links_to_return

#==================================#
#======CONSTRUCTION DU GRAPHE======#
#==================================#

#Question 2:
#Desc : write the information of a dictionary into a file
#Args : dico = the dictonary, file = the file to write the information
def svg_dico(dico, file) -> None:

    #open with auto close syntax, and append to the end of the file
    with open(file, "a") as f:

        dico_len = len(dico)

        #if the dico exist
        if dico_len > 0:

            for i in range(0,dico_len):

                #f string formatting to write into the file
                f.write(f"{list(dico.keys())[i]}:{list(dico.values())[i]}\n")
        else:
            f.write("Empty dictionary\n")

#Question 3 
#Desc : use a file to create and return a new dictionary
#Args : file = the file containing the info to create the dico
def chg_dico(file) -> dict:

    dico_to_return = {}

    #open in read mode
    with open(file, 'r') as f:

        #if the line exist add it to dico_to_return
        for line in f:

            #remove space from start and end of the line if exist
            line = line.strip()

            # ignore empty lines
            if not line: 
                continue  

            #split from ':', 1 time and recover in 2 var, key and value are str
            key, value = line.split(':', 1)

            #removing the unwanted char
            processed_value = value.replace("[","").replace("]","").replace("'","").replace("\"","")
            list_of_value = processed_value.split(", ")
            
            dico_to_return[key] = list_of_value

    return dico_to_return

#Question 4
#Desr : create a representation of the wiki in form of key:value into a file with svg_dico()
def graph_path() -> None: 

    file_name = "wiki_representation.txt"
    links_visited = []
    links_to_visite = ['Petyr_Baelish']

    #visite links until there is nothing left
    while links_to_visite :

        # get the first element 
        page = links_to_visite.pop(0)

        #leave if already visited
        if page in links_visited: 
            continue 

        links_visited.append(page)
        list_of_links = liste_liens(page)
        svg_dico({page:list_of_links}, file_name)
        
        #adding all links of the page to our parcours
        for link in list_of_links:
            links_to_visite.append(link)
        
#=============================================#
#=VARIATION SUR LE THEME DU PLUS COURS CHEMIN=#
#=============================================#

#Question 5 : 
#Desc : find the shortest way from A to B, graph = dictonary
#Args : graph = the dictonary to visite, source = starting point, target = target page to search
def plus_court_chemin(graph, source, target) -> list:

    nodes_to_visite = [source]
    parent = {source: None} # store nodes' parent to recover the shortest way
    
    while nodes_to_visite:
        node = nodes_to_visite.pop(0) # get the first element 

        # if we find the 'target' node
        if node == target: 
            path = []

            #stop until node start which has a parent = None
            while node: 
                path.append(node)
                node = parent[node]

            path.reverse() # put 'path' in right order
            return path

        # if empty node, the links doesn't have any values
        if len(graph.get(node, [])) == 0: 
            continue

        #search the values from the key 'node'
        for voisin in graph[node]:
            #if not already visited
            if voisin not in parent:
                parent[voisin] = node
                nodes_to_visite.append(voisin)
    
    return None # there is no path 

#Question 6
#Desc : find the minimal weight path
#Args : graph = the dictonary to visite, source = starting point, target = target page to search
def pcc_voyelles(graph, source, target) -> list:

    nodes_to_visite = [source]
    nodes_weight = {source: 0}
    parent = {source: None}
    min_path_to_return = []

    #we stop until nodes_to_visite is empty to find the shortest path (optimal weight)
    #this 'while' loop will setup the optimal way to find the target 
    while nodes_to_visite:
        node = nodes_to_visite.pop()

        # if empty node or target node we can 'continue'
        if (len(graph.get(node, [])) == 0) or (node == target): 
            continue
        
        #define the weight of each nodes
        for neighbour in graph[node]:

            cost = nodes_weight[node] + len(neighbour) + nb_voyelles(neighbour)

            #if the neighbour already has a weight we can compare
            if neighbour in nodes_weight:
                # cost > n (already got the smallest weight)
                if cost > nodes_weight[neighbour]:
                    continue
                
            # cost < n (change to a smaller weight) or not in nodes_weight
            if neighbour not in nodes_to_visite: #to not parcours again (adding time complexity)
                nodes_to_visite.append(neighbour) #add to the parcours

            nodes_weight[neighbour] = cost # add the weight
            parent[neighbour] = node

    #set our path from source to target with the min weight
    while target is not None:
        min_path_to_return.append(target)
        target = parent[target]
    min_path_to_return.reverse()
  
    return min_path_to_return

#Q6
#Desc : return the number of vowels of n
#Args : n = a string
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
#Desc : look for all the characters from Category:Characters page to create our graph and put into a file named characters_list.txt
def graph_of_characters() -> None:

    list_of_dico = []
    list_of_characters = getListOfCharacters()

    #for every characters in our list
    for char in list_of_characters:
        list_of_dico.append(getDicoFromCharacter(char))
    
    #write the characters list into the file
    with open("characters_list.txt", "w") as f:
        
        #write for every element of the list 
        for dico in list_of_dico:

            #sibling -> sibling
            #fmc -> [parent],[children]
            #love -> spouse/lover
            #the attributs is separated with '| ' for better processing

            f.write(f"{dico['name']}:'siblings':{dico['siblings']}| 'fmc':{dico['fmc']}| 'love':{dico['love']}\n")

#Q7
#Desc : search all characters of the wiki and return it in a list
def getListOfCharacters() -> list:

    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    list_of_characters = [] 

    for alp in alphabet:

        adress = requests.get("https://iceandfire.fandom.com/wiki/Category:Characters?from=" + alp)
        soup = BeautifulSoup(adress.text, 'html.parser')

        #adding all names of the character starting with 'alp' in list_of_characters
        for a in soup.find_all('a',class_="category-page__member-link"):

            key = a.get('href').replace("/wiki/",'')
            list_of_characters.append(key)

    return list_of_characters

#Q7
#Desc : return a dictionary with all the relation of the character
#the form of the relation with be {'siblings':[siblings,..], 'fmc':[[parent,..],[children,..]], 'love:[spouse/lover,..]}
#Args : character = character's name
def getDicoFromCharacter(character) -> dict:

    adress = requests.get("https://iceandfire.fandom.com/wiki/" + character)
    soup = BeautifulSoup(adress.text, 'html.parser')

    dico_to_return = {
        'name': character,
        'siblings': [],
        'fmc': [], # parent/children
        'love': [] # spouse/lover
    }

    dico_to_return['siblings'] = getRelationAsList(soup, ['siblings'])
    dico_to_return['fmc'].append(getRelationAsList(soup, ['father', 'mother']))
    dico_to_return['fmc'].append(getRelationAsList(soup, ['children']))
    dico_to_return['love'] = getRelationAsList(soup, ['spouse', 'lover'])
    
    return dico_to_return

#Q7 
#Desc : return relationship as a list  
#Args : soup = html source to search, source = list of data-source to search
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
#Desc : print the list of incestuous couples in stdout and write into list_of_couple.txt
#Args : file = file containing the list of characters of the wiki
def incestuousCouple(file):

    list_of_couple = []

    with open(file, 'r') as f:

        for line in f:

            line = line.strip()
            if not line:
                continue  

            #obtaining the key=character and value=all relations
            key, value = line.split(':', 1)

            siblings = []
            fmc = [] #[parent], [children]
            love = [] #spouse/lover

            acquire_list_info = value.replace("'","").split("| ")
            
            #process the info
            for info in acquire_list_info:

                #obtaining the key and value of info (siblings, fmc, love)
                relation_key, relations = info.split(':',1)

                processed_relations = relations.replace('[','').replace(']','')

                if len(processed_relations) < 1:
                    continue
                if relation_key == 'siblings':
                    siblings = processed_relations.split(", ")
                if relation_key == 'fmc':
                    fmc = processed_relations.split(", ")
                if relation_key == 'love':
                    love = processed_relations.split(", ")

            #check the relation
            for sib in siblings:
                if sib in love:
                    list_of_couple.append((key,sib))

            for f in fmc:
                if f in love:
                    list_of_couple.append((key,f))

    #write into file
    with open("list_of_incestuous_couple.txt","w") as f:

        for i in list_of_couple:
            print(i)
            f.write(f"{i}\n")

#Question 9
#Desc : return the graph of descendences in form of 'parent -> children'
#Args : file = file containing the list of characters of the wiki
def graph_of_descendences(file):

    dico_of_ancesters = {}

    with open(file, "r") as f:
        
        for line in f:
            line = line.strip()
            if not line:
                continue  

            #obtaining the key=character and value=all relations
            key, value = line.split(':', 1)

            #getting siblings, fmc, love
            acquire_relations = value.replace("'","").split("| ")

            #only acquire the fmc
            acquire_fmc = acquire_relations[1].replace("fmc:","")

            #spliting between parents and children
            list_toprocess_fmc = acquire_fmc.split("], [")
            
            #list of parent
            str_of_parents = list_toprocess_fmc[0].replace("[[","").replace("]]","") #str
            list_of_parents = str_of_parents.split(", ")

            #list of children
            list_of_children = list_toprocess_fmc[1].replace("[[","").replace("]]","") #str

            #for parent
            for parent in list_of_parents:
                if parent not in dico_of_ancesters:
                    if parent == "": continue # for the parent = "", otherwise there will be parent with no name
                    dico_of_ancesters[parent] = key

            #for children
            dico_of_ancesters[key] = list_of_children
         
    #write the descendances into a file
    with open("list_of_descendances.txt","w") as f :
        #if the dico exist
        for key, value in dico_of_ancesters.items():
            # parent -> children
            f.write(f"{key} -> {value}\n")
            

#==================================#
#===============TEST===============#
#==================================#

#test Q1
# print("Links of the page 'Petyr_Baelish' :\n",liste_liens("Petyr_Baelish")) 

# test Q2
# svg_dico(
#     {"Petyr_Baelish": liste_liens("Petyr_Baelish")},
#     "svg_test.txt"
# )

#test Q3
# chg_test = chg_dico("chg_test.txt")
# for chg in chg_test:
#     print(f"{chg}:{chg_test[chg]}")

#test Q4
# graph_path()

#test Q5
# pcc_test = chg_dico("wiki_representation.txt")
# chemin = plus_court_chemin(pcc_test,"Dorne", "Rhaego")
# print(chemin)

#test Q6
# pcc_v_test = chg_dico("wiki_representation.txt")
# path = pcc_voyelles(pcc_v_test, "Dorne", "Rhaego")
# path2 = pcc_voyelles(pcc_v_test, "Dorne", "Bastardy")
# print(path)
# print(path2)

#test Q7
# graph_of_characters()

#test Q8
# incestuousCouple('characters_list.txt')

#test Q9
# graph_of_descendences('characters_list.txt')