from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from account.managers import UserManager


class User(AbstractUser):
    CLIENT = 'client'
    SALESMAN = 'salesman'
    ADMIN = 'admin'

    ROLE = (
        (CLIENT, 'Покупатель'),
        (SALESMAN, 'Продавец'),
        (ADMIN, 'Администратор')
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    avatar = models.ImageField(upload_to='avatars/', verbose_name='аватарка', null=True, blank=True)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона')
    email = models.EmailField(blank=True, verbose_name='электронная почта', unique=True)
    role = models.CharField('роль', choices=ROLE, default=CLIENT, max_length=15)
    bio = models.TextField(verbose_name='Биография')
    cash = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Кошелёк в ETH', editable=False, default=0.00)
    followers = models.IntegerField(verbose_name="Подписчики", default=0, editable=False)
    binance = models.ForeignKey('nft_app.Binance', related_name="user", editable=False,null=True, blank=True, on_delete=models.CASCADE)
    mbank = models.ForeignKey('nft_app.Mbank', related_name="user", editable=False,null=True, blank=True, on_delete=models.CASCADE)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    get_full_name.fget.short_description = 'полное имя'

    def __str__(self):
        return f'{self.email or str(self.phone)}'



