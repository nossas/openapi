"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from apps.actionnetwork.views import CampaignAPIListView
# from apps.auth2.views import UsersGroupListAPIView
from apps.phone.views import PhonePressureCreateAPIView, TargetPhoneListAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    
    # Phone Webhook URL
    path("api/phone/call/", include("apps.phone.urls")),
    
    # Campaigns URL
    path('api/campaigns/', CampaignAPIListView.as_view(), name="campaigns"),
    
    path("api/campaigns/<int:campaign_id>/phone/", PhonePressureCreateAPIView.as_view(), name="phone"),
    path("api/campaigns/<int:campaign_id>/phone/targets/", TargetPhoneListAPIView.as_view(), name="targets_phone"),
    

    # path('api/groups/', UsersGroupListAPIView.as_view(), name="usersgroups"),
]
