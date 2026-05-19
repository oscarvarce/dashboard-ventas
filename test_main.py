"""
Tests para el Dashboard de Ventas
=================================
Ejecutar con: pytest test_main.py
"""

import pytest
import pandas as pd
from datetime import datetime
from main import calcular_kpis, formatear_moneda


# ------------------------------------------------------------------
# FIXTURES: Datos de prueba reutilizables
# ------------------------------------------------------------------

@pytest.fixture
def df_ejemplo():
    """DataFrame de prueba con datos representativos."""
    return pd.DataFrame({
        "Fecha": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01", "2025-01-15"]),
        "Producto": ["Laptop Pro", "Mouse Wireless", "Laptop Pro", "Monitor 4K"],
        "Región": ["Norte", "Sur", "Norte", "Este"],
        "Vendedor": ["Ana García", "Carlos Ruiz", "Ana García", "María López"],
        "Cantidad": [2, 5, 3, 1],
        "Precio_Unitario": [1000.0, 25.0, 1000.0, 500.0],
        "Total_Venta": [2000.0, 125.0, 3000.0, 500.0]
    })


@pytest.fixture
def df_minimo():
    """DataFrame con solo las columnas obligatorias."""
    return pd.DataFrame({
        "Fecha": pd.to_datetime(["2025-01-01", "2025-02-01"]),
        "Producto": ["A", "B"],
        "Cantidad": [1, 2],
        "Total_Venta": [100.0, 200.0]
    })


# ------------------------------------------------------------------
# TESTS: formatear_moneda()
# ------------------------------------------------------------------

class TestFormatearMoneda:
    def test_entero(self):
        assert formatear_moneda(1000) == "$1,000.00"

    def test_decimales(self):
        assert formatear_moneda(1234.5) == "$1,234.50"

    def test_cero(self):
        assert formatear_moneda(0) == "$0.00"

    def test_miles(self):
        assert formatear_moneda(1000000) == "$1,000,000.00"


# ------------------------------------------------------------------
# TESTS: calcular_kpis()
# ------------------------------------------------------------------

class TestCalcularKpis:
    def test_total_ventas_correcto(self, df_ejemplo):
        kpis = calcular_kpis(df_ejemplo)
        assert kpis["total_ventas"] == 5625.0  # 2000 + 125 + 3000 + 500

    def test_total_unidades_correcto(self, df_ejemplo):
        kpis = calcular_kpis(df_ejemplo)
        assert kpis["total_unidades"] == 11  # 2 + 5 + 3 + 1

    def test_promedio_venta_correcto(self, df_ejemplo):
        kpis = calcular_kpis(df_ejemplo)
        assert kpis["promedio_venta"] == 5625.0 / 4  # 1406.25

    def test_num_transacciones(self, df_ejemplo):
        kpis = calcular_kpis(df_ejemplo)
        assert kpis["num_transacciones"] == 4

    def test_mejor_vendedor(self, df_ejemplo):
        kpis = calcular_kpis(df_ejemplo)
        assert kpis["mejor_vendedor"] == "Ana García"  # 2000 + 3000 = 5000
        assert kpis["ventas_mejor"] == 5000.0

    def test_producto_top(self, df_ejemplo):
        kpis = calcular_kpis(df_ejemplo)
        assert kpis["producto_top"] == "Laptop Pro"  # 2000 + 3000 = 5000
        assert kpis["ventas_top"] == 5000.0

    def test_columnas_opcionales_faltantes(self, df_minimo):
        """Si faltan Vendedor/Región/Producto, no debe fallar."""
        kpis = calcular_kpis(df_minimo)
        assert kpis["total_ventas"] == 300.0
        assert kpis["mejor_vendedor"] == "N/A"
        assert kpis["producto_top"] == "N/A"

    def test_dataframe_vacio(self):
        """Manejo de DataFrame vacio (edge case)."""
        df_vacio = pd.DataFrame(columns=["Fecha", "Producto", "Cantidad", "Total_Venta"])
        df_vacio["Fecha"] = pd.to_datetime(df_vacio["Fecha"])
        kpis = calcular_kpis(df_vacio)
        assert kpis["total_ventas"] == 0
        assert kpis["num_transacciones"] == 0
