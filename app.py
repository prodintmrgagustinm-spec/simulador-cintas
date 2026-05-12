import streamlit as st
import time

st.set_page_config(page_title="Monitor de Producción - Molino", layout="wide")

st.title("🌾 Monitor de Flujo y Entrega de Bolsas")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración de Línea")
    rpm_motor = st.number_input("RPM Motor", value=1450)
    ritmo = st.slider("Ritmo de Ensacado (bolsas/min)", 5, 120, 30)
    
    # Cálculo de bolsas por segundo
    bolsas_seg_teorico = ritmo / 60[cite: 2]
    
    st.divider()
    st.subheader("Parámetros por Tramo")
    datos_cintas = {}
    for i in range(1, 9):
        with st.expander(f"Tramo {i}"):
            d = st.number_input(f"Ø Rodillo (mm) - T{i}", value=150, key=f"d{i}")
            r = st.number_input(f"Reducción (i) - T{i}", value=25.0, key=f"r{i}")
            v = (3.14159 * (d/1000) * (rpm_motor/r)) / 60
            datos_cintas[i] = {"v": v}

# --- PANEL DE MÉTRICAS EN VIVO ---
col1, col2, col3 = st.columns(3)
metrica_bps = col1.metric("Entrega Teórica", f"{bolsas_seg_teorico:.2f} bolsas/seg")[cite: 2]
metrica_total = col2.metric("Total Entregado", "0 bolsas")
metrica_real = col3.metric("Frecuencia Real (Salida)", "0.00 bps")

# --- ESTILO CSS (Línea y Bolsa) ---
st.markdown("""
    <style>
    .linea-transporte {
        background-color: #2b2b2b;
        height: 120px; width: 100%; position: relative;
        border-bottom: 10px solid #444; margin-top: 20px;
        overflow: hidden; display: flex;
    }
    .division {
        height: 100%; width: 12.5%; border-right: 1px dashed #555;
        display: flex; align-items: flex-end; justify-content: center;
        color: #666; font-size: 10px; padding-bottom: 5px;
    }
    .bolsa-molino {
        width: 40px; height: 55px; background-color: #d2b48c;
        border-radius: 4px; position: absolute; bottom: 15px;
        border: 2px solid #a68966; display: flex; align-items: center; justify-content: center;
    }
    .bolsa-molino::before { content: "H"; font-weight: bold; color: #8b4513; }
    </style>
""", unsafe_allow_html=True)

# --- ANIMACIÓN Y LÓGICA DE CONTEO ---
animacion_placeholder = st.empty()

if st.button("▶️ INICIAR PRODUCCIÓN"):
    bolsas_en_linea = []
    total_entregadas = 0
    intervalo_bolsa = 60 / ritmo[cite: 2]
    ultimo_tiempo_bolsa = -intervalo_bolsa
    
    start_time = time.time()
    
    for frame in range(500):
        tiempo_actual = frame * 0.1
        
        # 1. Entrada de bolsas
        if tiempo_actual - ultimo_tiempo_bolsa >= intervalo_bolsa:
            bolsas_en_linea.append({"x": 0, "entregada": False})
            ultimo_tiempo_bolsa = tiempo_actual

        # 2. Movimiento
        for b in bolsas_en_linea:
            tramo = min(int(b["x"] / 12.5) + 1, 8)
            v_tramo = datos_cintas[tramo]["v"]
            b["x"] += v_tramo * 0.8
            
            # Conteo al final de la línea (100%)
            if b["x"] >= 100 and not b["entregada"]:
                total_entregadas += 1
                b["entregada"] = True

        # 3. Limpieza y actualización de métricas
        bolsas_en_linea = [b for b in bolsas_en_linea if b["x"] < 105]
        
        # Calcular bolsas por segundo reales (Total / Tiempo transcurrido)
        bps_real = total_entregadas / max(0.1, tiempo_actual)
        
        metrica_total.metric("Total Entregado", f"{total_entregadas} bolsas")
        metrica_real.metric("Frecuencia Real (Salida)", f"{bps_real:.2f} bps")

        # 4. Renderizado
        html_linea = '<div class="linea-transporte">'
        for i in range(1, 9): html_linea += f'<div class="division">TRAMO {i}</div>'
        for b in bolsas_en_linea:
            if b["x"] <= 100:
                html_linea += f'<div class="bolsa-molino" style="left: {b["x"]}%"></div>'
        html_linea += '</div>'
        
        animacion_placeholder.markdown(html_linea, unsafe_allow_html=True)
        time.sleep(0.05)
