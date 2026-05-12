import streamlit as st
import time
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Simulador de Molino - Ensacado", layout="wide")

st.title("🌾 Simulador de Cinta Transportadora de Bolsas")
st.markdown("Control de flujo y logística para líneas de ensacado de harina/granos.")

# --- BARRA LATERAL ---
st.sidebar.header("Configuración")
with st.sidebar:
    largo_cinta = st.slider("Longitud de la cinta (m)", 5, 50, 15)
    v_cinta = st.slider("Velocidad (m/s)", 0.1, 2.0, 0.5)
    bolsas_por_minuto = st.number_input("Ritmo de Ensacado (bolsas/min)", 5, 100, 20)
    peso_bolsa = st.selectbox("Peso Bolsa (kg)", [25, 50])

# --- CÁLCULOS ---
intervalo_segundos = 60 / bolsas_por_minuto
distancia_entre_bolsas = v_cinta * intervalo_segundos
carga_lineal = peso_bolsa / max(0.1, distancia_entre_bolsas)

# --- MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("Distancia entre bolsas", f"{distancia_entre_bolsas:.2f} m")
col2.metric("Carga Lineal", f"{carga_lineal:.1f} kg/m")

if distancia_entre_bolsas < 1.0:
    col3.error("⚠️ Riesgo de Atasco")
else:
    col3.success("✅ Flujo Seguro")

# --- SIMULACIÓN ---
st.subheader("Visualización de la Línea")
placeholder = st.empty()

if st.button("Iniciar Cinta"):
    # Representación simple de la cinta
    ancho_visual = 40
    cinta = ["—"] * ancho_visual
    
    for i in range(100):
        # Mover cinta
        cinta = ["—"] + cinta[:-1]
        
        # Nueva bolsa según el ritmo
        if (i * 0.2) % intervalo_segundos < 0.2:
            cinta[0] = "📦"
            
        linea_visual = "".join(cinta)
        placeholder.code(f"INICIO |{linea_visual}| FIN")
        time.sleep(0.1)

st.info("Sube estos archivos a tu repositorio de GitHub para activarlo en Streamlit Cloud.")
