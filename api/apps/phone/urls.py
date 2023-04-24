from django.urls import path

from .views.webhook import fowarding, tracking, check_status


urlpatterns = [
    path('<int:call_id>/fowarding/', fowarding, name="call_fowarding"),
    path('<int:call_id>/tracking/', tracking, name="call_tracking"),
    path('<int:call_id>/status/', check_status, name="call_status"),
]
