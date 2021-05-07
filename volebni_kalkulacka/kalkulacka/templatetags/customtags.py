from django import template
from django.templatetags import static
from config.settings.base import *

register = template.Library()


class FullStaticNode(static.StaticNode):
    def url(self, context):

        if ('request' in context):
            request = context['request']
            return request.build_absolute_uri(super().url(context))
        elif ('activate_url' in context):
            #CONFIRMATION EMAIL BUG WORKAROUND (missing context when called from django-allauth, will be fixed in django-allauth 0.43.0 or higher)
            request = None
            return context['activate_url'].split('auth')[0] + "static/" + self.path.var
        elif ('custom_path' in context):
            return os.path.join(context['custom_path'], 'static', self.path.var)


@register.tag('fullstatic')
def do_static(parser, token):
    return FullStaticNode.handle_token(parser, token)


@register.tag(name='support_href')
def support_href():
    return "mailto:info@todo.cz?subject=?Dotaz_na_podporu"

@register.filter(name='partycolor')
def partycolor(party):
    colors = {
        'ANO':'#111e6c', 
        'ODS':'#034ea2',
        'Piráti':'#000000',
        'SPD':'#1074bc',
        'ČSSD':'#ec5800',
        'KSČM':'#bf0202',
        'KDU-ČSL':'#d8b600',
        'TOP 09':'#993366',
        'TOP09-S':'#993366',
        'STAN':'#7ec192',
    }
    return colors.get(party)

