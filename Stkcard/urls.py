from django.conf.urls import url
from django.urls import path

from .views import TransactionDelete, TransactionList

urlpatterns = [
    path('trnxlist/', TransactionList.as_view(), name='transactionlist_link'),
    url(r'^trnxdel/(?P<pk>[0-9]+)/$', TransactionDelete.as_view()),
]