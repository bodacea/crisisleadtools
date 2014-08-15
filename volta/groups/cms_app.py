from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MembersApp(CMSApp):
    name = _("Members App") # give your app a name, this is required
    urls = ["members.urls"] # link your app to url configuration(s)

apphook_pool.register(MembersApp) # register your app
