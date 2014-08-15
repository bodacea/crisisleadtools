from django.db import models
from django.contrib.auth.models import User
from groups.models import Group

#Channel details
class Channel(models.Model):
    CHANNEL_TYPES = (
        ('S', 'Skype Chat'),
        ('N', 'Ning Group'),
        ('G', 'Google Group'),
    )
    owner                = models.ForeignKey(User) #When user leaves, need to change this
    group                = models.ForeignKey(Group, blank=True, null=True) #optional 
    network              = models.CharField(max_length=1, choices=CHANNEL_TYPES)
    name                 = models.CharField(max_length=40)
    remote_exists        = models.BooleanField()
    remote_name          = models.CharField(max_length=100)
    remote_api           = models.CharField(max_length=300)
    last_members_apiload = models.DateTimeField("Last members upload from API", blank=True, null=True)
    last_members_upload  = models.DateTimeField("Last members upload from file", blank=True, null=True)
    last_members_file    = models.CharField(max_length=300)


class Member(models.Model):
    channel           = models.ForeignKey(Channel)
    stated_fullname   = models.CharField(max_length=40)
    friended_by_owner = models.BooleanField()

    class Meta:
        abstract = True


# Googlegroup inputs
class Googlemember(Member):
    #Channel-specific info
    userid_in_channel = models.EmailField()
    group_status      = models.CharField(max_length=20)
    email_preference  = models.CharField(max_length=20)
    join_date         = models.DateTimeField("joining date")
    email_status      = models.CharField(max_length=20)

    #Location information
    stated_timezone   = models.CharField(max_length=30)

    
# Ning inputs
class Ningmember(Member):
    #Channel-specific info
    userid_in_channel    = models.CharField(max_length=30)
    ningaddress          = models.URLField()
    date_joined          = models.DateField()
    receiving_broadcasts = models.BooleanField()
    receiving_emails     = models.BooleanField()
    last_visit           = models.DateField()

    #Basic personal identifiers
    email                = models.CharField(max_length=300)
    stated_email         = models.CharField(max_length=300)
    stated_skypeid       = models.CharField(max_length=30)
    stated_twitterid     = models.CharField(max_length=30)

    #Skills and longform information
    stated_organisation  = models.CharField(max_length=30)
    stated_website       = models.CharField(max_length=300)
    stated_bio           = models.TextField()
    stated_ushahidi_experience = models.TextField()
    stated_ushahidi_tasks      = models.TextField()
    stated_skills        = models.TextField()
    stated_languages     = models.TextField()

    #Location information
    stated_location      = models.CharField(max_length=300)
    stated_country       = models.CharField(max_length=30)
    stated_zipcode       = models.CharField(max_length=30)
    stated_location_and_timezone = models.TextField()


# Skype inputs
class Skypemember(Member):
    #Channel-specific info
    userid_in_channel = models.CharField(max_length=30)
    numberofbuddies   = models.IntegerField()
    lastonline        = models.DateTimeField("last online")

    #Skills and longform information
    about             = models.TextField()
    stated_homepage   = models.CharField(max_length=300)
    language          = models.CharField(max_length=90)

    #Location information
    stated_country    = models.CharField(max_length=60)
    stated_province   = models.CharField(max_length=30)
    stated_city       = models.CharField(max_length=30)
    stated_timezone   = models.CharField(max_length=30)
 

