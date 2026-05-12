import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Animación Línea de Ensacado", layout="wide")

st.title("🏭 Simulador Animado de Molino: 8 Cintas")

# --- BARRA LATERAL: PARÁMETROS TÉCNICOS ---
with st.sidebar:
    st.header("⚙️ Configuración Mecánica")
    rpm_motor = st.number_input("RPM Motor", value=1450)
    ritmo = st.slider("Producción (bolsas/min)", 5, 60, 20)
    
    st.divider()
    datos_cintas = {}
    for i in range(1, 9):
        with st.expander(f"Cinta {i}"):
            d = st.number_input(f"Ø Rodillo (mm) - C{i}", value=150, key=f"d{i}")
            r = st.number_input(f"Reducción (i) - C{i}", value=20.0, key=f"r{i}")
            largo = st.slider(f"Largo (m) - C{i}", 2, 15, 8, key=f"l{i}")
            
            # Cálculo de velocidad real
            v = (3.14159 * (d/1000) * (rpm_motor/r)) / 60
            datos_cintas[i] = {"v": v, "largo": largo}

# --- ESTILO CSS PARA LAS BOLSAS ---
st.markdown("""
    <style>
    .cinta-container {
        background-color: #333;
        border-radius: 5px;
        margin-bottom: 10px;
        padding: 5px;
        position: relative;
        height: 45px;
        display: flex;
        align-items: center;
        overflow: hidden;
        border: 2px solid #555;
    }
    .bolsa {
        font-size: 25px;
        position: absolute;
        transition: left 0.1s linear;
    }
    .etiqueta-cinta {
        color: white;
        font-family: monospace;
        font-weight: bold;
        margin-right: 15px;
        z-index: 10;
        background: #222;
        padding: 2px 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESPACIO DE ANIMACIÓN ---
st.subheader("Simulación en Vivo")
if st.button("▶️ INICIAR PROCESO DE ENSACADO"):
    # Estado de las bolsas: cada elemento es [pos_x_pixel, cinta_actual]
    bolsas_activas = []
    frames = 150 # Duración de la simulación
    intervalo_bolsa = 60 / ritmo
    ultimo_tiempo_bolsa = 0
    
    # Placeholders para las 8 cintas
    slots = [st.empty() for _ in range(8)]
    
    # Bucle de animación
    for t in range(frames):
        # 1. Generar nueva bolsa en Cinta 1
        tiempo_actual = t * 0.2
        if tiempo_actual - ultimo_tiempo_bolsa >= intervalo_bolsa:
            bolsas_activas.append({"x": 0, "cinta": 1})
            ultimo_tiempo_bolsa = tiempo_actual

        # 2. Actualizar posiciones
        for b in bolsas_activas:
            c_idx = b["cinta"]
            v_cinta = datos_cintas[c_idx]["v"]
            # Movimiento: velocidad * factor de escala para píxeles
            b["x"] += v_cinta * 15 
            
            # Transferencia a la siguiente cinta
            if b["x"] > 90: # Si llega al final (90% del ancho)
                if c_idx < 8:
                    b["cinta"] += 1
                    b["x"] = 0 # Reinicia al inicio de la siguiente cinta
                else:
                    b["x"] = 200 # Sacar de pantalla (bolsa entregada)

        # 3. Dibujar las 8 cintas
        for i in range(1, 9):
            html_cinta = f'<div class="cinta-container"><span class="etiqueta-cinta">CINTA {i} ({datos_cintas[i]["v"]:.2f} m/s)</span>'
            for b in bolsas_activas:
                if b["cinta"] == i and b["x"] <= 100:
                    html_cinta += f'<div class="bolsa" style="left: {b["x"]}%">📦</div>'
            html_cinta += '</div>'
            slots[i-1].markdown(html_cinta, unsafe_allow_html=True)
            
        time.sleep(0.1)

    st.success("Simulación finalizada.")
