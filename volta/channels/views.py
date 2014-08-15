#FIXIT: To build: 
#Upload Skypegroup user list
#Upload Ning profile list
#Upload Googlegroup profile list
#Upload Skypegroup chat: cut and paste
#Upload Skypegroup chat: downloaded from Skype
#Download Skypegroup chat from Skype
#Send Skype contact request to everyone on a list
#Create Skypechat
#Invite everyone on a list into a Skypechat

from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.encoding import smart_unicode
from django.contrib.auth.decorators import login_required
import csv
from skypechatmanager import *
from skypechatconnector import *
from models import Channel, Googlemember, Ningmember, Skypemember
from groups.models import Group


class SkypechatCreateForm(forms.Form):
    chatname      = forms.CharField(max_length=40)
    skypeidlist   = forms.CharField()
    skypeidsfile  = forms.FileField(required=False)
    invitemessage = forms.CharField()

class SkypechatFileForm(forms.Form):
    skypechatfile = forms.FileField(required=False) #OR
    skypechannel  = forms.CharField(required=False)

class NewChannelForm(forms.Form):
    channelname   = forms.CharField()
    channeltype   = forms.ChoiceField(choices=Channel.CHANNEL_TYPES, initial='S')
    membersfile   = forms.FileField(required=False) #
    remoteexists  = forms.BooleanField(required=False) #OR
    createremote  = forms.BooleanField(required=False) #Skype only for now
    remotename    = forms.CharField(required=False) #Name in remote channel
    
class FriendForm(forms.Form):
    idlist        = forms.CharField()
    message       = forms.CharField()
    idsfile       = forms.FileField(required=False) #

def write_tmp_file(uploadedfile):
        # open a new file to write the contents into
        new_file_name = 'media/' + uploadedfile.name 
 
        destination = open(new_file_name, 'wb+')
        destination.write(uploadedfile.file.read())
        destination.close()
 
        return str(new_file_name)


def get_list_from_uploaded_file(uploadedfile, column="0", header=False,
                          lowercase=False):
    #Read list in from file
    #Column numbering starts at 0, not 1
    csvin = csv.reader(uploadedfile.file)
    
    #Ignore header, if used
    if header == True:
        headers = csvin.next()
    
    #Get list from rest of file
    outlist = []
    for row in csvin:
        if len(row) <= column:
            continue
        item = row[column]
        outlist += [item]

    #FIXIT: yes, I know there's a pythonic way to do this, but I'm on a plane
    #and can't remember it at the moment
    if lowercase == True:
        templist = outlist
        outlist = []
        for item in templist:
            if type(item) == str or type(item) == unicode:
                item = item.lower()
            outlist += [item]
    
    return(outlist)


#Add members to a channel
def add_members_to_channel(memberslist, channel):

    if channel.network == "G":
        for memberid in memberslist:
            dbaseid = Googlemember.objects.create(
                channel = channel,
                userid_in_channel = memberid,
                stated_fullname = "unknown"
            )
        channel_members = Googlemember.objects.filter(channel = channel)

    elif channel.network == "N":
        for memberid in memberslist:
            dbaseid = Ningmember.objects.create(
                channel = channel,
                userid_in_channel = memberid,
                stated_fullname = "unknown"
            )
        channel_members = Ningmember.objects.filter(channel = channel)

    elif channel.network == "S":
        for memberid in memberslist:
            dbaseid = Skypemember.objects.create(
                channel = channel,
                userid_in_channel = memberid,
                stated_fullname = "unknown"
            )
        channel_members = Skypemember.objects.filter(channel = channel)
    
    return channel_members


@login_required
def index(request):
    return render_to_response('channels/index.html',
                              {},
                              context_instance=RequestContext(request))

#Doesn't need login
def sandbox(request):
    return render_to_response('channels/sandbox.html',
                              {},
                              context_instance=RequestContext(request))                              

@login_required
def viewchannel(request):
    return render_to_response('channels/viewchannel.html',
                              {},
                              context_instance=RequestContext(request))                              

@login_required
def addchannel(request):
    if request.method == 'POST':
        form = NewChannelForm(request.POST, request.FILES)
        if form.is_valid():
            channelname  = form.cleaned_data['channelname']
            channeltype  = form.cleaned_data['channeltype']
            remoteexists = form.cleaned_data['remoteexists']
            remotename   = form.cleaned_data['remotename']
            createremote = form.cleaned_data['createremote']
            if request.FILES.has_key('membersfile'):
                membersfile = request.FILES['membersfile']
                memberslist = get_list_from_uploaded_file(
                    membersfile, 0, True, False)
            else:
                memberslist = []

            #Add channel to the database, in group named "None".
            try:
                none_group = Group.objects.get(name="None")
            except Group.DoesNotExist:
                none_group = Group.objects.create(name="None", parent=None,
                                                  owner=request.user)
            
            channel = Channel.objects.create(
                owner = request.user,
                group = none_group,
                name = channelname,
                network = channeltype,
                remote_name = remotename)

            #Add members to the channel
            channel_members = add_members_to_channel(memberslist, channel)

            #Create remote channel if possible and requested
            #Fixit: add code for googlegroup and ning groups
            if createremote == True:
                print("creating remote channel")
                if channeltype == "S":
                    s = SkypechatConnector()
                    groupid, newbuddies = s.create_chatroom(remotename, memberslist,
                                                            "Welcome to "+remotename)
                    remoteexists = True
            
            data = {}
            data['channel'] = channel
            data['members'] = channel_members
            return render_to_response('channels/viewchannel.html',
                              {'data': data},
                              context_instance=RequestContext(request))
    else:
        form = NewChannelForm()
    return render_to_response('channels/addchannel.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def action(request):
    return render_to_response('channels/nothereyet.html',
                              {},
                              context_instance=RequestContext(request))                              

def nothereyet(request):
    return HttpResponse("This function hasn't been included yet. Please check back later!")


def friend_all(request):
    if request.method == 'POST':
        form = FriendForm(request.POST, request.FILES)
        if form.is_valid():
            formidlist = form.cleaned_data['idlist']
            idlist = formidlist.split(",")
            message = form.cleaned_data['message']
            if request.FILES.has_key('idsfile'):
                idsfile = request.FILES['idsfile']
                print("Not using uploaded file " + idsfile.name + "at the moment")
            s = SkypechatConnector()
            newbuddies, oldbuddies = s.make_buddies(idlist, message)
            results = {}
            results['message'] = message
            results['oldbuddies'] = oldbuddies
            results['newbuddies'] = newbuddies
            return render_to_response('channels/friendsummary.html',
                              {'results': results},
                              context_instance=RequestContext(request))
    else:
        form = FriendForm()
    return render_to_response('channels/friendrequests.html', {'form': form},
                              context_instance=RequestContext(request))


def create_skypechat(request):
    if request.method == 'POST':
        form = SkypechatCreateForm(request.POST, request.FILES)
        if form.is_valid():
            chatname = form.cleaned_data['chatname']
            formskypeidlist = form.cleaned_data['skypeidlist']
            skypeidlist = formskypeidlist.split(",")
            invitemessage = form.cleaned_data['invitemessage']
            if request.FILES.has_key('skypeidsfile'):
                skypeidsfile = request.FILES['skypeidsfile']
                print("Not using uploaded file " + skypeidsfile.name + "at the moment")
            s = SkypechatConnector()
            groupid, newbuddies = s.create_chatroom(chatname, skypeidlist, invitemessage)
            results = {}
            results['skypechatname'] = chatname
            results['members'] = skypeidlist
            results['newbuddies'] = newbuddies
            return render_to_response('channels/skyperoomsummary.html',
                              {'results': results},
                              context_instance=RequestContext(request))
    else:
        form = SkypechatCreateForm()
    return render_to_response('channels/skypechatcreate.html', {'form': form},
                              context_instance=RequestContext(request))


    
#Summarise a cut-and-pasted set of messages from a Skypechat
def summarise_skypechat(uploadedfile="", channelid=""):

    if channelid == "":
        skypemessages = read_skypemessages_cutpaste_stream(uploadedfile)
        skypeusers = {}
    ##    userstats = count_countributions(skypemessages)
        userstats, addgraph, texthist = analyse_skypechat(skypemessages, skypeusers)
        #Sort array by contributions, with largest numbers first
        revcnt = sorted(userstats.iteritems(), reverse=True, key=lambda x:x[1]['num_messages'])
        print(texthist)
    else:
        s = SkypechatConnector()
        print("Connecting to "+channelid)
        i = s.get_chatroom(channelid)
        userstats = s.get_messages(i)
        addgraph = {} #FIXIT: get these from the chatroom data
        texthist = {} #FIXIT: get these from the chatroom data
        revcnt = sorted(userstats.iteritems(), reverse=True, key=lambda x:x[1]['num_messages'])
    
    return revcnt, addgraph, texthist



def upload_skypechat(request):
    if request.method == 'POST':
        form = SkypechatFileForm(request.POST, request.FILES)
        if form.is_valid():
            results = {}
            if request.FILES == {}:
                #No file uploaded - assume have been given a skypechat name
                channel = form.cleaned_data['skypechannel']
                contribs, addgraph, texthist = summarise_skypechat("", channel)
                print(channel)
            else:
                uploadedfile = request.FILES['skypechatfile']
                ##print("Uploaded file " + uploadedfile.name)
                contribs, addgraph, texthist = summarise_skypechat(uploadedfile)
                results['filename'] = uploadedfile.name
            results['contribs'] = contribs
            results['addgraph'] = addgraph
            results['texthist'] = texthist
                
            return render_to_response('channels/skypechatsummary.html',
                              {'results': results},
                              context_instance=RequestContext(request))
    else:
        form = SkypechatFileForm()
        
    return render_to_response('channels/skypechatupload.html', {'form': form},
                              context_instance=RequestContext(request))


def summarise_skypeninggoogle(request):
    temp_filename = write_tmp_file(request.Files['skypeuserfile'],
                                   request.Files['ningexcelfile'],
                                   request.Files['googleuserfile'])
    members = compare_skypeninggoogle(temp_filename)
    return members


def upload_skypeninggoogle(request):
    if request.method == 'POST':
        form = SkypeNingGoogleFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Uploaded skype file " + uploadedskype.name)
            members = summarise_skypeninggoogle(request)
            results = {}
            results['request'] = request
            results['members'] = members
            return render_to_response('channels/skypeninggooglesummary.html',
                              {'results': results},
                              context_instance=RequestContext(request))
    else:
        form = SkypechatFileForm()
    return render_to_response('channels/skypeninggoogleup.html', {'form': form},
                              context_instance=RequestContext(request))

 
