from django.shortcuts import render
from django.conf import settings
# Create your views here.

from django.db.models import F, Value, Sum
from django.db.models.functions import TruncMonth

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import Product, Purchase, Sales, SalesFile, Status
from .serializers import InventorySerializer, ProductSerializer, PurchaseSerializer, SaleSerializer, ProductAllSerializer,\
                            FileSerializer, SalesSerializer


import pandas

from api.inventory.authentication import RefreshJWTAuthentication
from .authentication import AccessJWTAuthentication, RefreshJWTAuthentication

class ProductListView(APIView):
    def get(self, request, format=None):
        """
        商品一覧を取得（在庫数も含める）
        """
        queryset = Product.objects.all()
        serializer = ProductAllSerializer(queryset, many=True)
        print(f"\nserializer:{serializer}\n")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductView(APIView):
    """
    商品操作に関する関数
    """
    # authentication_classes = [AccessJWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # 認証無効化時、認証クラスを空にする
    authentication_classes = []
    permission_classes = []

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, id=None, format=None):
        """
        商品の一覧、もしくは一位の商品をを取得する
        """
        if id is None :
            # queryset = Product.objects.all()
            # serializer = ProductSerializer(queryset, many=True)
            # print(f"\queryset{queryset}\n")
            # print(f"\nProductSerializer{serializer}\n")
            queryset = Product.objects.all()
            serializer = ProductAllSerializer(queryset, many=True)
            print(f"\nserializer:{serializer.data}\n")
        else: 
            product = self.get_object(id)
            serializer = ProductSerializer(product)            
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        #validationを通らなかった場合、例外を投げる
        #⇒検証したデータを永続化する
        print(f"\nReceived Request Data: {request.data}\n")
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def put(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(status = status.HTTP_200_OK)

class PurchaseView(APIView):
    """
    仕入れ情報を登録する
    """
    def post(self, request, format=None):
        print(f"\nReceived Request Data: {request.data}\n")
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class SalesView(APIView):
    """
    売上情報を登録する
    """
    def post(self, request, format=None):
        serializer = SaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InventoryView(APIView):   
    authentication_classes = []
    permission_classes = []
    # 仕入れ,売上情報を取得する
    def get(self, request, id=None, format=None):
        print(f"\n inventoryView: id={id}\n")  # デバッグ用
        if id is None :
            # 件数が多くなるので商品IDは必ず指定する
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST)
        else:
            # UNIONするために、それぞれフィールド名を再定義している
            # WHERE句のようにfileterで絞り込み
            # product_idに紐づく情報をprefetch_relatedでJOINしている
            # valuesによって取得するデータやカラム名の加工
            purchase = Purchase.objects.filter(product_id=id).prefetch_related('product').values(
                "id", "quantity", type=Value('1'), date=F('purchase_date'), unit=F('product__price'))
            sales = Sales.objects.filter(product_id=id).prefetch_related('product').values(
                "id", "quantity", type=Value('2'), date=F('sales_date'), unit=F('product__price'))
            # unionによって2つのクエリセットを1つにまとめている、その後order_byで日付カラムの並び変え
            queryset = purchase.union(sales).order_by(F("date"))
            serializer = InventorySerializer(queryset, many=True)
            print(f"\nInventorySerializer:{serializer.data}\n")
            print(f"\nInventorySerializer:{purchase}\n")
            print(f"\nInventorySerializer:{sales}\n")
            return Response(serializer.data, status.HTTP_200_OK)    
class LoginView(APIView):
    """ユーザーのログイン処理
    Args:
    APIView (class): rest_framework.viewsのAPIViewを受け取る
    """
    # 認証クラスの指定
    # リクエストヘッダーにtokenを差し込む追加処理はないのでそのまま継承
    # authentication_classes = [JWTAuthentication]
    authentication_classes = []
    # アクセス許可の指定
    permission_classes = []

    def post(self, request):
        # 認証無効化時、以下コメントアウト
        # serializer = TokenObtainPairSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # access = serializer.validated_data.get("access", None)
        # refresh = serializer.validated_data.get("refresh", None)

        # if access:
        #     response = Response(status=status.HTTP_200_OK)
        #     max_age = settings.COOKIE_TIME
        #     response.set_cookie('access', access, httponly=True, max_age=max_age)
        #     response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)
            # return response
        # return Response({'errMsg': 'ユーザーの認証に失敗しました'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg': 'ログアウト処理は不要です'}, status=status.HTTP_200_OK)
    
class RetryView(APIView):
    # authentication_classes = [RefreshJWTAuthentication]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # 認証無効化時、以下コメントアウト
        # request.data['refresh'] = request.META.get('HTTP_REFRESH_TOKEN')
        # serializer = TokenRefreshSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # access = serializer.validated_data.get('access', None)
        # refresh = serializer.validated_data.get("refresh", None)
        # if access:
        #     response = Response(status=status.HTTP_200_OK)
        #     max_age = settings.COOKIE_TIME
        #     response.set_cookie('access', access, httponly=True, max_age=max_age)
        #     response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)
        #     return response
        # return Response({'errMsg': 'ユーザーの認証に失敗しました'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg': 'ログアウト処理は不要です'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
    
class SalesSyncViews(APIView):
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filename = serializer.validated_data['file'].name

        with open(filename, 'wb') as f:
            f.write(serializer.validated_data['file'].read())
        
        sales_file = SalesFile(file_name=filename, status=Status.SYNC)
        sales_file.save()

        df = pandas.read_csv(filename)
        for _ , row in df.iterrows():
            sales = Sales(product_id = row['product'], sales_data=row['date'],quantity=row['quantity'], import_file=sales_file)
            sales.save()
        
        return Response(status=201)
    
class SalesAsyncViews(APIView):
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filename = serializer.validated_data['file'].name

        with open(filename, 'wb') as f:
            f.write(serializer.validated_data['file'].read())

        sales_file = SalesFile(file_name=filename, status=Status.ASYNC_UNPROCESSED)
        sales_file.save()

        return Response(status=201)

class SalesList(ListAPIView):
    queryset = Sales.objects.annotate(monthly_data=TruncMonth('sales_data')).values('monthly_data')\
                            .annotate(monthly_price=Sum('quantity')).order_by('monthly_data')
    serializer_class = SalesSerializer
    print(f"\n{queryset=}\n")
    
