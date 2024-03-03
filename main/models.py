from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
import uuid

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img1 = models.ImageField("Фото профиля", upload_to="profile/", null=True, blank=True,)
    curss = models.JSONField('Купленные курсы',default=dict, null=True, blank=True,)
    # add additional fields in here


class regist(models.Model):
    username = models.CharField('Username', max_length=50)
    name= models.CharField('Name', max_length=50)
    email = models.EmailField('e-mail')
    password1 = models.CharField('Пароль', max_length=50)
    password2 = models.CharField('Повтор пароля', max_length=50)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class curs(models.Model):
    name = models.CharField('Название курса', max_length=50)
    info = models.TextField('Информация о курсе')
    dop_info = models.TextField('Дополнительная информация о курсе', blank=True, null=True)
    img = models.ImageField("Фото курса", upload_to="curs/")
    price = models.FloatField('Цена за курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-id']


class lessons(models.Model):
    curs = models.ForeignKey(curs, on_delete = models.CASCADE)
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название урока', max_length=50)
    video = models.FileField("Видео урока",
                             upload_to="video/",
                             null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
                             )
    text = models.TextField('Текст урока')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'



class lessons_text(models.Model):
    lesson = models.ForeignKey(lessons, on_delete = models.CASCADE)
    title = models.CharField('Что делаем?', max_length=50, null=True, blank=True)
    text = models.TextField('Дополнительный текст урока', null=True, blank=True)
    img = models.ImageField("Фото к тексту", upload_to="curs/", null=True, blank=True)

    code_or_not = (
        ('1', 'Yes'),
        ('2', 'No'),
        ('3', 'Photo')
    )
    code = models.CharField('Код?', max_length=10, choices=code_or_not)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Описание уроков'
        verbose_name_plural = 'Описание уроков'
        ordering = ['id']


class buy_curs(models.Model):
    name = models.CharField('За какой курс', max_length=50)
    curs = models.ForeignKey(curs, on_delete=models.CASCADE)
    price = models.FloatField('Цена за курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
