import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px


# Configurar el diseño de la página
st.set_page_config(layout="wide")

# Cargar los datos
ventas_full = pd.read_csv("ventas_full.csv")

# Convertir la columna 'Fecha' al tipo de dato de fecha de pandas
ventas_full['Fecha'] = pd.to_datetime(ventas_full['Fecha'], format='%Y-%m-%d')

# Calcular las ventas totales por año
ventas_por_anio = ventas_full.groupby(ventas_full['Fecha'].dt.year)['Ventas'].sum()

# Crear un DataFrame para Altair
ventas_por_anio_df = ventas_por_anio.reset_index()
ventas_por_anio_df.columns = ['Año', 'Ventas Totales']


# Crear el gráfico
st.title('Reporte para Automotors: Servicio Automotriz')

# Agregar imagen PNG debajo del título
st.image('logo.png')
# Agregar imagen PNG debajo del título centrada horizontalmente
# Párrafo justificado
st.markdown("""
            <p style='text-align: justify;'>Automotors ofrece servicios automotrices, 
            así como venta de llantas y accesorios para automóviles. Para consultar cómo se hizo la limpieza de los datos, puedes consultar 
            <a href="https://github.com/robertbarac/Automotors_Report/blob/main/limpieza.ipynb">aquí</a>.</p>
            """, unsafe_allow_html=True)




# Crear las pestañas laterales
tabs = ["Vendedores", "Sedes", "Productos", "Ventas"]
selected_tab = st.sidebar.radio("Selecciona una pestaña:", tabs)

# Mostrar el contenido de la pestaña seleccionada
if selected_tab == "Vendedores":
    st.subheader("Vendedores", divider='rainbow')
    # Aquí puedes agregar el contenido específico para la pestaña de vendedores
    
    # Filtrar por sede
    sede_filtro = st.selectbox("Selecciona la sede:", ["Todas"] + list(ventas_full['Sede'].unique()))

    # Filtrar los datos según la sede seleccionada
    if sede_filtro == "Todas":
        ventas_filtradas = ventas_full
    else:
        ventas_filtradas = ventas_full[ventas_full['Sede'] == sede_filtro]

    # Gráfica de los 10 vendedores que más venden en cantidad de ventas
    vendedores_mas_vendidos_cantidad = ventas_filtradas.groupby('Id_Empleado')['Cantidad'].sum().reset_index().sort_values(by='Cantidad', ascending=False).head(10)
    fig_mas_vendidos_cantidad = px.bar(vendedores_mas_vendidos_cantidad, x='Id_Empleado', y='Cantidad', title=f'Top 10 Vendedores Más Vendidos por Cantidad - {sede_filtro}', color='Id_Empleado')
    st.plotly_chart(fig_mas_vendidos_cantidad, use_container_width=True)

    # Gráfica de los 10 vendedores que más venden en términos monetarios
    vendedores_mas_vendidos_ingresos = ventas_filtradas.groupby('Id_Empleado')['Ventas'].sum().reset_index().sort_values(by='Ventas', ascending=False).head(10)
    fig_mas_vendidos_ingresos = px.bar(vendedores_mas_vendidos_ingresos, x='Id_Empleado', y='Ventas', title=f'Top 10 Vendedores Más Vendidos por Ingresos - {sede_filtro}', color='Id_Empleado')
    st.plotly_chart(fig_mas_vendidos_ingresos, use_container_width=True)


    
elif selected_tab == "Sedes":
    st.subheader("Sedes", divider='rainbow')
    # Aquí puedes agregar el contenido específico para la pestaña de sedes
    # Sedes disponibles
    sedes_disponibles = ventas_full['Sede'].unique()
    st.write("Sedes disponibles:", sedes_disponibles)
    
    # Ventas totales de sedes sectorizadas por año
    st.subheader("Ventas totales de sedes por año")
    
    # Crear un desplegable para seleccionar el año
    year_options = ['Total', '2016', '2017', '2018', '2019', '2020']
    selected_year = st.selectbox("Selecciona un año:", year_options)
    
    # Filtrar los datos según el año seleccionado
    if selected_year == 'Total':
        ventas_por_sede = ventas_full.groupby('Sede')['Ventas'].sum().reset_index()
    else:
        year = int(selected_year)
        ventas_por_sede = ventas_full[ventas_full['Fecha'].dt.year == year].groupby('Sede')['Ventas'].sum().reset_index()
    
    # Graficar las ventas totales de sedes
    fig = px.bar(ventas_por_sede, x='Sede', y='Ventas', title='Ventas totales por sede', color='Sede')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    
elif selected_tab == "Productos":
    st.subheader("Productos", divider='rainbow')
    # Aquí puedes agregar el contenido específico para la pestaña de productos

    # Filtrar por tipo de sede
    tipo_sede = st.selectbox("Selecciona el tipo de sede:", ["Todas"] + list(ventas_full['Sede'].unique()))

    # Filtrar los datos según el tipo de sede seleccionado
    if tipo_sede == "Todas":
        ventas_filtradas = ventas_full
    else:
        ventas_filtradas = ventas_full[ventas_full['Sede'] == tipo_sede]

    # Gráfica de los 10 productos más vendidos
    productos_mas_vendidos = ventas_filtradas.groupby('Productos')['Cantidad'].sum().reset_index().sort_values(by='Cantidad', ascending=False).head(10)
    fig_mas_vendidos = px.bar(productos_mas_vendidos, x='Productos', y='Cantidad', title=f'Top 10 Productos/Servicios Más Vendidos - {tipo_sede}', color='Productos')
    st.plotly_chart(fig_mas_vendidos, theme="streamlit", use_container_width=True)

    # Gráfica de los 10 productos que más ingresos generan
    productos_mas_ventas = ventas_filtradas.groupby('Productos')['Ventas'].sum().reset_index().sort_values(by='Ventas', ascending=False).head(10)
    fig_mas_ventas = px.bar(productos_mas_ventas, x='Productos', y='Ventas', title=f'Top 10 Productos/Servicios con Mayor Ingreso - {tipo_sede}', color='Productos')
    st.plotly_chart(fig_mas_ventas, theme="streamlit", use_container_width=True)

    
elif selected_tab == "Ventas":
    st.subheader("Ventas", divider='rainbow')
    # Aquí puedes agregar el contenido específico para la pestaña de ventas
    
    # Calcular la venta total por año
    venta_total_por_año = ventas_full.groupby(ventas_full['Fecha'].dt.year)['Ventas'].sum().reset_index()
    
    # Graficar la venta total por año con colores diferentes para cada barra y estilo personalizado
    fig = px.bar(venta_total_por_año, x='Fecha', y='Ventas', title='Venta total por año', color='Fecha')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)



# streamlit run main.py --server.runOnSave true