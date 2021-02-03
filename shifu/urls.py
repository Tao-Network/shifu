"""shifu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include,path,re_path
import web.api as api
import web.views as views
import web.auth as auth
from rest_framework import routers
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
import os,logging

api_info =   openapi.Info(
      title="Shifu API",
      default_version='v1',
      description="API for the Shifu Governance App",
      terms_of_service="https://shifu.tao.network/terms/",
      contact=openapi.Contact(email="info@tao.network"),
      license=openapi.License(name="BSD License"),
   )

schema_view = get_schema_view(
 	api_info,
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/candidates/', api.AllCandidatesApi.as_view(), name='all_candidates_api'),
	path('api/candidates/<address>/', api.OwnedCandidatesApi.as_view(), name='candidate_api'),
	path('api/network_info/', api.NetworkInfoApi.as_view(), name='network_info_api'),
	path('api/roi/<address>/', api.RoiApi.as_view(), name='roi_api'),
	path('api/roi/actual/<address>/', api.ActualRoiApi.as_view(), name='24Hour_roi_api'),
	path('api/votes/<address>/', api.VotesList.as_view(), name='vote_api'),
	path('api/earnings/details/<address>/', api.EarningsDetailsApi.as_view(), name = 'earnings_details_api'),
	path('api/earnings/', api.EarningsApi.as_view(), name='total_earnings_api'),
	path('api/earnings/<address>/', api.EarningsApi.as_view(), name='earnings_api'),

	path('profile/', login_required(views.account_profile), name='profile'),
	path('profile/<address>/', views.account_profile, name='account_profile'),

	re_path(r'^login_api/$', auth.login_api, name='web3_login_api'),
	re_path(r'^logout/', views.logout_view, name='logout'),
	re_path(r'^auto_login/', views.auto_login, name='autologin'),
	path('', views.index,name="index"),
	re_path(r'api/^$', schema_view, name='openapi-schema'),
	re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	re_path(r'^api/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
