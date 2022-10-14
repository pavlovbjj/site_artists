from django import template
from artists.models import *

register = template.Library()

# menu = [{'title': 'О сайте', 'url_name': 'about'},
#         {'title': 'Добавить статью', 'url_name': 'addpage'},
#         {'title': 'Обратная связь', 'url_name': 'contact'}]
#
#
# @register.inclusion_tag('artists/template_html/list_menu.html')
# def get_menu():
#     return {"menu": menu,}

@register.inclusion_tag('artists/template_html/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}

