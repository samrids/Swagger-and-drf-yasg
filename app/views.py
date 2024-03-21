
import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DocumentItem
from .serializers import DocumentItemSerializer


class DocumentItemList(APIView):
    # permission_classes = (IsAuthenticated,)
    """
    List [40] DocumentItem, 
    or create a new DocumentItem.
    """


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
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)