from django.urls import path
from .views import UserEntryView

app_name="monitoreo"

urlpatterns = [
    path('', UserEntryView.as_view(), name="userEntry")
]