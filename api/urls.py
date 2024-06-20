from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('nfts', NftViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('tokens', TokenViewSet, basename="tokens")
urlpatterns = [
    path('nfts/buy/<int:id>/', NftBuy.as_view()),

    path('user/<int:id>/', UserViewSet.as_view()),

    path('auth/login/', LoginApiView.as_view()),
    path('auth/register/', RegisterApiView.as_view()),
    
    path('redactor_profile/<int:id>/', RedactorProfileApiView.as_view()),
    path('', include(router.urls)),
]