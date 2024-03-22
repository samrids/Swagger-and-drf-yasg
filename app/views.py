
import json

import requests
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DocumentItem
from .serializers import DocumentItemSerializer


class DocumentItemList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    """
    List [40] DocumentItem, 
    or create a new DocumentItem.
    """
    def get_object(self, pk):
        try:
            return DocumentItem.objects.get(pk=pk)
        except DocumentItem.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: DocumentItemSerializer(many=True)})
    def get(self, request, format=None):
        dataset = DocumentItem.objects.all().order_by('-created_at')[:40]
        serializer = DocumentItemSerializer(dataset, many=True)
        #Validate
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DocumentItemSerializer,
        responses={'201': openapi.Response('response description', DocumentItemSerializer(many=True))}
    )
    def post(self, request, format=None):
        serializer = DocumentItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user) #Create

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        request_body=DocumentItemSerializer,
        responses={'200': openapi.Response('response description', DocumentItemSerializer(many=True))}
    )
    def put(self, request, format=None):
        old_data = self.get_object(pk=request.data['id'])
        serializer = DocumentItemSerializer(old_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=self.request.user) #Update

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        