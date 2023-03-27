from bs4 import BeautifulSoup
import requests

# tupel = [('A',1),('B',2),('C',3)]
# t = tupel[1]
# cible, poids = t
# print(cible)
# print(poids)

dico_of_ancesters = {"david":2,"uni":3,"micela":4}
with open("list_of_decendances.txt","w") as f2 :
        print("yep")
        #if the dico exist
        t =1
        for characters, value in dico_of_ancesters.items():
            if t >10: 
            name = characters
            print(name)
            f2.write(f"{name}\n")
            # if len(dico_of_ancesters) > 0:
            #     f2.write(f"change {name}:{dico_of_ancesters[characters]}\n")
            # else:
            #     f2.write("Empty dictionary\n")