"""raterproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from gamerraterapi.views.pics import PicsViewSet
from gamerraterapi.views.rating import RatingViewSet
from gamerraterapi.views.review import ReviewViewSet
from gamerraterapi.views.category import CategoryViewSet
from gamerraterapi.views.game import GamesViewSet
from django.contrib import admin
from gamerraterapi.views import login_user, register_user
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GamesViewSet, 'game')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'reviews', ReviewViewSet, 'review')
router.register(r'ratings', RatingViewSet, 'rating')
router.register(r'images', PicsViewSet, 'pic')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)