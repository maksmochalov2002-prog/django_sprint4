from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:slug>/', views.StaticPageDetailView.as_view(), name='static_page'),
]