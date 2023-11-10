from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("news/", views.news, name="news"),
    path("news-details/<int:pk>/", views.news_details, name="news_details"),
    path('contacts/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name="about"),
    path('piu/', views.piu_staff, name='piu'),
    ]
