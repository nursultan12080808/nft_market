from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerProductOrReadOnly, IsSalesmanOrReadOnly, IsAdminUserOrReadOnly, IsSalesman
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from api.paginations import MediumPagination
from .filters import NftFilter
from django.core.mail import send_mail
from .serializers import *
from nft_app.models import *
from account.models import User


class NftViewSet(ModelViewSet):
    queryset = Nft.objects.all()
    lookup_field = 'token'
    serializer_class = {
        'list': ListNftSerializer,
        'retrieve': DetailNftSerializer,
        'create': CreateNftSerializer,
        'update': NftSerializer,
    }
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NftFilter
    pagination_class = MediumPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.serializer_class['update']
        return self.serializer_class[self.action] 


class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    lookup_field = 'id'
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly)



class TagViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly)



class UserViewSet(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = DetailUserSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)
    
    

class TokenViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = {
        'list': DetailTokenSerializer,
        'retrieve': DetailTokenSerializer,
        'create': TokenSerializer,
        'update': TokenSerializer,
    }
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.serializer_class['update']
        return self.serializer_class[self.action] 



class LoginApiView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = DetailUserSerializer(user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key
            })
        return Response({'detail': 'Не существуеет пользователя либо неверный пароль.'}, status.HTTP_400_BAD_REQUEST)


class RedactorProfileApiView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = request.data.get('password')
        if(password):
            if check_password(password, user.password):
                new_password = request.data.get('password1')
                user.set_password(new_password)
                user.save()
            else:
                return Response({'error': 'Пароль неверный'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = DetailUserSerializer(user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key
        })
    


class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = DetailUserSerializer(user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key
        })
    


class NftBuy(GenericAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, token_nft, *args, **kwargs):
        token = request.headers["Authorization"].split(' ')[1]
        token = Token.objects.get(key=token)
        if token_nft[-1] == 'n':
            token_nft = token_nft.replace("\n", "")
        nft = get_object_or_404(Nft, token=token_nft)
        user_data = TokenSerializer(instance=token)
        user = User.objects.get(id = user_data.data["user"]["id"])
        print(user)
        if nft and user:
            seller = User.objects.get(id = nft.user.id)
            if nft.price <= user.cash:
                nft.user = user
                seller.cash = seller.cash + nft.price
                user.cash = user.cash - nft.price
                nft.save()
                user.save()
                seller.save()
                return Response({
                "data": f"Вы успешно купили {nft}!!!"
                })
            return Response({
            "error": f"У вас не достаточно средств"
            })
        return Response({
            "error": "Что то пошло не так :("
            })



class BinanceAcc(GenericAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def post(self, request, *args, **kwargs):
        token = request.headers["Authorization"].split(' ')[1]
        token = Token.objects.get(key=token)
        user = User.objects.get(id = token.user.id)
        email = request.data.get("email")
        try:
            acc = get_object_or_404(Binance, email = email)
        except Http404:
            return Response({"error": "Нету такого пользователя!"})
        if acc:
            password_bin = request.data.get('password')
            if acc.password == password_bin[0:len(password_bin) - 1]:
                serializer = BinanceSerializer(acc)
                user.wallet = acc
                user.save()
                return Response({"data": serializer.data})
            return Response({"error": "Не правильный пароль!"})
        return Response({"error": "Нету такого пользователя!"})
    


class MbankAcc(GenericAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def post(self, request, *args, **kwargs):
        token = request.headers["Authorization"].split(' ')[1]
        token = Token.objects.get(key=token)
        user = User.objects.get(id = token.user.id)
        phone = request.data.get("phone")
        try:
            acc = get_object_or_404(Mbank, phone = phone)
        except Http404:
            return Response({"error": "Нету такого пользователя!"})
        if acc:
            password_bin = request.data.get('password')
            if acc.password == password_bin[0:len(password_bin) - 1]:
                serializer = MbankSerializer(acc)
                user.wallet = acc
                user.save()
                return Response({"data": serializer.data})
            return Response({"error": "Не правильный пароль!"})
        return Response({"error": "Нету такого пользователя!"})
    
    

class GetMoneyBinance(GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def post(self, request, id, *args, **kwargs):
        token = request.headers["Authorization"].split(' ')[1]
        token = Token.objects.get(key=token)
        user = get_object_or_404(User, id = token.user.id)
        if user.wallet:
            binance = Binance.objects.get(id = id)
            money = request.data.get("price")
            money = int(money)
            if (binance.price - money) > 0:
                binance.price = binance.price - money
                user.cash = user.cash + money
                binance.save()
                user.save()
                return Response({"data": f"Ваш баланс паполнен на {money}"})
            return Response({"error": f"На вашем балансе не достаточно средств"})
        return Response({"error": f"Нет бинанс аккаунта"})
        


class GetMoneyMbank(GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def post(self, request, id, *args, **kwargs):
        token = request.headers["Authorization"].split(' ')[1]
        token = Token.objects.get(key=token)
        user = get_object_or_404(User, id = token.user.id)
        if user.wallet:
            mbank = Mbank.objects.get(id = id)
            money = request.data.get("price")
            money = int(money)
            if (mbank.price - money) > 0:
                mbank.price = mbank.price - money
                user.cash = user.cash + money
                mbank.save()
                user.save()
                return Response({"data": f"Ваш баланс паполнен на {money}"})
            return Response({"error": f"На вашем балансе не достаточно средств"})
        return Response({"error": f"Нет бинанс аккаунта"})


class MessageForUser(GenericAPIView):

    def post(self, request, *args, **kwargs):
        subject = 'Важная информация с market_nft'
        message = request.data.get("message")
        email_from = 'nursultan.top.game@gmail.com'
        recipient_list = []
        for item in User.objects.all():
            recipient_list.append(item.email)
        print(recipient_list)
        send_mail(subject, message, email_from, recipient_list)
        return Response({
            "data": "Успешно отправлены письма на электронные почты"
        })

# Create your views here.
