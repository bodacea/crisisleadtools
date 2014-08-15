#Grab messages from a named Skype chat, using Skype4Py from a Linux PC
#
#Example use:
#
#import skypechat
#
#s = skypechat.Logger()
#i = s.get_chatroom("Ushahidi Dev Chat")
#s.dump_messages(i)
#
#Sara-Jayne Farmer 
#2012

import Skype4Py
from collections import Counter
import csv

#Produce time-sorted list
def message_timestamp_cmp(x, y):
    return int(x.Timestamp - y.Timestamp)


#Class to handle Skype chats
#Sara-Jayne Farmer
#2012
class Logger:
    
    name = "Logger"  #Class name
    sconn = Skype4Py.Skype(Transport='x11') #Skype connection
    chats = ""                #Chats
    mlist = ""                #Message list
    
    
    #Initialise Skype link
    def __init__(self):
        print("Setting up link to Skype")

        #Set up Skype
        #Need to have Skype running first, then click on "allow to access skype"
        #message in there when this program starts
        self.sconn = Skype4Py.Skype(Transport='x11')
        self.sconn.FriendlyName = "Skype_chat_trawler"
        self.sconn.Attach()
        
    
    #Get index for a named chat
    def get_chatroom(self, chatname):
        
        #Find the named chat in the list of attached chats
        self.chats = self.sconn.Chats
        for i in range(0,len(self.chats)):
            if(self.chats[i].FriendlyName.find(chatname) != -1):
                print("Found chatroom " + self.chats[i].FriendlyName)
                return(i)
        return(-1)
    
    
    #Get messages for a chat
    def get_messages(self, chatroom):
        
        #Grab the messages for this chat
        messages = self.chats[chatroom].Messages
        print(self.chats[chatroom].FriendlyName)

        #Convert and sort (by time) the list of messages
        self.mlist = list(messages)
        self.mlist.sort(message_timestamp_cmp)

        return(self.mlist)

    #Profile contributors
    def profile_writers(self):
        
        #Count contributions to chat
        cnt = Counter()
        for m in self.mlist:
            cnt[m.FromDisplayName] += 1

        print("Messages: "+ str(len(self.mlist)) + " writers: " + str(len(cnt)))
        return(cnt)

    #Locate chat members
    def find_members(self, chatroom):
        
        #Count contributions to chat
        countries = Counter()
        cities = Counter()
        timezones = Counter()
        for u in self.chats[chatroom].Members:
            countries[u.Country] += 1
            cities[u.City] += 1
            timezones[u.Timezone] += 1

        print("Countries: "+ str(len(countries)) + " cities: " + str(len(cities)))
        return([countries, cities, timezones])
        

    #Write messages for a chatroom to a csv file
    def dump_messages(self, chatroom):
        
        #Open CSV file to hold message data
        roomname = self.chats[chatroom].FriendlyName
        outfile = "skypechat_" + roomname[:min(len(roomname),10)] + ".csv"
        f = open(outfile, 'wb')
        csvout = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        self.get_messages(chatroom)
        for m in self.mlist:
            who  = m.FromHandle
            what = m.Body
            when = m.Timestamp
            wha  = m.Type
            csvout.writerow([who.encode('utf-8'), what.encode('utf-8'), when, wha])
        f.close()








