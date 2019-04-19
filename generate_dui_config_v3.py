# -*- coding: utf-8 -*-

import pandas as pd
import math
import time

print('Reading CSV file...')
df = pd.read_csv('config.csv', sep=';')
print('Done reading CSV file.\n')
time.sleep(1)

file_version = input('What is the version of this file? >>> v')
XML_file = open("dynamic-ui-configuration-tm056.xml","w")

print('Creating XML file...')
#Getting today's date to put into header data
today = time.strftime("%b %d 20%y")
#Print XML file header
XML_file.write("<hiddenEntitiesConfiguration version=\"BE/NL v%s %s\"\n  xmlns=\"http://www.1worldsync.com/xml/ns/2016/12/DynamicUI\">\n   <hiddenEntitiesList targetMarket=\"056\"><!-- Belgium -->\n" % (file_version, today))

# 1. Je crée une colonne qui concatène tous les GPC en un grand string
# 2. Je lis chaque ligne de la nouvelle colonne et ajoute chaque nouvel élément dans une liste
# 3. Je parcoure la liste, et pour chaque éléménent, si la nouvelle colonne correspond, j'ajoute l'attribut dans cette section

segments_cols = ["Segment1","Segment2","Segment3","Segment4","Segment5","Segment6","Segment7","Segment8","Segment9","Segment10","Segment11","Segment12","Segment13","Segment14","Segment15","Segment16","Segment17","Segment18","Segment19","Segment20"]

df['Segments'] = ""

df.fillna("-", inplace=True)

myList = []
for index, row in df.iterrows():
    if index > 2:
        myList = row[7:-1].tolist()
        df.at[index, 'Segments'] = myList
        myList = []

big_List=[]
for index, row in df.iterrows():
    if (row['Segments'] not in big_List and row['Segments']!=''):
        big_List.append(row['Segments'])

        
#Verify that there are no groups without any GPC attached, and if there is/are, delete it/them.
for e in big_List:
    if all(items == '-' for items in e) == True:
        big_List.remove(e)

# Parcourir la liste - imprimer la partie <code> du XML - puis parcourir rows du df et ajouter entry attribute pour chaque row['Segment' == element de la liste]
print('Generating GPC segment groups and attributes to be hidden...')
already_used_attributes = [] # list of attributes that we already used, to avoid dubbles
for e in big_List:
    #Print <code> line in XML file
    XML_file.write("     <entry>\n")
    XML_file.write("        <codes>\n       <!-- PASTE GPC CODES HERE -->\n")
    for element in e:
        if element != "-":
            XML_file.write("           <code key=\"%s\"/>\n" % element)
    XML_file.write("        </codes>\n")

    #Print attributes to be hidden under these GPCs
    XML_file.write("        <entities>\n")
    for index, row in df.iterrows():
        
        #XML_file.write HIGHER LEVEL GROUP NAME
        if row['Loc1']!="-":
            XML_file.write("     <!-- #########################################################\n")
            XML_file.write("          #  %s   \n" % row['Loc1'])
            XML_file.write("          ######################################################### -->\n")

        #XML_file.write LOWER LEVEL GROUP NAME
        if row['Loc2']!="-":
            XML_file.write("        <!-- %s -->\n" % row['Loc2'])
        
        #XML file write every attribute to be hidden for this particular GPC group
        if row['Segments'] == e:
            if (row['What_to_hide']=="Attribute" and row['Attr_name_1WS'] not in already_used_attributes):
                XML_file.write("           <entity type=\"attribute\" key=\"%s\"/>\n" % row['Attr_name_1WS'])
                already_used_attributes.append(row['Attr_name_1WS'])
            elif (row['What_to_hide']=="Composite" and row['Composite_name_1WS'] not in already_used_attributes):
                XML_file.write("           <entity type=\"attribute\" key=\"%s\"/>\n" % row['Composite_name_1WS'])
                already_used_attributes.append(row['Composite_name_1WS'])
            elif (row['What_to_hide']=="Module" and row['Module_name_1WS'] not in already_used_attributes):
                XML_file.write("           <entity type=\"module\" key=\"%s\"/>\n" % row['Module_name_1WS'])
                already_used_attributes.append(row['Module_name_1WS'])
        else:
            pass

    XML_file.write("        </entities>\n")
    XML_file.write("     </entry>\n")
    already_used_attributes = []
	
XML_file.write("  </hiddenEntitiesList>\n</hiddenEntitiesConfiguration>")
print('Done.')
time.sleep(1)
print('Closing XML file...')
XML_file.close()
print('File closed, you can now use your XML configuration file.')
time.sleep(3)