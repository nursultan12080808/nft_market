from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
import random
from .models import *


# Генерируем ключ для шифрования
def generate_key():
    return Fernet.generate_key()

# Функция для шифрования текста
def encrypt_text(text, key):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text.decode()

# Получаем ключ для шифрования
key = generate_key()



@receiver(pre_save, sender=Nft)
def pre_save_nft(sender, instance: Nft, *args, **kwargs):
    if not instance.token:
        instance.token = encrypt_text(instance.name, key)



@receiver(pre_save, sender=CodeForEmail)
def pre_save_nft(sender, instance: Nft, *args, **kwargs):
    if not instance.code:
        code = random.randint(100000, 999999)
        instance.code = str(code)