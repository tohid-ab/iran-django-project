from django.contrib import admin
from .models import ArticleClass, DjangoTricks, AskedQuestions, CategoryClass, DjangoRoadMap, IpAddress, Like
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(CategoryClass)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ArticleClass)
class ImageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'get_jalali_date', 'status',)
    list_filter = ('created',)
    list_editable = ('status',)
    summernote_fields = ('description',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(DjangoTricks)
class DjangoTricksAdmin(admin.ModelAdmin):
    list_display = ('name_video', 'id_video', 'created',)
    list_filter = ('created',)


@admin.register(AskedQuestions)
class AskedQuestionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'created',)
    list_filter = ('created',)


@admin.register(DjangoRoadMap)
class RoadMapDjangoAdmin(SummernoteModelAdmin):
    list_display = ('name',)
    summernote_fields = ('text',)


@admin.register(IpAddress)
class IPAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass