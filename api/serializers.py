from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from drf_extra_fields.fields import Base64ImageField
from rest_framework.authtoken.models import Token
from nft_app.models import *



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')



class DetailNftSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Nft
        fields = '__all__'


class CreateNftSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False) 
    class Meta:
        model = Nft
        fields = '__all__'



class NftSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False) 
    class Meta:
        model = Nft
        fields = '__all__'


class ListNftSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Nft
        exclude = ('description',)




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()




class DetailTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Token
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Token
        fields = '__all__'




class RegisterSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()  # Используем Base64ImageField вместо ListSerializer
    password1 = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions',)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        
        if password1 != password2:
            raise serializers.ValidationError({
                'password2': ['Пароли не совпадают!']
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = make_password(password)

        return super().create(validated_data)
    

class BinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Binance
        fields = '__all__'


class DetailUserSerializer(serializers.ModelSerializer):
    binance = BinanceSerializer()
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')

