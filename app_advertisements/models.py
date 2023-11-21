from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your models here.

class Advertisements(models.Model):
    title = models.CharField("Заголовок", max_length=128)
    description = models.TextField('Описание')
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    auction = models.BooleanField("Торг", help_text="Отметьте, если торг уместен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    image = models.ImageField('Изображение', upload_to="advertisements/")

    def __str__(self):
        return f"Advertisement(id={self.id}, title={self.title}, price={self.price})"


    def get_absolute_url(self):
        return reverse('adv-detail', kwargs={'pk': self.id})


    @admin.display(description='дата создания')
    def created_date(self):
        from django.utils import timezone
        if self.created_at.date() == timezone.now().date():
            created_time = self.created_at.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: green; font-weight: bold;">Сегодня в {}</span>', created_time
            )
        elif self.updated_at.date() == timezone.now().date() - timezone.timedelta(hours=24):
            created_time = self.updated_at.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: green; font-weight: bold;">Вчера в {}</span>', created_time
            )

        return self.created_at.strftime("%d.%m.%Y в %H:%M:%S")
#g

    @admin.display(description='дата последнего обновления')
    def updated_date(self):
        from django.utils import timezone
        if self.updated_at.date() == timezone.now().date():
            created_time = self.updated_at.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: red; font-weight: bold;">Сегодня в {}</span>', created_time
            )
        elif self.updated_at.date() == timezone.now().date() - timezone.timedelta(hours=24):
            created_time = self.updated_at.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: red; font-weight: bold;">Вчера в {}</span>', created_time
            )
        return self.updated_at.strftime("%d.%m.%Y в %H:%M:%S")

    @admin.display(description='фото')
    def get_html_image(self):
        if self.image:
            return format_html(
                '<img src="{url}" style="max-width: 80px; max-height: 80px;"', url=self.image.url
            )


class Meta:
    db_table = "advertisements"