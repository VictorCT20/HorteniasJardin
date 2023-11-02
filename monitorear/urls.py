from django.urls import path
from .views import UserEntryView

app_name="monitorear"

urlpatterns = [
    path('', UserEntryView.as_view(), name="userEntry")
]