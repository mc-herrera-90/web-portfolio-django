from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='web_home'),
    path('portfolio/', views.portfolio, name='web_portfolio'),
    path('contact/', views.contact, name='web_contact')
]
