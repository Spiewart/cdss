from django.urls import path  # type: ignore

from .views import PageDetailView

app_name = "pages"

urlpatterns = [
    path("<int:pk>/", PageDetailView.as_view(), name="detail"),
]
