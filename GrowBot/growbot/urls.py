import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect, HttpResponse

## User login
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

## Import apps
from growbot.api import views
from growbot.dashboard.views import *

## RESTful junk
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'power', views.PowerSwitchViewSet)
router.register(r'outlet', views.PowerOutletViewSet)
router.register(r'snapshot', views.CameraSnapshotViewSet)
urlpatterns = [
  url(r'^accounts/profile/', lambda r: HttpResponseRedirect('dashboard/')),
  url(r'^$', lambda r: HttpResponseRedirect('dashboard/')),
  url(r'^dashboard/*', DashboardView.as_view(),name='dashboard'),
  url(r'^api/*', include(router.urls)),
  url(r'^admin/', admin.site.urls),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  url(regex=r'^login/$',view=login,kwargs={'template_name': 'dashboard/login.html'},name='login'),
  url(regex=r'^logout/$',view=logout,kwargs={'next_page': '/'},name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root='/')
