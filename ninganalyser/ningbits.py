#Convert Ning output from Json to csv
#
#Example use:
#
#from ningbits import *
#ningjsontoexcel("yourfilename.json")
#
#Sara-Jayne Farmer 
#2012

import xlwt
import json
import os
import re

#Convert any apostrophes etc in the text into json-readable form
#(Python is stricter on json format than most)
#From http://stackoverflow.com/questions/8011692/valueerror-in-decoding-json
def asciirepl(match):
    return '\\u00' + match.group()[2:]


#Correct json file produced by Ning
#Sara-Jayne Farmer
#2012
def correct_json(jsonfile, ningtype):

    #Get Ning data from file
    fin = open(jsonfile)
    ff = fin.read()
    fin.close()
    
    #Put Ning data into Python-readable json format
    correcteddata = '{"' + ningtype + '":' + ff[1:len(ff)-1] + "}"
    p = re.compile(r'\\x(\w{2})')
    ascii_string = p.sub(asciirepl, correcteddata)
    return(ascii_string)


#Convert json file to csv file
# Jsonfile is the input json file
# ningtype is 'group', 'member' or 'event'
#
#Sara-Jayne Farmer
#2012
def ningjsontoexcel(jsonfile, ningtype):

    #Grab data lists out of the json
    ascii_string = correct_json(jsonfile, ningtype)
    data = json.loads(ascii_string)
    jsonkeys = data.keys() #data is a dictionary
    listtype = jsonkeys[0]
    dataset = data[listtype] #dataset is an array of entities: groups, members, etc.
    
    #Create excel workbook. Add a worksheet (summary) to it
    wbk = xlwt.Workbook()
    sumsheet = wbk.add_sheet('Summary', cell_overwrite_ok=True)

    #members: dataset is a dictionary with keys:
    #()

    #Handle groups
    #Group data format: dataset is a dictionary with keys:
    #(description, title, memberCount, contributorName,
    #approved, allowInvitations, updatedData, groupPrivacy,
    #url, members, createdDate, allowMemberMessaging, id)
    #Group: dataset['members'] is an array
    #Group: dataset['contributorName'] is an array
    #Want csv file that looks like:
    #key1,value
    #key2,value
    #members,value1,details1
    #members,value2,details2
    #...
    #contributorName,value1, details1
    #contributorName,value2, details2
    #...
    if ningtype == "group":
        print("Found groups")

        grow = 1   #Group's row in the CSV worksheet "summary"
        keycols = [] #Ordered list of all columns in the CSV worksheet "summary"
        listkeys = [] #List of all the keys that do *not* go into the CVS worksheet "summary"

        #loop around each group
        for group in dataset:

            #Get keys for this group
            #NB different groups have different sets of keys.
            groupkeys = group.keys()

            #Add new keys to the CVS worksheet 'summary' and to the list of CSV worksheet columns
            for key in groupkeys:
                
                #Don't put lists onto the summary page.
                if type(group[key]) == type(list()):
                    listkeys += [key]

                else:
                    #Write new key to worksheet header and put into keycols array
                    if (key in keycols) == False:
                        keycols = keycols + [key]
                        sumsheet.write(0,len(keycols)-1,key)
                        
                    col = keycols.index(key)
                    sumsheet.write(grow, col, [group[key]])

            #Convert contributorName from code to member's full name  
            cn = group['contributorName']
            initiator = cn #if we can't find the initiator, record the code instead
            
            #Print out list keys
            sheetname = group['url']
            sheetname = sheetname[:min(31,len(sheetname))] #Excel limits name to 31 chars
            groupsheet = wbk.add_sheet(sheetname, cell_overwrite_ok=True)
            prow = 1
            pkeys = []
            for person in group['members']:
                for pkey in person.keys():
                    if (pkey in pkeys) == False:
                        pkeys = pkeys + [pkey]
                        groupsheet.write(0,len(pkeys)-1,pkey)
                    pcol = pkeys.index(pkey)
                    groupsheet.write(prow,pcol,[person[pkey]])
                prow = prow+1

                #Check for group initiator's code
                if person['contributorName'] == cn:
                    col = keycols.index('contributorName')
                    sumsheet.write(grow, col, person['fullName'])
                
            grow = grow + 1

    #Save the new data in the CSV file
    wbk.save("ning_data_temp.xls")    
    return ()


