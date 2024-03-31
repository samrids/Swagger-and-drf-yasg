from django.urls import path

from .views import DocumentItemList, DocumentItemUpdate, VendorList

urlpatterns = [
    path('Document/', DocumentItemList.as_view()),
    path('Document/<uuid:id>', DocumentItemUpdate.as_view()),

    path('Vendor/', VendorList.as_view()),
]