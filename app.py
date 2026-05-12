import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Simulador Molino - 8 Cintas", layout="wide")

st.title("🏭 Control de Flujo: Sistema de 8 Cintas en Serie")

# --- CONFIGURACIÓN EN LA BARRA LATERAL ---
with st.sidebar:
    st.header("Configuración General")
    ritmo_ensacado = st.number_input("Ritmo de Ensacado (bolsas/min)", 5, 120, 30)
    peso_bolsa = st.selectbox("Peso Bolsa (kg)", [25, 50])
    
    st.divider()
    st.subheader("Velocidades de Cintas (m/s)")
    
    # Creamos un diccionario para guardar las velocidades de las 8 cintas
    vels = {}
    for i in range(1, 9):
        # Usamos expanders para no ocupar tanto espacio
        with st.expander(f"Configurar Cinta {i}"):
            vels[i] = st.slider(f"V{i}", 0.1, 2.0, 0.6, key=f"v{i}")

# --- CÁLCULOS DE ESTADO ---
st.subheader("📊 Estado de la Línea")
cols = st.columns(4) # 2 filas de 4 columnas
for i in range(1, 9):
    col_idx = (i-1) % 4
    distancia = vels[i] * (60/ritmo_ensacado)
    estado = "✅ OK" if distancia > 1.1 else "⚠️ SATURADA"
    cols[col_idx].metric(f"Cinta {i}", f"{vels[i]} m/s", estado)

# --- SIMULACIÓN DINÁMICA ---
st.divider()
contenedores = [st.empty() for _ in range(8)] # Espacios para las 8 cintas

if st.button("▶️ Arrancar Línea Completa"):
    # Inicializamos 8 arrays (cintas) de 20 espacios cada uno
    lineas = [["—"] * 20 for _ in range(8)]
    intervalo_ensacado = 60 / ritmo_ensacado
    
    for t in range(200): # Duración de la simulación
        # 1. Movimiento de atrás hacia adelante (de la cinta 8 a la 2)
        for n in range(7, 0, -1): # n va de 7 a 1 (índices de cintas)
            # Solo movemos si la velocidad lo permite en este "tick"
            if t % int(2.1 - vels[n+1]) == 0:
                transferencia = lineas[n-1][-1] # Bolsa que sale de la anterior
                lineas[n] = [transferencia] + lineas[n][:-1]
                lineas[n-1][-1] = "—" # Limpiamos la salida de la anterior

        # 2. Movimiento y Entrada en la Cinta 1
        if t % int(2.1 - vels[1]) == 0:
            lineas[0] = ["—"] + lineas[0][:-1]
            if (t * 0.1) % intervalo_ensacado < 0.1:
                lineas[0][0] = "📦"

        # 3. Renderizado de las 8 cintas
        for idx, cont in enumerate(contenedores):
            visual = "".join(lineas[idx])
            icono = "🚛" if idx == 7 else "⬇️"
            cont.code(f"CINTA {idx+1} |{visual}| {icono}")
        
        time.sleep(0.1)
