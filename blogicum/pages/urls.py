from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.StaticPageDetailView.as_view(), name='about'),
    path('rules/', views.StaticPageDetailView.as_view(), name='rules'),
    path('registration/', views.SignUpView.as_view(), name='registration'),
    path('<slug:slug>/', views.StaticPageDetailView.as_view(),
         name='static_page'),
]
