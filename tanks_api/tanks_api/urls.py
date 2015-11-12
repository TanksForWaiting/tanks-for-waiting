"""tanks_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers
from api.views import GameViewSet, PlayerViewSet, TargetViewSet, redirect_to_game

router = routers.SimpleRouter()
router.register(r'games', GameViewSet)
router.register(r'players', PlayerViewSet)
targets_router = routers.NestedSimpleRouter(router, r'games', lookup='games')
targets_router.register(r'targets', TargetViewSet)
# router.register(r'targets', TargetViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(targets_router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^', redirect_to_game),
]
