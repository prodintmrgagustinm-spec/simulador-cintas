import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Ingeniería de Cintas - Molino", layout="wide")

st.title("⚙️ Simulador Técnico de Transporte de Bolsas")
st.markdown("Cálculo de velocidad tangencial basado en mecánica de transmisión.")

# --- BARRA LATERAL: PARÁMETROS TÉCNICOS ---
with st.sidebar:
    st.header("Configuración de Motor")
    rpm_motor = st.number_input("RPM Nominal del Motor", value=1450)
    
    st.divider()
    st.subheader("Parámetros por Cinta")
    
    datos_cintas = {}
    for i in range(1, 9):
        with st.expander(f"Cinta {i} - Especificaciones"):
            largo = st.slider(f"Largo (m) - C{i}", 2.0, 30.0, 10.0, key=f"l{i}")
            diametro_mm = st.number_input(f"Ø Rodillo (mm) - C{i}", value=150, key=f"d{i}")
            relacion = st.number_input(f"Relación Reductor (i) - C{i}", value=20.0, key=f"r{i}")
            
            # Cálculo Físico:
            # 1. RPM Salida = RPM Motor / Relación
            rpm_salida = rpm_motor / relacion
            # 2. Velocidad (m/s) = (Pi * D * RPM) / 60
            velocidad_ms = (np.pi * (diametro_mm / 1000) * rpm_salida) / 60
            
            datos_cintas[i] = {
                "largo": largo,
                "v": velocidad_ms,
                "rpm_s": rpm_salida
            }
            st.caption(f"Velocidad Resultante: {velocidad_ms:.3f} m/s")

# --- PANEL DE DATOS TÉCNICOS ---
st.subheader("📋 Resumen de Cálculo Mecánico")
df_data = []
for i in range(1, 9):
    df_data.append({
        "Cinta": i,
        "Velocidad (m/s)": f"{datos_cintas[i]['v']:.3f}",
        "Largo (m)": datos_cintas[i]['largo'],
        "RPM Rodillo": f"{datos_cintas[i]['rpm_s']:.1f}",
        "Tiempo Tránsito (s)": f"{(datos_cintas[i]['largo'] / datos_cintas[i]['v']):.1f}"
    })
st.table(df_data)

# --- SIMULACIÓN VISUAL ---
st.subheader("🚚 Flujo de Bolsas en Tiempo Real")
ritmo = st.slider("Ritmo de Producción (bolsas/min)", 5, 60, 20)
intervalo = 60 / ritmo

contenedores = [st.empty() for _ in range(8)]

if st.button("▶️ Iniciar Simulación Física"):
    # Cada cinta tiene una resolución de 1 metro por carácter
    lineas = [["—"] * int(datos_cintas[i]['largo']) for i in range(1, 9)]
    
    for t in range(300):
        # Lógica de transferencia (de 8 a 1)
        for n in range(7, 0, -1):
            # Movemos según la velocidad calculada de cada cinta
            if t % max(1, int(1 / (datos_cintas[n+1]['v'] + 0.1))) == 0:
                trans = lineas[n-1][-1]
                lineas[n] = [trans] + lineas[n][:-1]
                lineas[n-1][-1] = "—"

        # Cinta 1 y entrada de bolsas
        if t % max(1, int(1 / (datos_cintas[1]['v'] + 0.1))) == 0:
            lineas[0] = ["—"] + lineas[0][:-1]
            if (t * 0.2) % intervalo < 0.2:
                lineas[0][0] = "📦"

        # Dibujar
        for idx, cont in enumerate(contenedores):
            visual = "".join(lineas[idx])
            cont.code(f"C{idx+1} ({datos_cintas[idx+1]['v']:.2f} m/s) |{visual}|")
        
        time.sleep(0.1)
