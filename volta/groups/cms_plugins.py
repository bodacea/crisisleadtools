from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from members.models import MemberPlugin as MemberPluginModel
from django.utils.translation import ugettext as _

class MemberPlugin(CMSPluginBase):
    model = MemberPluginModel # Model where data about this plugin is saved
    name = _("Member Plugin") # Name of the plugin
    render_template = "members/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(MemberPlugin) # register the plugin
