"""
Dashboard de Análisis de Ventas - Streamlit App
================================================
Aplicación interactiva para análisis de datos de ventas.
Autor: [Tu Nombre]
Fecha: 2026-05-19
"""

# ------------------------------------------------------------------
# SECCIÓN 1: IMPORTACIÓN DE LIBRERÍAS
# ------------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os


# ------------------------------------------------------------------
# SECCIÓN 2: CONFIGURACIÓN GLOBAL DE LA PÁGINA
# ------------------------------------------------------------------

st.set_page_config(
    page_title="📊 Dashboard de Ventas",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------------
# SECCIÓN 2.5: PALETA DE COLORES PERSONALIZADA
# ------------------------------------------------------------------
# Centralizamos los colores para facilitar cambios y mantener
# consistencia visual en todo el dashboard.
COLOR_PRIMARIO = "#6366f1"      # Indigo vibrante (líneas, acentos)
COLOR_SECUNDARIO = "#10b981"    # Esmeralda (barras, éxitos)
COLOR_ACENTO = "#f59e0b"        # Ámbar (alertas, destacados)
COLOR_GRISES = "#64748b"        # Slate (textos secundarios)

# ------------------------------------------------------------------
# SECCIÓN 3: FUNCIONES AUXILIARES (Helpers)
# ------------------------------------------------------------------

@st.cache_data
def cargar_datos_default():
    """
    Carga el dataset de ejemplo incluido en el repositorio.
    El decorador @st.cache_data evita recargar el archivo en cada interacción,
    mejorando drásticamente el rendimiento de la app.
    """
    df = pd.read_csv("ventas_ejemplo.csv")
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df


def cargar_csv_usuario(archivo_subido):
    """
    Carga un CSV subido por el usuario y valida que tenga las columnas mínimas.
    Retorna el DataFrame o None si hay error.
    """
    try:
        df = pd.read_csv(archivo_subido)
        # Validación básica de columnas esperadas
        columnas_esperadas = {"Fecha", "Producto", "Cantidad", "Total_Venta"}
        if not columnas_esperadas.issubset(set(df.columns)):
            st.error(f"❌ El CSV debe contener al menos las columnas: {columnas_esperadas}")
            return None
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
        if df["Fecha"].isna().any():
            st.warning("⚠️ Algunas fechas no pudieron convertirse. Revisa el formato.")
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        return None


def formatear_moneda(valor):
    """
    Formatea un número como moneda (USD) para mostrar en la interfaz.
    """
    return f"${valor:,.2f}"


def calcular_kpis(df):
    """
    Calcula las métricas clave (KPIs) a partir del DataFrame filtrado.
    Retorna un diccionario con los valores formateados.
    """
    total_ventas = df["Total_Venta"].sum()
    total_unidades = df["Cantidad"].sum()
    promedio_venta = df["Total_Venta"].mean()
    num_transacciones = len(df)

    # Mejor vendedor (por total de ventas)
    if "Vendedor" in df.columns:
        mejor_vendedor = df.groupby("Vendedor")["Total_Venta"].sum().idxmax()
        ventas_mejor = df.groupby("Vendedor")["Total_Venta"].sum().max()
    else:
        mejor_vendedor = "N/A"
        ventas_mejor = 0

    # Producto top
    if "Producto" in df.columns:
        producto_top = df.groupby("Producto")["Total_Venta"].sum().idxmax()
        ventas_top = df.groupby("Producto")["Total_Venta"].sum().max()
    else:
        producto_top = "N/A"
        ventas_top = 0

    return {
        "total_ventas": total_ventas,
        "total_unidades": total_unidades,
        "promedio_venta": promedio_venta,
        "num_transacciones": num_transacciones,
        "mejor_vendedor": mejor_vendedor,
        "ventas_mejor": ventas_mejor,
        "producto_top": producto_top,
        "ventas_top": ventas_top,
    }


# ------------------------------------------------------------------
# SECCIÓN 4: BARRA LATERAL (Sidebar) - Carga de datos y Filtros
# ------------------------------------------------------------------

st.sidebar.title("⚙️ Panel de Control")
st.sidebar.markdown("---")

# --- 4.1 Selector de fuente de datos ---
st.sidebar.subheader("📁 Fuente de Datos")

opcion_datos = st.sidebar.radio(
    "Selecciona una opción:",
    options=["Usar dataset de ejemplo", "Subir mi propio CSV"],
    index=0,
    help="Elige si quieres usar los datos de demostración o cargar tu propio archivo."
)

df = None

if opcion_datos == "Usar dataset de ejemplo":
    df = cargar_datos_default()
    st.sidebar.success("✅ Dataset de ejemplo cargado (500 registros)")
else:
    archivo = st.sidebar.file_uploader(
        "📤 Arrastra o selecciona tu archivo CSV",
        type=["csv"],
        help="El archivo debe contener columnas: Fecha, Producto, Cantidad, Total_Venta, etc."
    )
    if archivo is not None:
        df = cargar_csv_usuario(archivo)
        if df is not None:
            st.sidebar.success(f"✅ Archivo cargado: {len(df)} registros")
    else:
        st.sidebar.info("⏳ Esperando archivo CSV...")

st.sidebar.markdown("---")


# ------------------------------------------------------------------
# SECCIÓN 5: CONTENIDO PRINCIPAL (Solo si hay datos cargados)
# ------------------------------------------------------------------

if df is not None:

    # --- 5.1 Filtros dinámicos en la sidebar ---
    st.sidebar.subheader("🔍 Filtros")

    # Filtro de rango de fechas
    fecha_min = df["Fecha"].min().date()
    fecha_max = df["Fecha"].max().date()

    rango_fechas = st.sidebar.date_input(
        "Rango de fechas:",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
        help="Filtra los datos por un período específico."
    )

    # Asegurar que se seleccionaron dos fechas
    if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
    else:
        fecha_inicio, fecha_fin = fecha_min, fecha_max

    # Filtro de Región (si existe la columna)
    if "Región" in df.columns:
        regiones = sorted(df["Región"].unique())
        region_seleccionada = st.sidebar.multiselect(
            "Región:",
            options=regiones,
            default=regiones,
            help="Selecciona una o varias regiones para filtrar."
        )
    else:
        region_seleccionada = []

    # Filtro de Producto (si existe la columna)
    if "Producto" in df.columns:
        productos = sorted(df["Producto"].unique())
        producto_seleccionado = st.sidebar.multiselect(
            "Producto:",
            options=productos,
            default=productos,
            help="Selecciona uno o varios productos."
        )
    else:
        producto_seleccionado = []

    # Filtro de Vendedor (si existe la columna)
    if "Vendedor" in df.columns:
        vendedores = sorted(df["Vendedor"].unique())
        vendedor_seleccionado = st.sidebar.multiselect(
            "Vendedor:",
            options=vendedores,
            default=vendedores,
            help="Selecciona uno o varios vendedores."
        )
    else:
        vendedor_seleccionado = []

    st.sidebar.markdown("---")
    st.sidebar.info("💡 Tip: Puedes descargar los datos filtrados desde la tabla inferior.")


    # --- 5.2 Aplicar filtros al DataFrame ---
    df_filtrado = df.copy()

    # Filtro de fechas
    df_filtrado = df_filtrado[
        (df_filtrado["Fecha"].dt.date >= fecha_inicio) &
        (df_filtrado["Fecha"].dt.date <= fecha_fin)
    ]

    # Filtro de región
    if region_seleccionada:
        df_filtrado = df_filtrado[df_filtrado["Región"].isin(region_seleccionada)]

    # Filtro de producto
    if producto_seleccionado:
        df_filtrado = df_filtrado[df_filtrado["Producto"].isin(producto_seleccionado)]

    # Filtro de vendedor
    if vendedor_seleccionado:
        df_filtrado = df_filtrado[df_filtrado["Vendedor"].isin(vendedor_seleccionado)]


    # --- 5.3 Encabezado del Dashboard ---
    st.title("📊 Dashboard de Análisis de Ventas")
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;">
        📅 <b>Período analizado:</b> {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}  
        📋 <b>Registros filtrados:</b> {len(df_filtrado):,} de {len(df):,} totales
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")


    # --- 5.4 Tarjetas de KPIs ---
    kpis = calcular_kpis(df_filtrado)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Total Ventas",
            value=formatear_moneda(kpis["total_ventas"]),
            delta=None
        )

    with col2:
        st.metric(
            label="📦 Unidades Vendidas",
            value=f"{kpis['total_unidades']:,}",
            delta=None
        )

    with col3:
        st.metric(
            label="🧾 Transacciones",
            value=f"{kpis['num_transacciones']:,}",
            delta=None
        )

    with col4:
        st.metric(
            label="📈 Promedio por Venta",
            value=formatear_moneda(kpis["promedio_venta"]),
            delta=None
        )

    # Segunda fila de KPIs adicionales
    col5, col6 = st.columns(2)

    with col5:
        st.metric(
            label="🏆 Mejor Vendedor",
            value=kpis["mejor_vendedor"],
            delta=formatear_moneda(kpis["ventas_mejor"]),
            delta_color="off"
        )

    with col6:
        st.metric(
            label="⭐ Producto Top",
            value=kpis["producto_top"],
            delta=formatear_moneda(kpis["ventas_top"]),
            delta_color="off"
        )

    st.markdown("---")


    # --- 5.5 Gráficos Interactivos ---

    # Fila 1: Tendencia temporal + Distribución por región
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("📈 Tendencia de Ventas en el Tiempo")

        if len(df_filtrado) > 0:
            ventas_tiempo = df_filtrado.groupby(df_filtrado["Fecha"].dt.to_period("M"))["Total_Venta"].sum().reset_index()
            ventas_tiempo["Fecha"] = ventas_tiempo["Fecha"].dt.to_timestamp()

            fig_line = px.line(
                ventas_tiempo,
                x="Fecha",
                y="Total_Venta",
                markers=True,
                title="Ventas Mensuales",
                labels={"Total_Venta": "Ventas ($)", "Fecha": "Mes"},
                template="plotly_white"
            )
            fig_line.update_traces(line_color=COLOR_PRIMARIO, marker_size=8)
            fig_line.update_layout(hovermode="x unified")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("No hay datos para mostrar en este rango.")

    with col_graf2:
        st.subheader("🌍 Ventas por Región")

        if "Región" in df_filtrado.columns and len(df_filtrado) > 0:
            ventas_region = df_filtrado.groupby("Región")["Total_Venta"].sum().reset_index().sort_values("Total_Venta", ascending=False)

            fig_pie = px.pie(
                ventas_region,
                names="Región",
                values="Total_Venta",
                title="Distribución % por Región",
                hole=0.4,
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No hay datos de región disponibles.")


    # Fila 2: Ventas por Producto + Ventas por Vendedor
    col_graf3, col_graf4 = st.columns(2)

    with col_graf3:
        st.subheader("🛒 Ventas por Producto")

        if "Producto" in df_filtrado.columns and len(df_filtrado) > 0:
            ventas_producto = df_filtrado.groupby("Producto")["Total_Venta"].sum().reset_index().sort_values("Total_Venta", ascending=True)

            fig_bar_prod = px.bar(
                ventas_producto,
                x="Total_Venta",
                y="Producto",
                orientation="h",
                title="Top Productos por Ventas",
                labels={"Total_Venta": "Ventas ($)", "Producto": ""},
                template="plotly_white",
                color="Total_Venta",
                color_continuous_scale=["#e0e7ff", COLOR_PRIMARIO]
            )
            fig_bar_prod.update_layout(yaxis_categoryorder="total ascending")
            st.plotly_chart(fig_bar_prod, use_container_width=True)
        else:
            st.warning("No hay datos de producto disponibles.")

    with col_graf4:
        st.subheader("👤 Ventas por Vendedor")

        if "Vendedor" in df_filtrado.columns and len(df_filtrado) > 0:
            ventas_vendedor = df_filtrado.groupby("Vendedor")["Total_Venta"].sum().reset_index().sort_values("Total_Venta", ascending=False)

            fig_bar_vend = px.bar(
                ventas_vendedor,
                x="Vendedor",
                y="Total_Venta",
                title="Rendimiento por Vendedor",
                labels={"Total_Venta": "Ventas ($)", "Vendedor": ""},
                template="plotly_white",
                color="Vendedor",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_bar_vend.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar_vend, use_container_width=True)
        else:
            st.warning("No hay datos de vendedor disponibles.")


    # Fila 3: Scatter plot avanzado
    st.subheader("🔍 Análisis de Precio vs. Cantidad")

    if len(df_filtrado) > 0 and "Precio_Unitario" in df_filtrado.columns:
        fig_scatter = px.scatter(
            df_filtrado,
            x="Precio_Unitario",
            y="Cantidad",
            color="Producto" if "Producto" in df_filtrado.columns else None,
            size="Total_Venta",
            hover_data=["Vendedor", "Región", "Fecha"] if all(c in df_filtrado.columns for c in ["Vendedor", "Región", "Fecha"]) else None,
            title="Relación entre Precio Unitario y Cantidad Vendida",
            labels={"Precio_Unitario": "Precio Unitario ($)", "Cantidad": "Cantidad"},
            template="plotly_white"
        )
        fig_scatter.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color="DarkSlateGrey")))
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("El scatter plot requiere las columnas 'Precio_Unitario' y 'Cantidad'.")


    # --- 5.6 Tabla de datos con descarga ---
    st.markdown("---")
    st.subheader("📋 Detalle de Transacciones Filtradas")

    # Mostrar tabla
    st.dataframe(
        df_filtrado.sort_values("Fecha", ascending=False),
        use_container_width=True,
        height=400,
        hide_index=True
    )

    # Botón de descarga
    csv_filtrado = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar datos filtrados como CSV",
        data=csv_filtrado,
        file_name=f"ventas_filtradas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Descarga el dataset actualmente filtrado para análisis externo."
    )


    # --- 5.7 Footer profesional ---
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; color:grey; font-size:12px;">
        🛠️ Desarrollado con Python, Streamlit, Pandas y Plotly | 
        <a href="https://streamlit.io" target="_blank">Streamlit</a> 🚀
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    # Estado inicial cuando no hay datos cargados
    st.title("📊 Dashboard de Análisis de Ventas")
    st.info("👈 Selecciona una fuente de datos en la barra lateral para comenzar.")

    # Mostrar preview del dataset de ejemplo para atraer al usuario
    st.subheader("📄 Vista previa del dataset de ejemplo")
    df_preview = cargar_datos_default().head(10)
    st.dataframe(df_preview, use_container_width=True, hide_index=True)

    st.markdown("""
    ### 🚀 Características de esta app:
    - **Carga de datos**: Usa el dataset de ejemplo o sube tu propio CSV.
    - **Filtros dinámicos**: Fecha, región, producto y vendedor.
    - **KPIs en tiempo real**: Métricas clave que se actualizan automáticamente.
    - **Gráficos interactivos**: Tendencias, distribuciones y análisis de correlación.
    - **Exportación**: Descarga los datos filtrados en cualquier momento.
    """)
