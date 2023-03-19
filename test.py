#Question 3 
#use the file to creation a new dictionary and return it
def chg_dico(file) -> dict:
    dico_to_return = {}

    with open(file, 'r') as f:

        #for each line, add it to dico if exist
        for line in f:

            liste = []
            # mot = ""
            line = line.strip()#remove escape from start and end if exist

            if not line: # ignore empty lines
                continue  

            key, value = line.split(':', 1)#split from ':' 1 time and recover in 2 var

            #before add the key and value, transform value into list 
            value_no_bracket = value.replace("[","").replace("]","").replace("'","").replace("\"","") #remove '[' and ']' and " ' "
            liste = value_no_bracket.split(", ")
            
        
            dico_to_return[key] = liste

    return dico_to_return





newdico = chg_dico("test.txt")
print(newdico)
# #test Q3
# # testdico = chg_dico("test.txt")
# # print(testdico)
# # print(testdico['Aenys_I'])
# # testdico['Aenys_I']




# # str = "Historical_Timeline#After_Aegon's_Landing"
# # str += ", 'Storm%27s_End', 'Knighthood', 'Dragonstone'"
# # print(str)
# # ['some strings are present in between ', 'geeks', ' ', 'for', ' ', 'geeks', ' ']

# # inputstring = 'some strings are present in between "geeks" "for" "geeks" '

# # result = inputstring.split('"')[1::2]
# # print(result);

# maliste = "'The_Vale', 'Aegon_I_Targaryen', 'Jaehaerys_I_Targaryen', 'Rhaena_Targaryen'"
# l = maliste.replace("'","").split(",")
# print(l)


# ============
# #Question 3 
# #use the file to creation a new dictionary and return it
# def chg_dico(file) -> dict:
#     dico_to_return = {}

#     with open(file, 'r') as f:

#         #for each line, add it to dico if exist
#         for line in f:

#             liste = []
#             mot = ""
#             line = line.strip()#remove escape from start and end if exist

#             if not line: # ignore empty lines
#                 continue  

#             key, value = line.split(':', 1)#split from ':' 1 time and recover in 2 var

#             #before add the key and value, transform value into list 
#             value_no_bracket = value.replace("[","").replace("]","").replace(" ","") #remove '[' and ']' and " ' "

#             #extract the single quote from " text's ", the order in the list might change but it's not a big deal
#             #time one
#             while "\"" in value_no_bracket: #search ' " '
#                 tmp_value = value_no_bracket #store default
#                 first_quotes = value_no_bracket.find("\"")
#                 value_no_bracket = value_no_bracket[first_quotes+1:]
#                 second_quotes = value_no_bracket.find("\"")
#                 value_no_bracket = value_no_bracket[second_quotes+1+1:]#another +1 for the ' " ' we removed in firstquote,tatonement
#                 #extracting
#                 liste.append(tmp_value[first_quotes+1:second_quotes+1])

#             value_no_bracket = value_no_bracket.replace("'","")

#             #add every word spliting from "," to the list
#             for index, char in enumerate(value_no_bracket):
#                 if char == ",":
#                     #-1 for 0 and -1 for current
#                     if index < len(value_no_bracket)-2 and value_no_bracket[index:index+2] == ",_":
#                         mot += char
#                     else:
#                         liste.append(mot)
#                         mot = ""
#                 else:
#                     mot += char

#             # add last word 
#             if mot:
#                 liste.append(mot)
        
#             dico_to_return[key] = liste

#     return dico_to_return