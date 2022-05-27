from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from . models import *
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import CommentForm, ContactForm
from django.contrib import messages
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
    data = get_object_or_404(ArticleClass, slug=slug)
    # سیستم کامنت
    comment = Comment.objects.filter(post=data, status=True).order_by('-created_on')
    new_comment = None
    category = CategoryClass.objects.all()
    suggested_article = ArticleClass.objects.filter(status='Activate')[0:4]
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            name = comment_form.cleaned_data.get('name')
            email = comment_form.cleaned_data.get('email')
            comment_s = comment_form.cleaned_data.get('comment')
            new_comment.name = name
            new_comment.email = email
            new_comment.comment = comment_s
            # Assign the current post to the comment
            new_comment.post = data
            # Save the comment to the database
            new_comment.save()
            messages.success(request, 'خیلی ممنون ، نظر شما پس از برسی نمایش داده خواهد شد')
            return redirect(f'/articles/{slug}')
    else:
        comment_form = CommentForm()

    context = {
        'data': data,
        'comment': comment,
        'category': category,
        'suggested_article': suggested_article,
        'new_comment': new_comment,
        'comment_form': comment_form,
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


def about_me(request):
    return render(request, 'about-me.html')


def trick_page(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            new_comment = contact_form.save(commit=False)
            name = contact_form.cleaned_data.get('name')
            email = contact_form.cleaned_data.get('email')
            comment_s = contact_form.cleaned_data.get('comment')
            new_comment.name = name
            new_comment.email = email
            new_comment.comment = comment_s
            # Save the comment to the database
            new_comment.save()
            messages.success(request, 'خیلی ممنون ، به زودی با شما تماس خواهیم گرفت')
            return redirect('/contact-us/')
    else:
        contact_form = ContactForm()

    context = {
        'contact_form': contact_form,
    }

    return render(request, 'tricks/django-tricks.html', context)












