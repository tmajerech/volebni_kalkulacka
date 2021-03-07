from django import template
from django.templatetags import static
from config.settings.base import *
from volebni_kalkulacka.psp_data.helpers import get_current_election_period

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

@register.simple_tag
def poslanec_party(id_osoba, organ_set):

    organ = organ_set.filter(zarazeni__id_osoba=id_osoba).first()


    return organ.zkratka
