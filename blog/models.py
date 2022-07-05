from django.db import models
from django.urls import reverse
from jalali_date import date2jalali, datetime2jalali
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import uuid


# Create your models here.


class CategoryClass(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام دسته بندی', name='name')
    slug = models.SlugField(max_length=255, verbose_name='لینک دسته بندی', name='slug')

    def get_absolute_url(self):
        return reverse('blog:slug', args=[str(self.slug)])

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name


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
    read_time = models.IntegerField(default=1, blank=False, verbose_name='زمان مطالعه')
    visite = models.IntegerField(verbose_name="تعداد بازدید", blank=False, null=False, default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت', name='created')
    updated = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت', name='update')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail-article", args=[str(self.slug)])

    def get_jalali_date(self):
        return datetime2jalali(self.created)


class IpUserToView(models.Model):
    userName = models.CharField(max_length=225, default="None", null=True, blank=True, verbose_name="نام کاربر")
    userIp = models.CharField(max_length=15, default="000,000,000,000", null=False, blank=False, verbose_name="IP کاربر")
    date_visite = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(ArticleClass, on_delete=models.CASCADE, verbose_name="آیتم؟")

    def __str__(self):
        return f"{self.userName} | {self.userIp} | {self.date_visite} | {self.item}"

    class Meta:
        verbose_name = "آدرس IP کاربر"
        verbose_name_plural = "آدرس های IP کاربران صفحه مقالات"

    def get_jalali_date(self):
        return datetime2jalali(self.date_visite)


class Comment(models.Model):
    post = models.ForeignKey(ArticleClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(default=None)
    comment = models.TextField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        ordering = ['created_on']
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.comment[:60]} --> {self.post.title[:20]} | {self.status}'


class ReplyComment(models.Model):
    r_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.r_comment} -> {self.text[:30]}'

    class Meta:
        verbose_name = 'پاسخ کامنت'
        verbose_name_plural = 'پاسخ کامنت ها'


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post_id = models.ForeignKey(ArticleClass, on_delete=models.CASCADE, related_name='likes')
    liked_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.username} --> {self.post_id.id} | post_user: {self.post_id.user}'

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'


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
        verbose_name = 'سوال'
        verbose_name_plural = 'سوال های پرتکرار'

    def __str__(self):
        return f'ID:{self.id} title: {self.title}'


class DjangoRoadMap(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True, name='text')

    def __str__(self):
        return self.name


class DjangoTricksDaily(models.Model):
    test = models.CharField(max_length=50, unique=True)
    random_url = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.test


class ContactUs(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(default=None, blank=False)
    title = models.CharField(max_length=150, blank=False)
    comment = models.TextField(max_length=800, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        ordering = ['created_on']
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما'

    def __str__(self):
        return self.title


class ProjectSourceClass(models.Model):
    STATUS_CHOICES = (
        ('Activate', 'فعال'),
        ('Deactivate', 'غیر فعال'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, verbose_name='user')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Deactivate', verbose_name='وضعیت')
    title = models.CharField(max_length=255, verbose_name='عنوان پروژه', name='title', null=True)
    slug = models.SlugField(max_length=255, verbose_name='لینک', name='slug', null=True)
    description = models.TextField(verbose_name='متن پروژه', name='description', null=True)
    image = models.ImageField(upload_to='article/%Y/%m/%d', blank=True, verbose_name='عکس', name='image', null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت', name='created')
    updated = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت', name='update')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail-project", args=[str(self.slug)])

    def get_jalali_date(self):
        return datetime2jalali(self.created)