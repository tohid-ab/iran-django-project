from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_page, name='Home'),
    path('contact-us/', views.trick_page, name='Tricks'),
    path('post/like/', views.like, name='like-post'),
    path('articles/', views.article_page, name='Article'),
    path('articles/category/<str:slug>', views.category_filter, name='slug'),
    path('articles/<slug:slug>', views.detail_article, name='detail-article'),
    path('articles/serach/', views.SearchBox.as_view(), name='search'),
    path('free-project/', views.free_project, name='free-project'),
    path('about-me/', views.about_me, name='about-me'),
]