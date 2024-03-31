import json

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MovementTransaction, Product
from .serializers import (MovementTransactionCreateSerializer,
                          MovementTransactionSerializer)


class TransactionList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    """
    List all TransactionList, or create a new TransactionList.
    """

    def get_object(self, pk):
        try:
            return MovementTransaction.objects.get(pk=pk)
        except MovementTransaction.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: MovementTransactionSerializer(many=True)})
    def get(self, request, format=None):
        dataset = MovementTransaction.objects.all().order_by('-created_at')[:40]
        serializer = MovementTransactionSerializer(dataset, many=True)
        #Validate
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MovementTransactionCreateSerializer,
        responses={'201': openapi.Response('response description', MovementTransactionCreateSerializer(many=True))}
    )
    def post(self, request, format=None):
        serializer = MovementTransactionCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(created_by=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDelete(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    """
    Delete a TransactionList by id.
    """

    def get_object(self, pk):
        try:
            return MovementTransaction.objects.get(pk=pk)
        except MovementTransaction.DoesNotExist:
            raise Http404

    
    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        if data:
            data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)