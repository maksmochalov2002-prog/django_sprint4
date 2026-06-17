from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import StaticPage


class HomeView(TemplateView):
    template_name = 'pages/index.html'


class StaticPageDetailView(TemplateView):
    template_name = 'pages/static_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        page = get_object_or_404(StaticPage, slug=slug, is_published=True)
        context['page'] = page
        return context


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)