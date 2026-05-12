import streamlit as st
import time

st.set_page_config(page_title="Monitor de Producción - Molino", layout="wide")

st.title("🌾 Monitor de Flujo con Tramos Variables")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración de Línea")
    rpm_motor = st.number_input("RPM Motor", value=1450)
    ritmo = st.slider("Ritmo de Ensacado (bolsas/min)", 5, 120, 30)
    
    st.divider()
    st.subheader("Parámetros por Tramo")
    datos_tramos = {}
    largo_total_linea = 0
    
    for i in range(1, 9):
        with st.expander(f"Tramo {i}"):
            # Configuración de largo, diámetro y reducción
            largo = st.slider(f"Largo (m) - T{i}", 1.0, 20.0, 5.0, key=f"l{i}")
            d = st.number_input(f"Ø Rodillo (mm) - T{i}", value=150, key=f"d{i}")
            r = st.number_input(f"Reducción (i) - T{i}", value=25.0, key=f"r{i}")
            
            # Cálculo de velocidad real (m/s)
            v = (3.14159 * (d/1000) * (rpm_motor/r)) / 60
            datos_tramos[i] = {"v": v, "largo": largo}
            largo_total_linea += largo

# --- PANEL DE MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("Largo Total de Línea", f"{largo_total_linea:.1f} m")
metrica_total = col2.metric("Total Entregado", "0 bolsas")
metrica_real = col3.metric("Frecuencia Real", "0.00 bps")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .linea-transporte {
        background-color: #2b2b2b;
        height: 120px; width: 100%; position: relative;
        border-bottom: 10px solid #444; margin-top: 20px;
        overflow: hidden; display: flex;
    }
    .division {
        height: 100%; border-right: 1px dashed #555;
        display: flex; align-items: flex-end; justify-content: center;
        color: #666; font-size: 9px; padding-bottom: 5px;
    }
    .bolsa-molino {
        width: 35px; height: 50px; background-color: #d2b48c;
        border-radius: 4px; position: absolute; bottom: 15px;
        border: 2px solid #a68966; display: flex; align-items: center; justify-content: center;
    }
    .bolsa-molino::before { content: "H"; font-weight: bold; color: #8b4513; }
    </style>
""", unsafe_allow_html=True)

# --- ANIMACIÓN Y LÓGICA ---
animacion_placeholder = st.empty()

if st.button("▶️ INICIAR PRODUCCIÓN"):
    bolsas_en_linea = []
    total_entregadas = 0
    intervalo_bolsa = 60 / ritmo
    ultimo_tiempo_bolsa = -intervalo_bolsa
    
    start_time = time.time()
    
    # Simulación
    for frame in range(1000):
        tiempo_actual = frame * 0.1
        
        # 1. Entrada de bolsas
        if tiempo_actual - ultimo_tiempo_bolsa >= intervalo_bolsa:
            bolsas_en_linea.append({"dist_recorrida": 0, "entregada": False})
            ultimo_tiempo_bolsa = tiempo_actual

        # 2. Movimiento físico real
        for b in bolsas_en_linea:
            dist_acum = 0
            tramo_actual = 8
            for i in range(1, 9):
                dist_acum += datos_tramos[i]["largo"]
                if b["dist_recorrida"] <= dist_acum:
                    tramo_actual = i
                    break
            
            v_tramo = datos_tramos[tramo_actual]["v"]
            b["dist_recorrida"] += v_tramo * 0.1
            
            if b["dist_recorrida"] >= largo_total_linea and not b["entregada"]:
                total_entregadas += 1
                b["entregada"] = True

        # 3. Limpieza y métricas
        bolsas_en_linea = [b for b in bolsas_en_linea if b["dist_recorrida"] < largo_total_linea + 2]
        bps_real = total_entregadas / max(0.1, tiempo_actual)
        
        metrica_total.metric("Total Entregado", f"{total_entregadas} bolsas")
        metrica_real.metric("Frecuencia Real", f"{bps_real:.2f} bps")

        # 4. Renderizado HTML
        html_linea = '<div class="linea-transporte">'
        for i in range(1, 9):
            ancho_rel = (datos_tramos[i]["largo"] / largo_total_linea) * 100
            html_linea += f'<div class="division" style="width: {ancho_rel}%">T{i} ({datos_tramos[i]["largo"]}m)</div>'
        
        for b in bolsas_en_linea:
            pos_vis = (b["dist_recorrida"] / largo_total_linea) * 100
            if pos_vis <= 100:
                html_linea += f'<div class="bolsa-molino" style="left: {pos_vis}%"></div>'
        
        html_linea += '</div>'
        
        animacion_placeholder.markdown(html_linea, unsafe_allow_html=True)
        time.sleep(0.05)
