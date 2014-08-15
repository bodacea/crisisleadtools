# -*- coding: utf_8 -*-
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.encoding import smart_unicode
from django.contrib.auth.decorators import login_required
from models import Group, Member


#FIXIT: To build: 
#Create master user list from skype, ning and googlegroups

class GroupCreateForm(forms.Form):
    invitemessage = forms.CharField()

class ContactForm(forms.Form):
    subject   = forms.CharField(max_length=100)
    message   = forms.CharField()
    sender    = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class ActionForm(forms.Form):
    ACTION_TYPES = (
        ('M', 'Message All'),
        ('L', 'Load All'),
        ('S', 'Search All'),
    )
    action    = forms.ChoiceField(choices=ACTION_TYPES, initial='L')


def write_tmp_file(uploadedfile):
        # open a new file to write the contents into
        new_file_name = 'media/' + uploadedfile.name 
 
        destination = open(new_file_name, 'wb+')
        destination.write(uploadedfile.file.read())
        destination.close()
 
        return str(new_file_name)


@login_required
def index(request):
    group_list = Group.objects.all().order_by('name')
    groupdata = {}
    groupdata['group_list'] = group_list
    return render_to_response('groups/index.html',
                              {'groupdata': groupdata},
                              context_instance=RequestContext(request))   

#Doesn't need login
def sandbox(request):
    return render_to_response('groups/sandbox.html',
                              {},
                              context_instance=RequestContext(request))                              

@login_required
def viewgroup(request):
    return render_to_response('groups/viewgroup.html',
                              {},
                              context_instance=RequestContext(request))                              

@login_required
def addgroup(request):
    return render_to_response('groups/addgroup.html',
                              {},
                              context_instance=RequestContext(request))                              

@login_required
def action(request):
    return render_to_response('groups/nothereyet.html',
                              {},
                              context_instance=RequestContext(request))                              

    
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print("Received message" + form.cleaned_data['message'])
            #Redirect to thank-you page
            return render_to_response('groups/nothereyet.html',
                              {},
                              context_instance=RequestContext(request))
    else:
        form = ContactForm() # An unbound form

    return render(request, 'groups/contact.html', {
        'form': form,
    })


def nothereyet(request):
    return HttpResponse("This function hasn't been included yet. Please check back later!")


