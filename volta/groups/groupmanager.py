#!/usr/bin/env python
# -*- coding: cp1252 -*-

'''
General manager for lists of people, groups and chats from Ning, Skype and
Googlegroups

#Example use:
from groupmanager import *
compare_skypening(skypecsv, ningexcel)

Sara-Jayne Farmer
2012
'''

import csv
import re
import xlrd

#======================================================================================
#Compare people lists from Skype and Ning
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def crosscheck(skypeids, ningids, googleids):
        
    #Cross-check lists
    sset = set(skypeids)
    nset = set(ningids)
    snotn = sset.difference(nset)
    nnots = nset.difference(sset)
    
    #Basic paranoia about sock puppets
    if len(sset) != len(skypeids):
        print("Duplicates in Skype's Skype ids")
    if len(nset) != len(ningskypeids):
        print("Duplicates in Ning's Skype ids")

    #Dump to file
    fout = open("skypening.csv", 'wb')
    csvout = csv.writer(fout)
    csvout.writerow(['Skypeid', 'Ningid', 'Skype name'])
    for u in snotn:
        csvout.writerow([u, '', skypenames[u]])
    fout.close()

    #   return(stops)
