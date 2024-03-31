
import json

import requests
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
# from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from organizations.models import Organization, OrganizationUser
from rest_framework import permissions, status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DocumentItem, Vendor
from .serializers import (DocumentItemSerializer, DocumentItemUpdSerializer,
                          VendorSerializer)


class VendorList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # filter_backends = [DjangoFilterBackend,filters.OrderingFilter]

    """
    List [40] Vendor,
    or create a new Vendor.
    """

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: VendorSerializer(many=True)})
    def get(self, request, format=None):
        # org_id = OrganizationUser.objects.get(user=request.user).organization_id
            
        dataset = Vendor.objects.for_user(self.request.user).order_by('-created_at')[:40]
        serializer = VendorSerializer(dataset, many=True)
        #Validate
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=VendorSerializer,
        responses={'201': openapi.Response('response description', VendorSerializer(many=False))}
    )
    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            # todo organization_id
            org_id = OrganizationUser.objects.get(user=request.user).organization_id
            serializer.save(created_by=self.request.user, organization_id=org_id) #Create

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentItemList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    # permission_classes = [AllowAny]
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
        responses={'201': openapi.Response('response description', DocumentItemSerializer(many=False))}
    )
    def post(self, request, format=None):
        serializer = DocumentItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user) #Create

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DocumentItemUpdate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    """
    Update DocumentItem by id (uuid)
    """
    def get_object(self, pk):
        try:
            return DocumentItem.objects.get(pk=pk)
        except DocumentItem.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=DocumentItemUpdSerializer,
        responses={'200': openapi.Response('response description', DocumentItemUpdSerializer(many=False))}
    )
    def put(self, request, id, format=None):
        old_data = self.get_object(pk=id)
        serializer = DocumentItemUpdSerializer(old_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=self.request.user) #Update

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                