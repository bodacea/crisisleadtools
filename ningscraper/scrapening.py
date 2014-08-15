'''
Scrape Ning site for groups and users

Sara-Jayne Farmer
2013
'''

import urllib
import xlwt
from BeautifulSoup import BeautifulSoup
import re
import time

#User-set variables
siteurl = "standbytaskforce.ning.com"

#Global variables
opener = urllib.FancyURLopener() #in
wbk = xlwt.Workbook() #out

#Fetch a page from the ningsite
def getpage(siteroot, pagedir):
  rawpage = opener.open(siteroot + pagedir).read()
  return(BeautifulSoup(rawpage))


#Get user details from their homepage
def getUser(siteroot, userUrl, userName):
  print(userUrl)
  userPage = getpage(siteroot, '/profile/'+ userUrl+'?xg_source=profiles_memberList')
  user = {}
  #Add id and name to user details
  user['id'] = userUrl
  user['name'] = userName
  #Get email, skypeid, skills, languages, location
  deettext = userPage.find("div", {"class":"xg_module module_about_user"})
  if deettext == None: #Deal with your own page being different
    deettext = userPage.find("div", {"class":"xg_module movable sortable  module_about_user"})
  dls = deettext.findAll('dl')
  for dl in dls:
    user[dl.find('dt').text] = dl.find('dd').text  
  return(user)


'''
Get object count from a Ningpage
'''
def getcount(soup):
  
  #Get number of objects
  rawcount = soup.find('span', {'class':'count'}).text
  count = int("".join(re.findall("\w",rawcount)))  #Strip non-numbers from string then convert to int
  
  #get number of pages
  pagesect = soup.find('ul', {'class':"pagination easyclear "})
  if pagesect == None: #pagination list only exists for more than one page of results
    numpages = 1
  else:
    pageline = pagesect.find("span", {"style":"display:none"})
    numpages = int(pageline.get("_maxpage"))
  
  return(count, numpages)


def mineuserdata(mem):
  memname = mem.find('h5').text.title()
  memurl = mem.find('a')['href']
  memid = re.findall('profile/(.+?)\?xg_source', memurl)[0]
##  print("User: "+memname.encode('utf-8') +" ("+memid.encode('utf-8')+")");
  return(memid, memname)


'''
Get list of user attached to a group, event or ningsite
Sara-Jayne Farmer
2013
'''
def getUserList(siteroot, listroot):
  
  #Get number of pages in user list
  soup = getpage(siteroot, listroot+'?page=1')
  numusers, numpages = getcount(soup)
  
  #Get user names and Ning ids  
  userlist = {}
  for pagenum in range(1,numpages+1):
    soup = getpage(siteroot, listroot+'?page='+str(pagenum))
    mems = soup.findAll('div', {"class":"member_item "})  #All member links on page
    for mem in mems:
      memid, memname = mineuserdata(mem)
      userlist[memid] = memname

    #Get last user - this is usually the group owner
    mem = soup.find('div', {"class":"member_item last-child"})  #Last member link
    memid, memname = mineuserdata(mem)
    userlist[memid] = memname
    
  return(userlist)

'''
Get members list from ningsite

Sara-Jayne Farmer
2013
'''
def getAllUsers(siteroot):
  
  #Get each user's details from their homepage
  users = getUserList(siteroot, '/profiles/friend/list')
  for memid in users:
    users[memid] = getUser(siteroot, memid, users[memid])
  
  return(users)


'''
Get group details from its homepage

Sara-Jayne Farmer
2013
'''
def getGroup(siteroot, groupUrl):
  groupPage = getpage(siteroot, '/group/'+ groupUrl)
  group = {}
  #Get name
  group['name'] = groupPage.find("title").text
  #Get information
  groupinfo = groupPage.find("div", {"class":"pad5 group_details"}).text
  groupinfo = groupinfo.replace("Members:", ". Members:")
  groupinfo = groupinfo.replace("Latest Activity:", ". Latest Activity:")
  group['info'] = groupinfo
  
  #Get team list
  group['users'] = getUserList(siteroot, '/group/'+groupUrl+'/user/list')
  
  return(group)


'''
Get group lists from ningsite

Sara-Jayne Farmer
2013
'''
def getAllGroups(siteroot):
  soup = getpage(siteroot, '/groups')
  
  #get number of groups
  numgroups, numpages = getcount(soup)
  
  #Get all groups' details
  groups = {}
  for pagenum in range(1,numpages+1):
    soup = getpage(siteroot, '/groups?page='+str(pagenum))
    grouplist = soup.find('div', {'class':'xg_list xg_list_groups xg_list_groups_main'})
    gps = grouplist.findAll('h3')  #All group links on page
    for gp in gps:
      gpname = gp.text
      gplongurl = gp.find('a')['href']
      gpurl = re.findall('group/(.+?)$', gplongurl)[0]
      print("Group: "+gpname.encode('utf-8') +" ("+gpurl.encode('utf-8')+")");
      groups[gpname] = getGroup(siteroot, gpurl)
  return(groups)


#Map dictionary keys to excel spreadsheet columns, and output as header row in spreadsheet
def writeHeader(dictionary, excelsheet):
  col=0
  keycols = {}
  for key in dictionary[dictionary.keys()[0]].keys():
    keycols[key] = col
    excelsheet.write(0, col, key)
    col += 1

  return(keycols)


#Write user data to excel file
def writeUsersToExcel(users):
  memsheet = wbk.add_sheet("MemberSummary", cell_overwrite_ok=True)
  
  #write header row in excel file
  keycols = writeHeader(users, memsheet)
  
  #Add each user to the datasheet
  mrow = 1
  for user in users:
    for key in keycols:
      memsheet.write(mrow, keycols[key], users[user][key])
    mrow += 1
  
  return


#Write group data to excel file
def writeGroupsToExcel(groups):

  #Write groups summary sheet to workbook
  sumsheet = wbk.add_sheet('GroupSummary', cell_overwrite_ok=True) 
  keycols = writeHeader(groups, sumsheet)
  usercol = keycols.pop('users') #Don't try to write the users lists into the summary page
  grow = 1
  for gpname in groups:
    for key in keycols:
      sumsheet.write(grow, keycols[key], groups[gpname][key])
    sumsheet.write(grow, usercol, len(groups[gpname]['users']))
    grow += 1
  
  #Write group details to worksheet
  for gpname in groups:
    sheetname = re.sub('[\[\]\*/\\\?:]', '', gpname) #Remove invalid excel characters
    sheetname = sheetname[:min(31,len(gpname))] #Excel limits name to 31 chars
    groupsheet = wbk.add_sheet(sheetname, cell_overwrite_ok=True)

    #Write user list into worksheet
    groupsheet.write(0,0, "NingId")
    groupsheet.write(0,1, "Name")
    mrow = 1
    for user in groups[gpname]['users']:
      groupsheet.write(mrow,0, user)
      groupsheet.write(mrow,1, groups[gpname]['users'][user])
      mrow += 1
  return


def findfriends(siteroot, userid):
  listroot = "/profiles/friend/list?user="+userid
  #Also worth looking at /profiles/friendrequest/listSent
  #and /profiles/friendrequest/listReceived
  friends = getUserList(siteroot, listroot)
  return(friends)


def makefriend(siteroot, userid, message):
  siteroot + "/profiles/friendrequest/create?xn_out=json&screenName="+userid

  #It's a form!
  #use http://epydoc.sourceforge.net/stdlib/urllib.URLopener-class.html#open
  #with data set like we do with the requests library
  #Form is:
  #<input type="hidden" name="xg_token" value="687cd84f9e567454bccbec902d6da650">
  #<textarea class="add-friend-message" name="message" cols="20" rows="3"></textarea>
  #<input type="submit" class="button action-primary" value="Send">
  #No url given - is it the same as the profile?
  #is it: http://standbytaskforce.ning.com/profiles/friendrequest/create?xn_out=json&screenName=0awgo3fdok1ij
  data = urllib.urlencode({"message":message,
                           "xg_token":"687cd84f9e567454bccbec902d6da650"})
  response = opener.open(siteroot + "/profiles/friendrequest/create?xn_out=json&screenName="+userid,
                         data)
  
  return()


def sendmessage(siteroot, userid, message):
  sendurl = siteroot + "/profiles/message/newFromProfile?screenName="+userid
  return


#MAIN CODE
def main():
  
  #Get username and password from file, then set Ningsite root url with them
  fpass = open("ningpass.txt", "rb")
  uname = fpass.readline().strip() #strips return characters from end of line
  upass = fpass.readline().strip()
  fpass.close()
  siteroot = 'http://' + uname+':'+ upass+ '@' + siteurl
  
  #Test that site url works
  print("If your username, password and sitename are all valid, you'll have a copy " \
        "of the site's front page in file testningoutput.html")
  fout = open("testningoutput.html", "wb")
  fout.write(getpage(siteroot, '').prettify())
  fout.close()
  
  #Open and write header to Excel
  frontsheet = wbk.add_sheet("Summary", cell_overwrite_ok=True)
  frontsheet.write(0,0, "Ning database summary")
  frontsheet.write(1,0, "Created " + time.asctime(time.gmtime()) + " GMT")
  frontsheet.write(2,0, "From url :" + siteurl)
  
  #Get Ning member data and output it to Excel file
  users = getAllUsers(siteroot)
  writeUsersToExcel(users)
  
  #Get Ning group data and output it to Excel file
  groups = getAllGroups(siteroot)
  writeGroupsToExcel(groups)
  
  #Do we need to do events too?
  
  #Write then close excel file and go home happy
  wbk.save(siteurl+"_groups.xls")
  return()

#Run code
main()

                       
