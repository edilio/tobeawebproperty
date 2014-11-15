from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

from ..models import Menu, Organization, Content


def gen_menu(parents=None, sub_menu=False):
    if not parents:
        parents = Menu.objects.filter(parent__isnull=True).order_by('index')

    result = ""
    for parent in parents:
        if parent.how_many_children == 0:
            if parent.is_divider:
                result += '<li class="divider"></li>'
            else:
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
    menu = gen_menu()
    organization = Organization.objects.all()[0]
    context = {'menu': menu, 'organization': organization}
    return render(request, 'home.html', context)


class ContentListView(ListView):

    model = Content
    template_name = 'pages_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContentListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['menu'] = gen_menu()
        context['organization'] = Organization.objects.all()[0]
        return context


class ContentDetail(DetailView):
    model = Content
    template_name = 'base.html'
    http_method_names = ['get']
    context_object_name = 'content_obj'

    def get_context_data(self, **kwargs):
        context = super(ContentDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['menu'] = gen_menu()
        context['organization'] = Organization.objects.all()[0]
        return context
