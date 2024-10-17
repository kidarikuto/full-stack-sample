from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.responese import Responese
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status

class ProductView(APIView):
    """
    商品操作に関する関数
    """

    def get(self, requet format=None):
        """
        商品の一覧を取得する
        """
        queryset = Product.object.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)