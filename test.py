t = "['hi','hey','ho']"
d = t.replace("[","").replace("]","").replace("'","")
d2 = d.split(",")

print(d2[2])
# d = {'x' : [1,2,3]}
# print(d['x'][1])