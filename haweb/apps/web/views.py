from django.shortcuts import render
from .models import Menu


def gen_menu(parents, sub_menu=False):
    result = ""
    for parent in parents:
        if parent.how_many_children == 0:
            result += '<li class="menu-item "><a href="{}">{}</a></li>\n'.format(parent.link, parent.name)
        else:
            if sub_menu:
                result += '<li class="menu-item dropdown dropdown-submenu">\n'
                result += '<a href="#" class="dropdown-toggle" data-toggle="dropdown">{}</a>\n'.format(parent.name)
            else:
                result += '<li class="menu-item dropdown">\n'
                href = '<a href="#" class="dropdown-toggle" data-toggle="dropdown">{}<b class="caret"></b></a>\n'
                result += href.format(parent.name)
            result += '<ul class="dropdown-menu">\n'
            result += gen_menu(parent.children_orderby_index, True)
            result += '\n</ul>'
            result += '\n</li>'

    return result


def home(request):
    menu_parents = Menu.objects.filter(parent__isnull=True).order_by('index')
    menu = gen_menu(menu_parents)
    return render(request, 'home.html', {'menu_parents': menu_parents, 'menu': menu})
