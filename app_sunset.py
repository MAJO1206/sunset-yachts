import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sunset Yachts", page_icon="⚓", layout="wide")

# --- FUNCIONES ---
FILE = 'reportes.csv'
CATS = ["Mecánica", "Electrónica", "Interiores", "Cubierta", "Limpieza", "Admin"]

def get_data():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=["Fecha", "Yate", "Cat", "Desc", "Foto"])

# --- INTERFAZ PRINCIPAL ---
# Intentar mostrar logo, si no hay, mostrar texto
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=250)
else:
    st.title("SUNSET YACHTS GROUP")

st.markdown("---")

# Menú lateral
menu = st.sidebar.radio("Menú:", ["Registrar", "Reportes"])

if menu == "Registrar":
    st.subheader("📝 Nuevo Reporte")
    with st.form("formulario_reporte", clear_on_submit=True):
        yate = st.text_input("Nombre del Yate")
        cat = st.selectbox("Categoría", CATS)
        desc = st.text_area("Detalles del trabajo")
        foto = st.file_uploader("Foto evidencia", type=['jpg','png', 'jpeg'])
        
        guardar = st.form_submit_button("Guardar Reporte", type="primary")
        
        if guardar:
            if yate and desc:
                # Crear el registro
                new_data = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Yate": yate,
                    "Cat": cat,
                    "Desc": desc,
                    "Foto": foto.name if foto else "Sin foto"
                }
                # Guardar en CSV
                df = get_data()
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv(FILE, index=False)
                st.success("✅ ¡Reporte guardado exitosamente!")
            else:
                st.error("⚠️ Faltan datos: Por favor escribe el nombre del Yate y los Detalles.")

elif menu == "Reportes":
    st.subheader("📊 Historial de Mantenimiento")
    df = get_data()
    
    if not df.empty:
        # Ordenar: Lo más nuevo primero
        df = df.sort_values(by="Fecha", ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("📭 No hay reportes registrados todavía.")
