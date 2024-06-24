import cryptography
import secrets
import base64
import getpass
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
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



@receiver(post_save, sender=Nft)
def pre_save_nft(sender,instance: Nft, created, *args, **kwargs):
    if created:
        instance.token = encrypt_text(instance.name, key)