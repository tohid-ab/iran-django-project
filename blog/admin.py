from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


class ReplyCommentInline(admin.StackedInline):
    model = ReplyComment
    extra = 0


class Comments(admin.ModelAdmin):
    list_display = ('name', 'comment', 'post', 'email', 'status',)
    list_filter = ('post', 'created_on',)

    inlines = [
        ReplyCommentInline,
    ]


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class ImageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'get_jalali_date', 'status',)
    list_filter = ('created',)
    list_editable = ('status',)
    summernote_fields = ('description',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        CommentInline,
    ]


class DjangoTricksAdmin(admin.ModelAdmin):
    list_display = ('name_video', 'id_video', 'created',)
    list_filter = ('created',)


class AskedQuestionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'created',)
    list_filter = ('created',)


class RoadMapDjangoAdmin(SummernoteModelAdmin):
    list_display = ('name',)
    summernote_fields = ('text',)


class IpAdmin(SummernoteModelAdmin):
    list_display = ('userName', 'userIp', 'get_jalali_date', 'item',)
    search_fields = ('userIp',)


admin.site.register(CategoryClass, CategoryAdmin)
admin.site.register(Comment, Comments)
admin.site.register(ReplyComment)
admin.site.register(ArticleClass, ImageAdmin)
admin.site.register(AskedQuestions, AskedQuestionsAdmin)
admin.site.register(DjangoRoadMap, RoadMapDjangoAdmin)
admin.site.register(Like)
admin.site.register(DjangoTricksDaily)
admin.site.register(ContactUs)
admin.site.register(IpUserToView, IpAdmin)