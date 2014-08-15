#!/usr/bin/env python
# -*- coding: cp1252 -*-

#This program contains small functionsa to analyse text files
#
#Example use:
#
#from analysetext import *
# [cs, cons] = summarise_skypechat("../data/skypechats/skypechat_SBTF General Chat Room.csv")
#
#Sara-Jayne Farmer
#2012

import csv
import nltk
import pycountry
import re


#======================================================================================
#Compare two stopword lists
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def compare_stopwords(infile):

    stops = {}

    #Import nltk stopword list
    nltkstops = nltk.corpus.stopwords.words('english')
    for stop in nltkstops:
        stops[stop.lower()] = "nltk"

    #Import file stopword list
    fin = open(infile)
    for line in fin:
        stop = line.strip().lower()
        if stops.has_key(stop) and stops[stop] == "nltk":
            stops[stop] = "both"
        else:
            stops[stop] = "file"
    fin.close()
    
    #Dump to file
    fout = open("stopwordlists.csv", 'wb')
    csvout = csv.writer(fout)
    for stop in sorted(stops.keys()):
        csvout.writerow([stop, stops[stop]])
    fout.close()
            
    return(stops)


#Analyse member list for specific skills
#Member list is a list of people's characteristics indexed by id
#Freqdist is a dict whose keys are words, and freqdist[word] is the number of words seen
#
#Sara-Jayne Farmer
#2012
def find_skills(memberlist, lookfor="languages", lookin="languages"):

    if lookfor=="languages":
        #Languages spoken    
        stopwords = ["excellent", "fluent", "proficient", "intermediate", "conversational"]
        #Pycountry contains list of all known languages (ISO 639)
        #knownkeys = ["english", "french", "arabic", "german"]
        knownkeys = []
        for lang in list(pycountry.languages):
            langname = lang.name.lower()
            #filter out language families
            if langname.find("languages") < 0 and langname.find("old") < 0:
                #Remove anything left in brackets
                langname = re.sub(r' \([^)]*\)', '', langname)
                #Split out multiple names for the same language
                knownkeys += langname.split(";") 
        
    else:
        #Not a specific topic
        stopwords = []
        knownkeys = []

    #Get skill statements from each member
    allskills = []
    for memberid in memberlist:
        if memberlist[memberid].has_key(lookin):
            memberskills = memberlist[memberid][lookin]
            allskills += [memberskills]

    #Get frequency distribution of non-stopwords in all member statements on language
    skillstring = ' '.join(w for w in allskills) #Make one long string
    skillwords = re.compile(r'[^A-Z^a-z]+').split(skillstring.lower())
    freqdist = nltk.FreqDist(skillwords)
        
    return (freqdist)
