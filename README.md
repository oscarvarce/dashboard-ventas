# 📊 Dashboard de Análisis de Ventas

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-ff4b4b)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3f4f75)](https://plotly.com/python/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Aplicación web interactiva** para el análisis exploratorio de datos de ventas. Permite cargar datasets propios o usar datos de demostración, aplicar filtros dinámicos, visualizar KPIs en tiempo real y generar gráficos interactivos con Plotly.

---

## 🚀 Demo en vivo

🔗 **[Ver aplicación desplegada en Streamlit Cloud](https://tu-app.streamlit.app)** *(reemplaza con tu URL)*

---

## ✨ Características

| Funcionalidad | Descripción |
|---------------|-------------|
| 📁 **Carga de datos** | Dataset de ejemplo incluido o sube tu propio CSV |
| 🔍 **Filtros dinámicos** | Rango de fechas, región, producto y vendedor en sidebar |
| 📈 **KPIs en tiempo real** | Total ventas, unidades, transacciones, promedio, mejor vendedor y producto top |
| 📊 **Gráficos interactivos** | Tendencias temporales, pie chart, barras horizontales/verticales, scatter plot |
| 📋 **Tabla de datos** | Vista detallada con scroll y ordenamiento |
| ⬇️ **Exportación** | Descarga el dataset filtrado como CSV en cualquier momento |
| ⚡ **Alto rendimiento** | Uso de `@st.cache_data` para evitar recargas innecesarias |

---

## 🛠️ Tecnologías

- **Python** 3.9+
- **Streamlit** - Framework para apps web de datos
- **Pandas** - Manipulación y análisis de datos
- **Plotly** - Visualizaciones interactivas
- **NumPy** - Operaciones numéricas

---

## 📁 Estructura del Repositorio

```
📦 dashboard-ventas/
├── 📄 main.py                  # Aplicación principal (Streamlit)
├── 📄 requirements.txt         # Dependencias del proyecto
├── 📄 ventas_ejemplo.csv       # Dataset de demostración
├── 📄 README.md                # Documentación del proyecto
├── 📄 LICENSE                  # Licencia MIT (opcional)
├── 📁 assets/                  # Imágenes, logos, etc. (opcional)
└── 📁 .streamlit/
    └── config.toml             # Configuración personalizada de Streamlit (opcional)
```

---

## ⚙️ Instalación y Uso Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/dashboard-ventas.git
cd dashboard-ventas
```

### 2. Crear entorno virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
streamlit run main.py
```

La app se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 🌐 Despliegue en Streamlit Cloud (Gratis)

1. **Sube el código a GitHub**
   - Crea un repositorio nuevo en GitHub
   - Sube todos los archivos (`main.py`, `requirements.txt`, `ventas_ejemplo.csv`, `README.md`)
   - Asegúrate de que `main.py` esté en la raíz del repositorio

2. **Conectar con Streamlit Cloud**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Inicia sesión con tu cuenta de GitHub
   - Haz clic en **"New app"**
   - Selecciona tu repositorio, rama (`main` o `master`) y archivo principal (`main.py`)
   - Haz clic en **"Deploy"** 🚀

3. **Configuración adicional (opcional)**
   - Ve a **Settings → Secrets** si necesitas variables de entorno
   - Personaliza la URL de tu app en los ajustes

> 💡 **Tip:** Streamlit Cloud se actualiza automáticamente cada vez que haces `git push` a tu repositorio.

---

## 📊 Formato esperado del CSV

Si deseas usar tu propio archivo, asegúrate de que contenga al menos estas columnas:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `Fecha` | `datetime` o `date` | Fecha de la transacción |
| `Producto` | `string` | Nombre del producto |
| `Cantidad` | `int` | Unidades vendidas |
| `Total_Venta` | `float` | Monto total de la venta |
| `Región` *(opcional)* | `string` | Región geográfica |
| `Vendedor` *(opcional)* | `string` | Nombre del vendedor |
| `Precio_Unitario` *(opcional)* | `float` | Para el scatter plot |

---

## 🧑‍💻 Autor

**[Tu Nombre]** - *Data Analyst / Python Developer*

- 🐦 Twitter: [@tu_usuario](https://twitter.com/tu_usuario)
- 💼 LinkedIn: [linkedin.com/in/tu-usuario](https://linkedin.com/in/tu-usuario)
- 📧 Email: tu.email@ejemplo.com

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

<p align="center">
  ⭐ Si te gustó este proyecto, ¡dale una estrella en GitHub!
</p>
