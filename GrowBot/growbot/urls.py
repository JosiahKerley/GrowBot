from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from growbot.api import views

router = routers.DefaultRouter()
router.register(r'power', views.PowerSwitchViewSet)
router.register(r'outlet', views.PowerOutletViewSet)
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
