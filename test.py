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

a = "Targaryen"
print(nb_voyelles(a) + len(a))