from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('nfts', NftViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('users', UserViewSet)
router.register('tokens', TokenViewSet, basename="tokens")
urlpatterns = [
    path('binance/login/', BinanceAcc.as_view()),
    path('mbank/login/', MbankAcc.as_view()),

    path('nft_buy/<str:token_nft>/', NftBuy.as_view()),

    path('get_money_binace/<int:id>/', GetMoneyBinance.as_view()),
    path('get_money_mbank/<int:id>/', GetMoneyMbank.as_view()),


    path('auth/login/', LoginApiView.as_view()),
    path('auth/register/', RegisterApiView.as_view()),


    path('user_message/', MessageForUser.as_view()),

    # path('send_code/', CodeForUser.as_view()),

    # path('check_code/', CodeVerif.as_view()),
    
    path('redactor_profile/<int:id>/', RedactorProfileApiView.as_view()),
    path('', include(router.urls)),
]