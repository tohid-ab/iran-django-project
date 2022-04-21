from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_page, name='Home'),
    path('django-bog/', views.trick_page, name='Tricks'),
    path('post/like/', views.like, name='like-post'),
    path('articles/', views.article_page, name='Article'),
    path('articles/<slug:slug>', views.detail_article, name='detail-article'),
    path('articles/serach/', views.SearchBox.as_view(), name='search'),
    path('free-project/', views.free_project, name='free-project')
]