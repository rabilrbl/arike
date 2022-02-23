from django.template import Library

register = Library()

@register.inclusion_tag('System/template_tags/head_search.html')
def head_search(heading, btn_link):
    return {'heading': heading, 'btn_link': btn_link}