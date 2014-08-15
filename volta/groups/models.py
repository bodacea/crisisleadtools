from django.db import models
from django.contrib.auth.models import User
##from cms.models import CMSPlugin

##Class MemberPlugin(CMSPlugin):
##    userprofile = models.ForeignKey('Members.Userprofile', related_name='plugins')
##    def __unicode__(self):
##        return self.userprofile.real_name


# Group profile
class Group(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', blank=True, null=True) #Allow null
    owner = models.ForeignKey(User) #When user leaves, need to change this
    

# User data that group uses for contacts and assigning to tasks
class Member(models.Model):
    STATUS_CHOICES = (
        ('A','Admin'),
        ('M', 'Member'),
        ('O', 'Observer'),
    )
    
    real_name      = models.CharField(max_length=30)
    skype_id       = models.CharField(max_length=30)
    ning_id        = models.CharField(max_length=30)
    twitter_id     = models.CharField(max_length=30)
    email          = models.EmailField()
    status         = models.CharField(max_length=30)
    location       = models.CharField(max_length=30)
    country        = models.CharField(max_length=30)
    timezone       = models.CharField(max_length=30)
    membersince    = models.DateField('member since')
    languagelist   = models.TextField()
    verifiedByCore = models.BooleanField()
    verifiedByUser = models.BooleanField()
    group          = models.ForeignKey(Group)
    


