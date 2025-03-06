from rest_framework import serializers

from .models import Product, Purchase, Sales
from django.db.models import Sum  # ← これを追加


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductAllSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()  # 在庫数を取得するカスタムフィールド
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']
    def get_stock(self, obj):
        """
        在庫数 = 仕入れの合計 - 売上の合計
        """
        # 仕入れ数の合計
        total_purchase = Purchase.objects.filter(product=obj).aggregate(Sum('quantity'))['quantity__sum'] or 0
        # 売上数の合計
        total_sales = Sales.objects.filter(product=obj).aggregate(Sum('quantity'))['quantity__sum'] or 0

        return total_purchase - total_sales

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    unit = serializers.IntegerField()
    quantity = serializers.IntegerField()
    type = serializers.IntegerField()
    date = serializers.DateTimeField()

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()