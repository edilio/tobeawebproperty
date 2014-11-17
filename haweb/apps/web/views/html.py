from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

from ..models import Menu, Organization, Content, FAQ, HelpfulLink, Career, ResourceForm, ResourceCategory


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


def gen_breadcrumb(path):
    lst = path.split('/')
    result = ['<li><a href="/">Home</a> <span class="divider"></span></li>']
    link = ''
    for m in lst[1:-1]:
        link += '/' + m
        result.append('<li><a href="{}">{}</a> <span class="divider"></span></li>'.format(link, m))
    if len(lst) > 1:
        result.append('<li class="active">{}</li>'.format(lst[-1]))

    return "".join(result)


def gen_common_context(path):
    return {
        'now': timezone.now(),
        'menu': gen_menu(),
        'organization': Organization.objects.all()[0],
        'breadcrumb': gen_breadcrumb(path)
    }


def common_render(request, template):
    return render(request, template, gen_common_context(request.path_info))


def home(request):
    return common_render(request, 'home.html')


def about_us(request):
    return common_render(request, 'about_us.html')


def contact_us(request):
    return common_render(request, 'contact_us.html')


class HAWebListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(HAWebListView, self).get_context_data(**kwargs)
        context.update(gen_common_context(self.request.path_info))

        return context


class ContentListView(HAWebListView):
    model = Content
    template_name = 'pages_list.html'


class ContentDetail(DetailView):
    model = Content
    template_name = 'base.html'
    http_method_names = ['get']
    context_object_name = 'content_obj'

    def get_context_data(self, **kwargs):
        context = super(ContentDetail, self).get_context_data(**kwargs)
        context.update(gen_common_context(self.request.path_info))
        return context


class FAQListView(HAWebListView):
    model = FAQ
    template_name = 'faqs.html'


class HelpfulLinkListView(HAWebListView):
    model = HelpfulLink
    template_name = 'helpful_links.html'


class CareerListView(HAWebListView):
    model = Career
    template_name = 'careers.html'


class ResourceListView(HAWebListView):
    model = ResourceForm
    template_name = 'resources.html'

    def get_context_data(self, **kwargs):
        context = super(ResourceListView, self).get_context_data(**kwargs)
        context.update({'categories': ResourceCategory.objects.all()})
        return context