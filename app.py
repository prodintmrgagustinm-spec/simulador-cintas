import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Línea de Transporte de Bolsas", layout="wide")

st.title("🌾 Línea Continua de Transporte de Bolsas")
st.markdown("Simulación técnica de una sola línea dividida en 8 tramos de control.")

# --- BARRA LATERAL: PARÁMETROS TÉCNICOS ---
with st.sidebar:
    st.header("⚙️ Configuración Mecánica")
    rpm_motor = st.number_input("RPM Motor", value=1450)
    ritmo = st.slider("Producción (bolsas/min)", 5, 60, 15)
    
    st.divider()
    st.subheader("Parámetros por Tramo (1-8)")
    datos_cintas = {}
    for i in range(1, 9):
        with st.expander(f"Tramo {i}"):
            d = st.number_input(f"Ø Rodillo (mm) - T{i}", value=150, key=f"d{i}")
            r = st.number_input(f"Reducción (i) - T{i}", value=25.0, key=f"r{i}")
            # Velocidad real calculada
            v = (3.14159 * (d/1000) * (rpm_motor/r)) / 60
            datos_cintas[i] = {"v": v}

# --- ESTILO CSS PARA LA LÍNEA Y LA BOLSA DE MOLINO ---
st.markdown("""
    <style>
    .linea-transporte {
        background-color: #2b2b2b;
        height: 120px;
        width: 100%;
        position: relative;
        border-bottom: 10px solid #444;
        border-top: 5px solid #111;
        margin-top: 50px;
        overflow: hidden;
        display: flex;
    }
    .division {
        height: 100%;
        width: 12.5%; /* 100% / 8 tramos */
        border-right: 2px dashed #555;
        position: relative;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        color: #888;
        font-size: 10px;
        padding-bottom: 5px;
    }
    .bolsa-molino {
        width: 45px;
        height: 60px;
        background-color: #d2b48c; /* Color papel Kraft */
        border-radius: 5px 5px 2px 2px;
        position: absolute;
        bottom: 15px;
        border: 2px solid #a68966;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.3);
    }
    .bolsa-molino::before {
        content: "H"; /* Marca de harina */
        font-weight: bold;
        color: #8b4513;
        font-size: 20px;
    }
    .bolsa-molino::after {
        content: ""; /* Costura superior */
        position: absolute;
        top: 5px;
        width: 100%;
        height: 2px;
        border-top: 2px dotted #8b4513;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESPACIO DE ANIMACIÓN ---
animacion_placeholder = st.empty()

if st.button("▶️ ARRANCAR TRANSPORTE"):
    # Cada bolsa es un diccionario: {"x": posición_total_0_100}
    bolsas_en_linea = []
    intervalo_bolsa = 60 / ritmo
    ultimo_tiempo_bolsa = -intervalo_bolsa
    
    start_time = time.time()
    
    # Bucle de animación (se ejecuta mientras dure la simulación)
    for frame in range(400):
        tiempo_actual = frame * 0.1
        
        # 1. Entrada de nuevas bolsas
        if tiempo_actual - ultimo_tiempo_bolsa >= intervalo_bolsa:
            bolsas_en_linea.append({"x": 0})
            ultimo_tiempo_bolsa = tiempo_actual

        # 2. Lógica de movimiento por tramos
        # Dividimos el 100% de la línea en 8 partes de 12.5% cada una
        for bolsa in bolsas_en_linea:
            # Determinar en qué tramo está la bolsa actualmente
            tramo_actual = int(bolsa["x"] / 12.5) + 1
            tramo_actual = min(tramo_actual, 8)
            
            # Aplicar la velocidad específica de ese tramo
            v_tramo = datos_cintas[tramo_actual]["v"]
            # Factor de conversión para que el movimiento sea visible y proporcional
            bolsa["x"] += v_tramo * 0.8 

        # 3. Limpiar bolsas que salieron de la línea
        bolsas_en_linea = [b for b in bolsas_en_linea if b["x"] < 105]

        # 4. Construir el HTML de la línea completa
        html_linea = '<div class="linea-transporte">'
        # Dibujar las 8 divisiones de fondo
        for i in range(1, 9):
            html_linea += f'<div class="division">TRAMO {i}</div>'
        
        # Dibujar las bolsas encima
        for b in bolsas_en_linea:
            html_linea += f'<div class="bolsa-molino" style="left: {b["x"]}%"></div>'
        
        html_linea += '</div>'
        
        animacion_placeholder.markdown(html_linea, unsafe_allow_html=True)
        time.sleep(0.05)

    st.success("Transporte completado.")
