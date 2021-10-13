from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, mixins, generics
from rest_framework import filters as rest_filter
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from .serializers import *
from .paginations import *
from .permissions import *


class SignUpApi(APIView):
    serializer_class = SignUpSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            login_user, token = serializer.registered()
        
            return Response({
                "user": UserSerializer(login_user).data,
                "token": token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SignInApi(APIView):
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            login_user = serializer.sign_in()
            token, token_created = Token.objects.get_or_create(user=login_user)

            return Response({
                "user": UserSerializer(login_user).data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class InvoiceApi(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, InvoiceHasOwnPermission)
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == "list":
            return MinimalInvoiceSerializer
        return InvoiceSerializer
        
    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user).prefetch_related("user", "items")


class ItemApi(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated, ItemHasOwnPermission)
    serializers = ItemSerializer
    queryset = Item.objects.all()