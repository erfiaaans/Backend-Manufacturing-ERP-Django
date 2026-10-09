from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Warehouse,
    InventoryStock,
    StockMovement,
)

from .serializers import (
    WarehouseSerializers,
    InventoryStockSerializer,
    StockMovementSerializer,
)


class WarehouseListCreateView(APIView):
    def get(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializers(warehouses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WarehouseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseDetailView(APIView):
    def get_object(self, pk):
        warehouse = self.get_object(pk)
        serializer = WarehouseSerializers(warehouse)
        return Response(serializer.data)

    def put(self, request, pk):
        warehouse = self.get_object(pk)
        serializer = WarehouseSerializers(warehouse, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        warehouse = self.get_object(pk)
        serializer = WarehouseSerializers(warehouse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        warehouse = self.get_object(pk)
        warehouse.delete()
        return Response(
            {"message": "Warehouse berhasil dihapus"}, status=status.HTTP_204_NO_CONTENT
        )


class InventoryStockListView(APIView):
    def get(self, request):
        stocks = InventoryStock.objects.select_related("product", "warehouse")
        product_id = request.query_params.get("product")
        if product_id:
            stocks = stocks.filter(product_id=product_id)
        warehouse_id = request.query_params.get("warehouse")
        if warehouse_id:
            stocks = stocks.filter(warehouse_id=warehouse_id)
        serializer = InventoryStockSerializer(stocks, many=True)
        return Response(serializer.data)


class InventoryStockDetailView(APIView):
    def get(self, request, pk):
        stock = get_object_or_404(
            InventoryStock.objeects.select_related("product", "warehouse"), pk=pk
        )
        serializer = InventoryStockSerializer(stock)
        return Response(serializer.data)


class StockMovementListView(APIView):
    def get(self, request):
        movements = StockMovement.objects.select_related(
            "product", "warehouse", "created_by"
        )
        product_id = request.query_params.get("product")
        if product_id:
            movements = movements.filter(product_id=product_id)
        warehouse_id = request.query_params.get("warehouse")
        if warehouse_id:
            movements = movements.filter(warehouse_id=warehouse_id)
        movement_type = request.query_params.get("movement_type")
        if movement_type:
            movements = movements.filter(movement_type=movement_type)
        serializer = StockMovementSerializer(movements, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = StockMovementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product = serializer.validated_data["product"]
        warehouse = serializer.validated_data["warehouse"]
        movement_type = serializer.validated_data["movement_type"]
        quantity = serializer.validated_data["quantity"]

        if quantity <= Decimal("0"):
            return Response(
                {"message": "Quantity harus lebih besar dari 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        stock, created = InventoryStock.objects.get_or_create(
            product=product,
            warehouse=warehouse,
            defaults={
                "quantity": Decimal("0"),
                "reserved_quantity": Decimal("0"),
                "minimum_stock": Decimal("0"),
            },
        )
        if movement_type == StockMovement.MovementType.IN:
            stock.quantity += quantity
        elif movement_type == StockMovement.MovementType.OUT:
            available_quantity = stock.quantity - stock.reserved_quantity
            if quantity > available_quantity:
                return Response(
                    {
                        "message": "Stock tidak mencukupi",
                        "available_quantity": available_quantity,
                        "requested_quantity": quantity,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            stock.quantity -= quantity
        elif movement_type == StockMovement.MovementType.ADJUSTMENT:
            stock.quantity = quantity
        else:
            return Response(
                {"message": "Movement type tidak valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        stock.save()
        movement = serializer.save(created_by=request.user)
        return Response(
            {
                "message": "Stock movement berhasil dibuat",
                "movement": StockMovementSerializer(movement).data,
                "stock": InventoryStockSerializer(stock).data,
            },
            status=status.HTTP_201_CREATED,
        )


class StockMovementDetailView(APIView):
    def get(self, request, pk):
        movement = get_object_or_404(
            StockMovement.objects.select_related("product", "warehouse", "created_by"),
            pk=pk,
        )
        serializer = StockMovementSerializer(movement)
        return Response(serializer.data)
