from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status

from rest_framework.viewsets import ModelViewSet

class ProductView(APIView):
    """
    商品操作に関する関数
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, id=None, format=None):
        """
        商品の一覧、もしくは一位の商品をを取得する
        """
        if id is None:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
        else:
            product = self.get_object(id)
            serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        #validationを通らなかった場合、例外を投げる
        #⇒検証したデータを永続化する
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def put(self, request, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(instance=product, data=requeset.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(statu=status.HTTP_200_OK)

    

class PurchaseView(APIView):
    """
    仕入れ情報を登録する
    """
    def post(self, request, format=None):
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class SalesView(APIView):
    """
    売上情報を登録する
    """
    def post(self, request, format=None):
        serializer = SalesSerializer(data=request.data)
        serializer.is_vali(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)



class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


