import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Sunset Yachts", layout="wide")

# --- BUSCADOR DE LOGO Y DIAGNÓSTICO ---
def buscar_logo():
    files = os.listdir('.')
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg')): return f
    return None

logo = buscar_logo()
col1, col2 = st.columns([1, 4])

with col1:
    if logo:
        st.image(logo, width=150)
    else:
        st.error("⚠️ No veo el logo")
        st.info(f"Archivos en esta carpeta: {os.listdir('.')}")

with col2:
    st.title("SUNSET YACHTS GROUP")
    st.markdown("**Management System**")

st.divider()

# --- DATOS ---
FILE = 'reportes.csv'
CATS = ["Mecánica", "Electrónica", "Interiores", "Cubierta", "Limpieza", "Admin"]

def get_data():
    return pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=["Fecha", "Yate", "Cat", "Desc", "Foto"])

# --- APP ---
menu = st.sidebar.radio("Menú:", ["Registrar", "Reportes"])

if menu == "Registrar":
    st.subheader("📝 Nuevo Reporte")
    with st.form("f", clear_on_submit=True):
        yate = st.text_input("Yate")
        cat = st.selectbox("Categoría", CATS)
        desc = st.text_area("Detalles")
        foto = st.file_uploader("Foto", type=['jpg','png'])
        if st.form_submit_button("Guardar", type="primary"):
            if yate and desc:
                new = {"Fecha": datetime.now(), "Yate": yate, "Cat": cat, "Desc": desc, "Foto": foto.name if foto else ""}
                df = pd.concat([get_data(), pd.DataFrame([new])], ignore_index=True)
                df.to_csv(FILE, index=False)
                st.success("✅ Guardado")
            else: st.error("Faltan datos")

elif menu == "Reportes":
    df = get_data()
    st.dataframe(df, use_container_width=True) if not df.empty else st.info("Sin datos")
