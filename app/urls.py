from django.urls import path

from .views import DocumentItemList

urlpatterns = [
    path('Document/', DocumentItemList.as_view()),
]