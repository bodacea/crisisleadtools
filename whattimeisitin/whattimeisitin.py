# -*- coding: cp1252 -*-
import csv
import time
from datetime import datetime

#Convert CSV time entry into GMT time in python-readable format
def storetime(timein, gmtoffset):
  offset = int(gmtoffset*60*60) #Time offset in seconds
  t = time.mktime(time.strptime(timein, '%I:%M%p %m/%d/%y')) - offset
  return(t)

#Convert CSV time entry into GMT time in python-readable format
def unstoretime(timein, gmtoffset):
  offset = int(gmtoffset*60*60) #Time offset in seconds
  weekday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  t = time.strftime('%I:%M%p %w', time.localtime(timein + offset))
  t = t[:-1] + weekday[int(t[-1])]
  return(t)


#Set up 
fin  = open("SpaceAppsVenues.csv", "rb")
csvin  = csv.reader(fin)

#Read in venues
venuedetails = {}
timevenues = {}
headers = csvin.next()
for row in csvin:
  name = row[0]
  tz = float(row[1])
  #convert to python-readable time - note that need *local* not gmt to reverse this
  gmtstart = storetime(row[2], tz)
  gmtend   = storetime(row[4], tz)
  continent = row[5]
  venuedetails[name] = {'name':name, 'gmt':tz, 'gmtstart':gmtstart, 'gmtend':gmtend,
                          'continent':continent}
  timevenues.setdefault(tz, [])
  timevenues[tz] = timevenues[tz] + [name]

fin.close()

#sort venues by time
timelist = sorted(timevenues.iteritems(), key=lambda (x,y):float(x), reverse=True)  
colorder = []
for i in timelist:
  colorder += i[1] #list of venues at that timezone

#Get start and end times for whole hackathon
start = venuedetails[timelist[0][1][0]]['gmtstart']
for i in timelist[0][1]:
  vtime = venuedetails[i]['gmtstart']
  if start > vtime:
    start = vtime

end = venuedetails[timelist[-1][1][0]]['gmtend']
for i in timelist[-1][1]:
  vtime = venuedetails[i]['gmtend']
  if end < vtime:
    end = vtime

#Write to csv file
fout = open("SpaceAppsTimes.csv", "wb")
csvout = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC) #Quoting is important
csvout.writerow(colorder) #Venue names
timezones=[] #Yes, I can do this in Lambda notation, but later... when have time to debug
for venue in colorder:
  timezones += [str(venuedetails[venue]['gmt'])]
csvout.writerow(timezones) #time difference from GMT for each city

#rest of rows: time in each city, for all hours of the hackathon, per hour
for t in range(int(start), int(end+3600), 3600):
  row = []
  for venue in colorder:
    if t >= venuedetails[venue]['gmtstart'] and t <= venuedetails[venue]['gmtend']:
      row += [unstoretime(t, venuedetails[venue]['gmt'])]
    else:
      row += [""]
  csvout.writerow(row)

fout.close()
