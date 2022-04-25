from django.db import models
from django.urls import reverse
from jalali_date import date2jalali, datetime2jalali
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your models here.


class CategoryClass(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام دسته بندی', name='name')
    slug = models.SlugField(max_length=255, verbose_name='لینک دسته بندی', name='slug')

    def get_absolute_url(self):
        return reverse('blog:slug', args=[str(self.slug)])

    def __str__(self):
        return self.name


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(null=True, verbose_name='آیپی کاربر')


class ArticleClass(models.Model):
    STATUS_CHOICES = (
        ('Activate', 'فعال'),
        ('Deactivate', 'غیر فعال'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, verbose_name='user')
    category = models.ManyToManyField(CategoryClass, verbose_name='دسته بندی')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Deactivate', verbose_name='وضعیت')
    title = models.CharField(max_length=255, verbose_name='عنوان مقاله', name='title', null=True)
    slug = models.SlugField(max_length=255, verbose_name='لینک', name='slug', null=True)
    description = models.TextField(verbose_name='متن مقاله', name='description', null=True)
    image = models.ImageField(upload_to='article/%Y/%m/%d', blank=True, verbose_name='عکس', name='image', null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت', name='created')
    updated = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت', name='update')
    visits = models.ManyToManyField(IpAddress, blank=True, related_name='visits', verbose_name='تعداد بازدید مقاله')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail-article", args=[str(self.slug)])

    def get_jalali_date(self):
        return datetime2jalali(self.created)


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post_id = models.ForeignKey(ArticleClass, on_delete=models.CASCADE, related_name='likes')
    liked_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.username} --> {self.post_id.id} | post_user: {self.post_id.user}'


class DjangoTricks(models.Model):
    name_video = models.CharField(max_length=255, name='name_video', verbose_name='نام ویدیو')
    id_video = models.CharField(max_length=255, null=False, blank=False, name='id_video', verbose_name='آیدی ویدیو')
    src = models.TextField(name='src', verbose_name='آدرس ویدیو')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت', name='created')
    updated = models.DateField(auto_now=True, verbose_name='آخرین آپدیت', name='update')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.name_video


class AskedQuestions(models.Model):
    title = models.CharField(max_length=255, name='title', verbose_name='سوال')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت', name='created')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'ID:{self.id} title: {self.title}'


class DjangoRoadMap(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True, name='text')

    def __str__(self):
        return self.name