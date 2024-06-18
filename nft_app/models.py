from django.db import models
from django.contrib.auth.views import get_user_model

User = get_user_model()

class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True

class Nft(TimeStampAbstractModel):

    class Meta:
        verbose_name = "NFT", 
        verbose_name_plural = 'NFT'
    name = models.CharField(verbose_name="Название Nft", max_length=100, unique=True)
    image = models.ImageField(verbose_name="Изображение NFT", upload_to="nft_image/")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена в Ethereum')
    token = models.TextField(verbose_name="Токен NFT", unique=True, editable=False)
    description = models.TextField(verbose_name="Описание NFT")
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name="nft")
    category = models.ForeignKey('nft_app.Categories', related_name="nfties",verbose_name="Выберите категории", on_delete=models.CASCADE)
    tags = models.ManyToManyField('nft_app.Tags', related_name="nfts")

    def __str__(self) -> str:
        return f'{self.name}'
    

class Categories(models.Model):
    class Meta:
        verbose_name = 'Категория', 
        verbose_name_plural = 'Категории'
    name = models.CharField(verbose_name='Название категории', max_length=100, unique=True)
    def __str__(self) -> str:
        return f'{self.name}'
    

class Tags(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    name = models.CharField(verbose_name="Название тега", max_length=100)
    def __str__(self) -> str:
        return f'{self.name}'
# Create your models here.
