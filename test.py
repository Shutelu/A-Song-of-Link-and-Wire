#Question 3 
#use the file to creation a new dico
def chg_dico(file) -> dict:
    newdico = {}#dico to return 

    with open(file, 'r') as f:
        #for each line, add it to dico if exist
        for line in f:
            liste = []
            mot = ""
            line = line.strip()#remove escape from start and end
            if not line: # ignore empty lines
                continue  

            key, value = line.split(':', 1)#split from ':' 1 time and recover in 2 var
            # print(key)
            # print(value)
            #before add the key and value, transform value into list 
            value_no_bracket = value.replace("[","").replace("]","").replace(" ","") #remove '[' and ']' and " ' "
            # print("value no bracket :",value_no_bracket)
            #extract the " text's "
            #time one
            while "\"" in value_no_bracket:
                tmp_value = value_no_bracket
                first_quotes = value_no_bracket.find("\"")
                value_no_bracket = value_no_bracket[first_quotes+1:]
                second_quotes = value_no_bracket.find("\"")
                value_no_bracket = value_no_bracket[second_quotes+1+1:]#another +1 for the ' " ' we removed in firstquote
                #extracting
                liste.append(tmp_value[first_quotes+1:second_quotes+1])
                # print("finaleent :",tmp_value[first_quotes+1:second_quotes+1])
                # print("valeu apres ",value_no_bracket)
                # print(liste)

            value_no_bracket = value_no_bracket.replace("'","")
            # print("bracket",value_no_bracket)
            for index, char in enumerate(value_no_bracket):
                if char == ",":
                    if index < len(value_no_bracket)-2 and value_no_bracket[index:index+2] == ",_":
                        mot += char
                    else:
                        liste.append(mot)
                        mot = ""
                else:
                    mot += char

            # Ajout du dernier mot à la liste
            if mot:
                liste.append(mot)
            # print("value no bracket est :",value_no_bracket)
            # value_splited = value_no_bracket.split(",") #transform to list
            # print("la liste : ", liste)
            newdico[key] = liste #value_splited

    return newdico





newdico = chg_dico("f1.txt")
print(newdico["Historical_Timeline#After_Aegon's_Landing"])
#test Q3
# testdico = chg_dico("test.txt")
# print(testdico)
# print(testdico['Aenys_I'])
# testdico['Aenys_I']




# str = "Historical_Timeline#After_Aegon's_Landing"
# str += ", 'Storm%27s_End', 'Knighthood', 'Dragonstone'"
# print(str)
# ['some strings are present in between ', 'geeks', ' ', 'for', ' ', 'geeks', ' ']

# inputstring = 'some strings are present in between "geeks" "for" "geeks" '

# result = inputstring.split('"')[1::2]
# print(result);
