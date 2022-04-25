from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import ArticleClass, DjangoTricks, AskedQuestions, DjangoRoadMap, CategoryClass, Like
from django.db.models import Q
from django.contrib.auth.models import User
# like system
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# import pagination
from django.core.paginator import Paginator
# search page
from django.views.generic import ListView
# Create your views here.


@login_required
def like(request):
    post_id = request.POST['post_id']
    post = ArticleClass.objects.get(pk=post_id)
    liked = True

    like_object, created = Like.objects.get_or_create(user_id=request.user, post_id=post)
    if not created:
        like_object.delete()  # the user already liked this picture before
        liked = False

    return JsonResponse({'liked': liked})


def home_page(request):
    if request.user.is_authenticated:
        article = ArticleClass.objects.filter(status='Activate')[0:3]
        article_block = ArticleClass.objects.filter(status='Activate')[0:2]
        video_tricks = DjangoTricks.objects.all()[0:2]
        questions = AskedQuestions.objects.all()
        road_map = DjangoRoadMap.objects.all()
        # سیستم لایک
        liked_posts = []
        for liked_post in request.user.likes.all():
            liked_posts.append(liked_post.post_id)
        context = {
            'article': article,
            'article_block': article_block,
            'video': video_tricks,
            'question': questions,
            'map': road_map,
            'liked_posts': liked_posts,
        }
        return render(request, 'index.html', context)
    else:
        article = ArticleClass.objects.filter(status='Activate')[0:3]
        article_block = ArticleClass.objects.filter(status='Activate')[0:2]
        video_tricks = DjangoTricks.objects.all()[0:2]
        questions = AskedQuestions.objects.all()
        road_map = DjangoRoadMap.objects.all()
        context = {
            'article': article,
            'article_block': article_block,
            'video': video_tricks,
            'question': questions,
            'map': road_map,
        }
        return render(request, 'index.html', context)


def trick_page(request):
    return render(request, 'tricks/django-tricks.html')


def article_page(request):

    if request.user.is_authenticated:
        article = ArticleClass.objects.filter(status='Activate')
        # pagination or صفحه بندی
        paginator = Paginator(article, 6)
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)
        # دسته بندی
        category_d = CategoryClass.objects.all()
        # سیستم لایک
        liked_posts = []
        for liked_post in request.user.likes.all():
            liked_posts.append(liked_post.post_id)
        context = {
            'category': category_d,
            'pagination_article': articles,
            'liked_posts': liked_posts,
        }
        return render(request, 'articles/article.html', context)

    else:
        article = ArticleClass.objects.filter(status='Activate')
        # pagination or صفحه بندی
        paginator = Paginator(article, 6)
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)
        # دسته بندی
        category_d = CategoryClass.objects.all()

        context = {
            'category': category_d,
            'pagination_article': articles,
        }

        return render(request, 'articles/article.html', context)


def detail_article(request, slug):
    data = ArticleClass.objects.get(slug=slug)
    category = CategoryClass.objects.all()
    suggested_article = ArticleClass.objects.filter(status='Activate')[0:4]

    context = {
        'data': data,
        'category': category,
        'suggested_article': suggested_article,
    }
    return render(request, 'articles/detail-article.html', context)


def free_project(request):
    return render(request, 'projects/free-project.html')


class SearchBox(ListView):
    model = ArticleClass
    template_name = 'articles/search.html'
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = ArticleClass.objects.filter(status='Activate')
        context['category'] = CategoryClass.objects.all()
        return context

    def get_queryset(self):
        query = self.request.GET.get('Q')
        object_list = self.model.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return object_list


def category_filter(request, slug):
    if request.user.is_authenticated:
        article = ArticleClass.objects.filter(category__slug=slug, status='Activate')
        # pagination or صفحه بندی
        paginator = Paginator(article, 6)
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)
        # دسته بندی
        category_d = CategoryClass.objects.filter(slug=slug)
        # سیستم لایک
        liked_posts = []
        for liked_post in request.user.likes.all():
            liked_posts.append(liked_post.post_id)
        context = {
            'category': category_d,
            'pagination_article': articles,
            'liked_posts': liked_posts,
        }
        return render(request, 'articles/article-category.html', context)

    else:
        article = ArticleClass.objects.filter(category__slug=slug, status='Activate')
        # pagination or صفحه بندی
        paginator = Paginator(article, 6)
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)
        # دسته بندی
        category_d = CategoryClass.objects.filter(slug=slug)

        context = {
            'category': category_d,
            'pagination_article': articles,
        }

        return render(request, 'articles/article.html', context)













