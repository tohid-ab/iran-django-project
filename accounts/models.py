from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, max_length=255)
    image = models.ImageField(default="profiles/profile.jpg", upload_to="profiles/profile/", verbose_name='انتخاب عکس')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل'

    def image_tag(self):
        return format_html("<img width=50 style='border-radius:5px;' src='{}'>".format(self.image.url))
    image_tag.short_description = 'پروفایل'

