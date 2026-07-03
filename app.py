import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64
from io import BytesIO

st.set_page_config(page_title="Perfil Dermatológico · Recomendador",
                   page_icon="🌸", layout="centered")

# ─────────────────────────────────────────────────────────────
# BANNER SUPERIOR (imagen Skincare.png del repositorio)
# ─────────────────────────────────────────────────────────────
def mostrar_banner(ruta="Skincare.png"):
    if os.path.exists(ruta):
        with open(ruta, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="width:100%;margin:-1rem 0 1.2rem 0;">
            <img src="data:image/png;base64,{data}"
                 style="width:100%;border-radius:18px;
                        box-shadow:0 8px 30px rgba(0,0,0,0.3);display:block;">
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PALETA Y TIPOGRAFÍA (borgoña · rosa · blanco)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@300;400;500&display=swap');

.stApp {
    background: linear-gradient(180deg, #6F0303 0%, #6F0303 35%, #8B2838 65%, #C97B8E 100%);
    background-attachment: fixed;
}
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
    color: #FBEDF0; font-weight: 300; letter-spacing: 0.02em;
}
/* Forzar legibilidad de TODO el texto sobre el fondo rojo */
.stApp, .stApp p, .stApp span, .stApp label, .stApp li,
.stMarkdown, [data-testid="stMarkdownContainer"] p {
    color: #FBEDF0 !important;
}
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #FBEDF0 !important; font-weight: 500 !important;
}
h1 { font-size: 2.9rem !important; line-height: 1.1; }
h2 { font-size: 2.0rem !important; }
h3 { font-size: 1.5rem !important; }
.eyebrow {
    font-family: 'Jost', sans-serif; font-size: 0.72rem;
    letter-spacing: 0.32em; text-transform: uppercase;
    color: #E8A0B4; font-weight: 400; margin-bottom: 0.2rem;
}
.card-eje {
    border-radius: 18px; padding: 1.4rem 1.6rem; margin-bottom: 1.1rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.22);
}
.eje-1 { background: #FFFFFF; color: #5C1526; }
.eje-2 { background: #FCE4EC; color: #6A1730; }
.eje-3 { background: #F9D2DE; color: #6A1730; }
.eje-4 { background: #F5BFD0; color: #5C1526; }
.card-eje h4 {
    font-family: 'Cormorant Garamond', serif; font-size: 1.35rem;
    margin: 0 0 0.3rem 0; font-weight: 600;
}
.card-eje p { margin: 0; font-size: 0.94rem; line-height: 1.5; }
/* Texto oscuro dentro de tarjetas (cubre h4, p y div para ganar al global) */
div.card-eje.eje-1, div.card-eje.eje-1 h4, div.card-eje.eje-1 p, div.card-eje.eje-1 div,
[data-testid="stMarkdownContainer"] .eje-1 div { color: #5C1526 !important; }
div.card-eje.eje-2, div.card-eje.eje-2 h4, div.card-eje.eje-2 p, div.card-eje.eje-2 div,
[data-testid="stMarkdownContainer"] .eje-2 div { color: #6A1730 !important; }
div.card-eje.eje-3, div.card-eje.eje-3 h4, div.card-eje.eje-3 p, div.card-eje.eje-3 div,
[data-testid="stMarkdownContainer"] .eje-3 div { color: #6A1730 !important; }
div.card-eje.eje-4, div.card-eje.eje-4 h4, div.card-eje.eje-4 p, div.card-eje.eje-4 div,
[data-testid="stMarkdownContainer"] .eje-4 div { color: #5C1526 !important; }

/* Expander "¿Por qué?" con borde brillante rosa (igual que el botón) */
div[data-testid="stExpander"] {
    border: 1.5px solid #E8A0B4 !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.06) !important;
    box-shadow: 0 0 12px rgba(232,160,180,0.35);
    overflow: hidden;
    margin-bottom: 0.6rem;
}
div[data-testid="stExpander"] summary {
    color: #F5BFD0 !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em;
}
div[data-testid="stExpander"] summary:hover {
    color: #FBEDF0 !important;
}
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] [data-testid="stCaptionContainer"] p {
    color: #FBEDF0 !important;
    font-style: italic;
    font-size: 0.82rem;
}
.stSelectbox label, .stRadio label {
    color: #FBEDF0 !important; font-weight: 400; font-size: 0.95rem;
}
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.94); border: none;
    border-radius: 10px; color: #4A0E1F;
}
.stButton > button {
    background: #E8A0B4; color: #4A0E1F; border: none; border-radius: 30px;
    padding: 0.8rem 2.2rem; font-family: 'Jost', sans-serif; font-weight: 500;
    letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.85rem;
    transition: all 0.25s ease;
    box-shadow: 0 0 0 rgba(232,160,180,0.6);
    animation: pulso 2.4s ease-in-out infinite;
}
.stButton > button:hover {
    background: #F5BFD0; color: #3D0A18; transform: translateY(-2px);
    box-shadow: 0 6px 26px rgba(245,191,208,0.7);
    animation: none;
}
@keyframes pulso {
    0%   { box-shadow: 0 0 0 0 rgba(232,160,180,0.55); }
    70%  { box-shadow: 0 0 0 14px rgba(232,160,180,0); }
    100% { box-shadow: 0 0 0 0 rgba(232,160,180,0); }
}
/* Botón de descarga PDF con mismo efecto brillante */
.stDownloadButton > button {
    background: #E8A0B4 !important; color: #4A0E1F !important; border: none !important;
    border-radius: 30px !important; padding: 0.8rem 2.2rem !important;
    font-family: 'Jost', sans-serif !important; font-weight: 500 !important;
    letter-spacing: 0.14em !important; text-transform: uppercase !important;
    font-size: 0.85rem !important; transition: all 0.25s ease !important;
    animation: pulso 2.4s ease-in-out infinite;
}
.stDownloadButton > button:hover {
    background: #F5BFD0 !important; color: #3D0A18 !important;
    transform: translateY(-2px); box-shadow: 0 6px 26px rgba(245,191,208,0.7) !important;
    animation: none;
}
hr { border-color: rgba(232,160,180,0.25) !important; }
.axis-track {
    position: relative; height: 8px; border-radius: 10px;
    background: linear-gradient(90deg, rgba(255,255,255,0.35), rgba(255,255,255,0.7));
    margin: 0.5rem 0 0.2rem 0;
}
.axis-marker {
    position: absolute; top: -5px; width: 18px; height: 18px; border-radius: 50%;
    background: #5C1526; border: 3px solid #FFFFFF;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3); transform: translateX(-50%);
}
.axis-ends { display: flex; justify-content: space-between; margin-top: 0.1rem; }
.rutina-box {
    border-radius: 16px; padding: 1.3rem 1.4rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.22);
}
.rutina-am { background: #FFFFFF; }
.rutina-pm { background: #FCE4EC; }
.rutina-box h3 { color: #5C1526 !important; margin-top: 0; }
.rutina-box, .rutina-box p, .rutina-box span { color: #5C1526 !important; }
.paso-num { font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 1.05rem; }
.stAlert {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(232,160,180,0.5) !important;
    border-radius: 12px;
}
.stAlert, .stAlert p, .stAlert div, .stAlert span,
[data-testid="stAlert"], [data-testid="stAlert"] p {
    color: #FBEDF0 !important;
}
.chip {
    display: inline-block; padding: 0.15rem 0.7rem; border-radius: 20px;
    font-size: 0.72rem; font-weight: 500; letter-spacing: 0.05em;
}
.chip-alta { background: #2E7D5B; color: #EAFBF2; }
.chip-media { background: #C9A227; color: #3A2E00; }
.chip-baja { background: #B5654D; color: #FFF0EA; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CARGA DE ARTEFACTOS
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def cargar_artefactos():
    return (joblib.load('modelo_ganador.pkl'),
            joblib.load('encoders.pkl'),
            joblib.load('feature_names.pkl'),
            joblib.load('mapas_scoring.pkl'),
            joblib.load('xgb_remaps.pkl'))

modelo, encoders, feature_names, mapas_scoring, xgb_remaps = cargar_artefactos()
CATEGORIAS = ['limpiador', 'exfoliante', 'mascarilla', 'toner', 'serum', 'hidratante', 'spf']

NOMBRES_LEGIBLES = {
    'limpiador': {'gel_salicilico': 'Gel limpiador con ácido salicílico',
                  'syndet_espuma': 'Espuma limpiadora syndet',
                  'syndet_sin_fragancia': 'Limpiador syndet sin fragancia',
                  'crema_no_espumoso': 'Limpiador en crema (no espumoso)'},
    'exfoliante': {'bha_salicilico': 'Exfoliante BHA (ácido salicílico)',
                   'aha_glicolico': 'Exfoliante AHA (ácido glicólico)',
                   'aha_lactico_suave': 'Exfoliante AHA suave (ácido láctico)',
                   'minimo': 'Exfoliación mínima (1 vez/semana)',
                   'ninguno': 'Sin exfoliante'},
    'mascarilla': {'arcilla': 'Mascarilla de arcilla', 'calmante': 'Mascarilla calmante',
                   'nutritiva': 'Mascarilla nutritiva', 'despigmentante': 'Mascarilla despigmentante',
                   'antioxidante': 'Mascarilla antioxidante'},
    'toner': {'niacinamida_te_verde': 'Tónico con niacinamida y té verde',
              'vitamina_c_kojico': 'Tónico con vitamina C y ácido kójico',
              'antioxidante': 'Tónico antioxidante',
              'no_recomendado': 'Tónico no recomendado para tu piel'},
    'serum': {'niacinamida': 'Sérum de niacinamida', 'vitamina_c': 'Sérum de vitamina C',
              'antiinflamatorio': 'Sérum antiinflamatorio', 'retinoide': 'Sérum con retinoide',
              'peptidos': 'Sérum de péptidos',
              'combinado_am_pm': 'Sérum combinado (vitamina C día / retinoide noche)'},
    'hidratante': {'gel_oil_free': 'Hidratante en gel oil-free', 'locion_ligera': 'Loción hidratante ligera',
                   'crema_ceramidas': 'Crema con ceramidas', 'crema_rica': 'Crema rica y nutritiva',
                   'locion_despigmentante': 'Loción hidratante despigmentante',
                   'crema_ceramidas_despig': 'Crema con ceramidas y activos despigmentantes'},
    'spf': {'estandar': 'Protector solar estándar SPF 50',
            'fisico_zno': 'Protector solar físico (óxido de zinc)',
            'amplio_espectro_obligatorio': 'Protector solar amplio espectro SPF 50+'}
}

EXPLICACION_PRODUCTO = {
    'gel_salicilico': 'El ácido salicílico es un beta-hidroxiácido liposoluble que penetra dentro del '
                      'poro y disuelve el sebo acumulado. En pieles grasas reduce la congestión, '
                      'controla el brillo y previene la aparición de brotes.',
    'syndet_espuma': 'Un limpiador syndet (detergente sintético) respeta el pH natural de la piel '
                     'mientras arrastra el exceso de grasa, evitando el efecto de tirantez que dejan '
                     'los jabones tradicionales.',
    'syndet_sin_fragancia': 'Al ser un detergente sintético sin fragancia, limpia sin alterar la '
                            'barrera cutánea ni introducir posibles irritantes, algo clave en pieles '
                            'sensibles que reaccionan con facilidad.',
    'crema_no_espumoso': 'La textura en crema limpia mediante emolientes en lugar de tensioactivos '
                         'fuertes, retirando impurezas sin eliminar los lípidos naturales que una '
                         'piel seca necesita conservar.',
    'bha_salicilico': 'El BHA (ácido salicílico) es liposoluble, por lo que penetra el poro obstruido '
                      'y lo desincrusta desde dentro, ideal cuando hay tendencia a puntos negros y '
                      'congestión.',
    'aha_glicolico': 'El ácido glicólico es el AHA de molécula más pequeña, penetra rápido y renueva '
                     'la capa superficial. En pieles resistentes mejora la textura y la luminosidad '
                     'sin apenas riesgo de irritación.',
    'aha_lactico_suave': 'El ácido láctico es un AHA de mayor tamaño molecular que exfolia con '
                         'suavidad mientras retiene agua en la piel, aportando exfoliación e '
                         'hidratación a la vez.',
    'minimo': 'En pieles sensibles se limita la exfoliación a una vez por semana o menos, para renovar '
              'la piel sin desencadenar enrojecimiento ni comprometer la barrera cutánea.',
    'ninguno': 'Según tu perfil, tu piel no requiere exfoliación adicional; añadirla podría alterar su '
               'equilibrio sin aportar beneficio.',
    'arcilla': 'La arcilla actúa por absorción: capta el exceso de sebo e impurezas de la superficie. '
               'Usada una o dos veces por semana, mantiene los poros despejados en pieles grasas.',
    'calmante': 'Una mascarilla calmante, con ingredientes como avena o centella asiática, reduce la '
                'reactividad y el enrojecimiento propios de la piel sensible.',
    'despigmentante': 'Concentra activos que inhiben la producción de melanina, atenuando de forma '
                      'progresiva las manchas en pieles con tendencia a pigmentarse.',
    'antioxidante': 'Los antioxidantes neutralizan los radicales libres generados por el sol y la '
                    'contaminación, principales responsables del envejecimiento prematuro de la piel.',
    'nutritiva': 'Aporta lípidos y agentes emolientes que devuelven confort y flexibilidad a las '
                 'pieles secas que han perdido componentes de su barrera.',
    'niacinamida_te_verde': 'La niacinamida regula la producción de sebo y refuerza la barrera, y el '
                            'té verde suma acción antioxidante y calmante. Juntos preparan la piel '
                            'grasa antes del sérum sin engrasarla.',
    'vitamina_c_kojico': 'La vitamina C ilumina y el ácido kójico inhibe la enzima que produce melanina. '
                         'Este tónico prepara la piel pigmentada potenciando la acción despigmentante '
                         'de los pasos siguientes.',
    'no_recomendado': 'En tu perfil, añadir un tónico con activos podría sobrecargar la piel o restarle '
                      'hidratación; es preferible concentrar los activos en el sérum.',
    'niacinamida': 'La niacinamida (vitamina B3) regula el sebo, minimiza la apariencia de los poros y '
                   'unifica el tono, siendo uno de los activos mejor tolerados.',
    'vitamina_c': 'La vitamina C es un antioxidante que ilumina el rostro, estimula el colágeno y '
                  'protege frente al daño ambiental; se usa de día bajo el protector solar.',
    'antiinflamatorio': 'Un sérum antiinflamatorio calma el enrojecimiento y la sensación de ardor '
                        'característicos de la piel sensible, reduciendo su reactividad.',
    'retinoide': 'El retinoide acelera la renovación celular y estimula el colágeno, mejorando textura '
                 'y arrugas. Se aplica de noche porque la luz solar lo degrada y aumenta la '
                 'fotosensibilidad.',
    'peptidos': 'Los péptidos son fragmentos de proteínas que envían señales a la piel para producir '
                'más colágeno, reforzando la firmeza sin causar irritación.',
    'combinado_am_pm': 'Tu perfil se beneficia de dos activos complementarios: vitamina C de día, para '
                       'proteger frente al daño ambiental, y retinoide de noche, para renovar la piel y '
                       'atenuar manchas y arrugas.',
    'gel_oil_free': 'Una fórmula en gel sin aceites hidrata mediante agua y humectantes ligeros, '
                    'aportando frescura sin obstruir los poros ni añadir grasa.',
    'locion_ligera': 'Una loción de textura ligera aporta la hidratación justa sin dejar sensación '
                     'pesada, adecuada cuando la piel necesita agua pero no lípidos densos.',
    'crema_ceramidas': 'Las ceramidas son lípidos que forman parte de la barrera cutánea; reponerlas '
                       'sella la hidratación y repara las pieles secas que las han perdido.',
    'crema_rica': 'Una textura rica en emolientes y lípidos nutre en profundidad las pieles secas con '
                  'signos de edad, devolviendo elasticidad y confort.',
    'locion_despigmentante': 'Combina hidratación ligera con activos que atenúan las manchas, ideal '
                             'para pieles grasas o mixtas con tendencia a pigmentarse que no toleran '
                             'texturas densas.',
    'crema_ceramidas_despig': 'Une la reparación de barrera de las ceramidas con activos '
                             'despigmentantes, atendiendo a la vez la sequedad y las manchas en un '
                             'solo paso.',
    'estandar': 'El protector solar es el paso más importante de la rutina: previene el '
                'fotoenvejecimiento y las manchas. Un SPF 50 diario protege frente a la radiación UVB.',
    'fisico_zno': 'El filtro físico con óxido de zinc refleja la radiación en la superficie de la piel '
                  'y es mejor tolerado por pieles sensibles, con menor riesgo de irritación.',
    'amplio_espectro_obligatorio': 'La protección de amplio espectro cubre rayos UVA y UVB. En tu '
                                   'perfil es imprescindible, pues previene tanto nuevas manchas como '
                                   'el agravamiento de los signos de edad.'
}

EXPLICACION_EJES = {
    'O': ('Grasa', 'produce más sebo; se benefician los activos seborreguladores y texturas ligeras.'),
    'D': ('Seca', 'pierde hidratación con facilidad; se priorizan ceramidas y texturas más ricas.'),
    'S': ('Sensible', 'reacciona con facilidad; se evitan fragancias y se eligen activos calmantes.'),
    'R': ('Resistente', 'tolera bien los activos; admite retinoides y exfoliantes potentes.'),
    'P': ('Pigmentada', 'tiende a formar manchas; se incorporan despigmentantes y más protección solar.'),
    'N': ('No pigmentada', 'mantiene un tono uniforme; la despigmentación no es prioritaria.'),
    'W': ('Con tendencia a arrugas', 'muestra signos de edad; se añaden antioxidantes y activos antiedad.'),
    'T': ('Estirada', 'se mantiene firme; el enfoque antiedad es preventivo.')
}

EJES_META = [
    ('e1', 'Hidratación', 'D · Seca', 'O · Grasa', 5, 25),
    ('e2', 'Sensibilidad', 'R · Resistente', 'S · Sensible', 5, 25),
    ('e3', 'Pigmentación', 'N · No pigmentada', 'P · Pigmentada', 4, 20),
    ('e4', 'Envejecimiento', 'T · Estirada', 'W · Arrugas', 4, 20),
]

def calcular_perfil(respuestas):
    ejes = {
        'e1': ['sensacion_lavado', 'brillo_tarde', 'poros', 'descamacion', 'base_comportamiento'],
        'e2': ['enrojece_productos', 'brotes_cosmeticos', 'irrita_sol', 'ardor_fragancia', 'antecedentes_reactiva'],
        'e3': ['manchas_herida', 'manchas_sol', 'pecas_melasma', 'uniformidad_tono'],
        'e4': ['arrugas_observa', 'horas_sol', 'frecuencia_spf', 'familia_envejecimiento'],
    }
    scores = {e: sum(mapas_scoring[c].get(respuestas[c], 3) for c in cols) for e, cols in ejes.items()}
    od = 'O' if scores['e1'] >= 15 else 'D'
    sr = 'S' if scores['e2'] >= 15 else 'R'
    pn = 'P' if scores['e3'] >= 12 else 'N'
    wt = 'W' if scores['e4'] >= 12 else 'T'
    return od + sr + pn + wt, scores

def predecir(respuestas):
    fila = pd.DataFrame(0.0, index=[0], columns=feature_names)
    for pregunta, respuesta in respuestas.items():
        col = f"{pregunta}_{respuesta}"
        if col in fila.columns:
            fila.at[0, col] = 1.0
    pred_remap = modelo.predict(fila)[0]
    pred_texto, confianzas = {}, {}
    for i, cat in enumerate(CATEGORIAS):
        cod = xgb_remaps[cat][pred_remap[i]]
        pred_texto[cat] = encoders[cat].inverse_transform([cod])[0]
        try:
            proba = modelo.estimators_[i].predict_proba(fila)[0]
            confianzas[cat] = float(np.max(proba))
        except Exception:
            confianzas[cat] = None
    return pred_texto, confianzas

def ensamblar_rutinas(pred):
    am, pm = [], []
    am.append(('Limpiador', NOMBRES_LEGIBLES['limpiador'][pred['limpiador']], pred['limpiador']))
    pm.append(('Limpiador', NOMBRES_LEGIBLES['limpiador'][pred['limpiador']], pred['limpiador']))
    if pred['toner'] != 'no_recomendado':
        am.append(('Tónico', NOMBRES_LEGIBLES['toner'][pred['toner']], pred['toner']))
        pm.append(('Tónico', NOMBRES_LEGIBLES['toner'][pred['toner']], pred['toner']))
    if pred['serum'] == 'combinado_am_pm':
        am.append(('Sérum', 'Sérum de vitamina C (día)', 'vitamina_c'))
        pm.append(('Sérum', 'Sérum con retinoide (noche)', 'retinoide'))
    elif pred['serum'] == 'retinoide':
        pm.append(('Sérum', NOMBRES_LEGIBLES['serum'][pred['serum']] + ' (noche)', 'retinoide'))
    else:
        am.append(('Sérum', NOMBRES_LEGIBLES['serum'][pred['serum']], pred['serum']))
        pm.append(('Sérum', NOMBRES_LEGIBLES['serum'][pred['serum']], pred['serum']))
    am.append(('Hidratante', NOMBRES_LEGIBLES['hidratante'][pred['hidratante']], pred['hidratante']))
    pm.append(('Hidratante', NOMBRES_LEGIBLES['hidratante'][pred['hidratante']], pred['hidratante']))
    am.append(('Protector solar', NOMBRES_LEGIBLES['spf'][pred['spf']], pred['spf']))
    if pred['exfoliante'] != 'ninguno':
        pm.append(('Exfoliante · 2-3 sem', NOMBRES_LEGIBLES['exfoliante'][pred['exfoliante']], pred['exfoliante']))
    pm.append(('Mascarilla · 1-2 sem', NOMBRES_LEGIBLES['mascarilla'][pred['mascarilla']], pred['mascarilla']))
    return am, pm

def chip_confianza(valor):
    if valor is None:
        return ''
    pct = int(round(valor * 100))
    clase = 'chip-alta' if valor >= 0.75 else 'chip-media' if valor >= 0.5 else 'chip-baja'
    return f'<span class="chip {clase}">{pct}%</span>'

def generar_pdf(perfil, am, pm):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2.2*cm, rightMargin=2.2*cm)
    styles = getSampleStyleSheet()
    borgona = colors.HexColor('#5C1526')
    titulo = ParagraphStyle('t', parent=styles['Title'], textColor=borgona, fontSize=22, spaceAfter=6)
    subt = ParagraphStyle('s', parent=styles['Heading2'], textColor=borgona, fontSize=14,
                          spaceBefore=14, spaceAfter=6)
    normal = ParagraphStyle('n', parent=styles['Normal'], fontSize=10.5, leading=16)
    elems = [Paragraph("Tu Rutina de Skincare Personalizada", titulo),
             Paragraph(f"Perfil dermatológico (Baumann): <b>{perfil}</b>", normal),
             Spacer(1, 0.3*cm), Paragraph("Rutina de Mañana (AM)", subt)]
    for i, (paso, prod, _) in enumerate(am, 1):
        elems.append(Paragraph(f"<b>{i}. {paso}:</b> {prod}", normal))
    elems.append(Paragraph("Rutina de Noche (PM)", subt))
    for i, (paso, prod, _) in enumerate(pm, 1):
        elems.append(Paragraph(f"<b>{i}. {paso}:</b> {prod}", normal))
    elems.append(Spacer(1, 0.6*cm))
    nota = ParagraphStyle('nota', parent=styles['Normal'], fontSize=8.5,
                          textColor=colors.grey, leading=12)
    elems.append(Paragraph("Recomendación generada por un modelo de machine learning (XGBoost) "
                           "con fines académicos y de orientación cosmética. No reemplaza una "
                           "consulta dermatológica. USIL 2026.", nota))
    doc.build(elems)
    buffer.seek(0)
    return buffer

# ═════════════════════════════════════════════════════════════
mostrar_banner()
st.markdown("# Tu perfil dermatológico")
st.markdown("Un cuestionario breve determina tu tipo de piel y construye una rutina de "
            "cuidado facial pensada para ti, dividida en día y noche.")
st.info("Prototipo académico de orientación cosmética. No reemplaza una consulta dermatológica profesional.")

with st.expander("📖  ¿Cómo funciona? Léeme antes de empezar"):
    st.markdown("""
    **Sigue estos pasos:**

    1. **Responde el paso previo.** Indica si tienes un diagnóstico dermatológico. Si lo tienes,
    la app te sugerirá acudir a un especialista, ya que este prototipo es solo para cuidado cosmético.

    2. **Completa el cuestionario.** Responde con sinceridad las preguntas sobre tu piel,
    organizadas en cuatro ejes: hidratación, sensibilidad, pigmentación y envejecimiento.
    No hay respuestas correctas o incorrectas; elige la opción que mejor describa tu piel.

    3. **Pulsa "Revelar mi rutina".** El sistema analizará tus respuestas y determinará tu
    tipo de piel según el sistema de clasificación de Baumann.

    4. **Revisa tu resultado.** Verás tu perfil, una explicación de cada característica de tu piel,
    y una rutina personalizada dividida en **mañana (AM)** y **noche (PM)**.

    5. **Explora el "¿Por qué?"** de cada producto para entender la razón de cada recomendación,
    y descarga tu rutina en PDF si deseas conservarla.

    *Tiempo estimado: 3 a 5 minutos.*
    """)

st.divider()

st.markdown('<p class="eyebrow">Paso previo</p>', unsafe_allow_html=True)
diagnostico = st.radio("¿Cuentas con diagnóstico médico de alguna enfermedad de la piel "
                       "(rosácea, dermatitis, psoriasis, acné severo en tratamiento, vitíligo u otra)?",
                       ['No', 'Sí'], index=0)
if diagnostico == 'Sí':
    st.warning("Dado que indicas un diagnóstico dermatológico, te recomendamos acudir a un "
               "especialista. Este prototipo atiende necesidades cosméticas no clínicas.")
    st.stop()

st.divider()
respuestas = {}

st.markdown('<p class="eyebrow">Eje 1</p>', unsafe_allow_html=True)
st.markdown("### Hidratación")
respuestas['sensacion_lavado'] = st.selectbox(
    "Treinta minutos después de lavar tu rostro, sin aplicar productos, ¿cómo se siente tu piel?",
    ['Muy tirante o áspera', 'Ligeramente tirante', 'Cómoda, sin brillo',
     'Con brillo en algunas zonas', 'Con brillo en todo el rostro'])
respuestas['brillo_tarde'] = st.selectbox("A media tarde, ¿cómo luce el brillo de tu rostro?",
    ['Sin brillo, más bien opaco', 'Brillo leve solo en la nariz',
     'Brillo en la zona T (frente y nariz)', 'Brillo en todo el rostro'])
respuestas['poros'] = st.selectbox("¿Qué tan visibles son tus poros en mejillas y nariz?",
    ['Casi imperceptibles', 'Visibles solo en la nariz',
     'Visibles en la zona T', 'Visibles en gran parte del rostro'])
respuestas['descamacion'] = st.selectbox("¿Tu piel tiende a descamarse o sentirse reseca?",
    ['Sí, con frecuencia', 'A veces, en zonas puntuales', 'Casi nunca', 'Nunca'])
respuestas['base_comportamiento'] = st.selectbox(
    "Si usas base o protector, ¿cómo se comporta durante el día?",
    ['Se cuartea o se ve reseca', 'Se mantiene estable',
     'Se desvanece por el brillo o sudor', 'No uso estos productos'])

st.markdown('<p class="eyebrow">Eje 2</p>', unsafe_allow_html=True)
st.markdown("### Sensibilidad")
respuestas['enrojece_productos'] = st.selectbox("¿Tu piel se enrojece, arde o pica al usar productos nuevos?",
    ['Nunca', 'Rara vez', 'A veces', 'Frecuentemente'])
respuestas['brotes_cosmeticos'] = st.selectbox("¿Has tenido brotes, ronchas o granitos al probar cosméticos?",
    ['Nunca', 'Alguna vez', 'Con frecuencia'])
respuestas['irrita_sol'] = st.selectbox("Al exponerte al sol, ¿tu piel se irrita o enrojece con facilidad?",
    ['No, tolera bien el sol', 'A veces', 'Sí, se irrita rápido'])
respuestas['ardor_fragancia'] = st.selectbox("¿Sientes ardor o tirantez con productos con fragancia o alcohol?",
    ['Nunca', 'A veces', 'Casi siempre'])
respuestas['antecedentes_reactiva'] = st.selectbox(
    "¿Tienes antecedentes de piel reactiva, alergias cutáneas o enrojecimiento frecuente?",
    ['No', 'Leves o esporádicos', 'Sí, marcados'])

st.markdown('<p class="eyebrow">Eje 3</p>', unsafe_allow_html=True)
st.markdown("### Pigmentación")
respuestas['manchas_herida'] = st.selectbox(
    "Cuando tienes un grano o herida, al sanar, ¿te queda una mancha oscura?",
    ['Nunca', 'A veces', 'Frecuentemente'])
respuestas['manchas_sol'] = st.selectbox("¿Has notado manchas oscuras en tu rostro por la exposición al sol?",
    ['No', 'Algunas leves', 'Sí, notorias'])
respuestas['pecas_melasma'] = st.selectbox("¿Presentas pecas, melasma o paño en el rostro?",
    ['No', 'Algunas pecas', 'Sí, manchas extensas'])
respuestas['uniformidad_tono'] = st.selectbox("¿Cómo describirías la uniformidad del tono de tu piel?",
    ['Tono parejo y uniforme', 'Ligeras irregularidades', 'Tono desigual o manchado'])

st.markdown('<p class="eyebrow">Eje 4</p>', unsafe_allow_html=True)
st.markdown("### Envejecimiento y hábitos")
respuestas['arrugas_observa'] = st.selectbox(
    "¿Observas líneas finas o arrugas (frente, contorno de ojos, boca)?",
    ['No, niguna', 'Muy leves al gesticular', 'Algunas visibles en reposo', 'Marcadas'])
respuestas['horas_sol'] = st.selectbox("¿Cuántas horas al día te expones al sol de forma acumulada?",
    ['Menos de 1 hora', 'Entre 1 y 3 horas', 'Más de 3 horas'])
respuestas['frecuencia_spf'] = st.selectbox("¿Con qué frecuencia usas protector solar?",
    ['A diario', 'A veces', 'Casi nunca o nunca'])
respuestas['familia_envejecimiento'] = st.selectbox(
    "En tu familia directa, ¿es común el envejecimiento cutáneo temprano?",
    ['No', 'No estoy seguro/a', 'Sí'])

st.markdown('<p class="eyebrow">Sobre ti</p>', unsafe_allow_html=True)
st.markdown("### Contexto")
respuestas['preocupacion_principal'] = st.selectbox("¿Cuál es tu principal preocupación con tu piel?",
    ['Acné o granitos', 'Manchas / hiperpigmentación', 'Ojeras', 'Textura o poros',
     'Resequedad', 'Líneas o arrugas', 'Ninguna en particular'])
respuestas['rutina_actual'] = st.selectbox("¿Realizas actualmente alguna rutina de cuidado facial?",
    ['No realizo ninguna', 'Solo limpieza ocasional',
     'Rutina básica (limpieza e hidratación)', 'Rutina completa con varios productos'])
respuestas['productos_usados'] = st.selectbox("¿Cuántos productos de skincare usas habitualmente?",
    ['Ninguno', '1 a 2', '3 a 4', '5 o más'])
respuestas['edad'] = st.selectbox("Edad", ['18 a 24 años', '25 a 29 años', '30 a 35 años'])
respuestas['sexo'] = st.selectbox("Sexo", ['Femenino', 'Masculino', 'Prefiero no decirlo'])

st.divider()

if st.button("Revelar mi rutina", type="primary", use_container_width=True):
    perfil, scores = calcular_perfil(respuestas)
    pred, confianzas = predecir(respuestas)
    am, pm = ensamblar_rutinas(pred)

    st.markdown('<p class="eyebrow">Tu resultado</p>', unsafe_allow_html=True)
    st.markdown(f"# Tipo de piel: {perfil}")

    # MEJORA 1 — Diagrama de los 4 ejes
    st.markdown('<p class="eyebrow">Tu perfil en los cuatro ejes de Baumann</p>', unsafe_allow_html=True)
    for key, nombre, izq, der, minv, maxv in EJES_META:
        val = scores[key]
        pct = max(4, min(96, (val - minv) / (maxv - minv) * 100))
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
          <div style="display:flex;justify-content:space-between;">
            <span style="font-family:'Cormorant Garamond',serif;font-size:1.15rem;color:#FBEDF0;">{nombre}</span>
            <span style="color:#E8A0B4;font-size:0.85rem;">puntaje {val} / {maxv}</span>
          </div>
          <div class="axis-track"><div class="axis-marker" style="left:{pct}%;"></div></div>
          <div class="axis-ends"><span style="color:#E8A0B4;font-size:0.78rem;">{izq}</span>
          <span style="color:#E8A0B4;font-size:0.78rem;">{der}</span></div>
        </div>""", unsafe_allow_html=True)

    # Significado del perfil (tarjetas por color)
    st.markdown('<p class="eyebrow">Qué significa tu perfil</p>', unsafe_allow_html=True)
    colores_texto = {'eje-1': '#5C1526', 'eje-2': '#6A1730', 'eje-3': '#6A1730', 'eje-4': '#5C1526'}
    for letra, css in zip(perfil, ['eje-1', 'eje-2', 'eje-3', 'eje-4']):
        nombre, desc = EXPLICACION_EJES[letra]
        c = colores_texto[css]
        st.markdown(
            f'<div class="card-eje {css}">'
            f'<div style="color:{c};font-family:\'Cormorant Garamond\',serif;'
            f'font-size:1.4rem;font-weight:600;margin-bottom:0.3rem;line-height:1.2;">{nombre}</div>'
            f'<div style="color:{c};font-size:0.94rem;line-height:1.5;font-weight:400;">'
            f'Tu piel {desc}</div></div>',
            unsafe_allow_html=True)

    st.markdown('<p class="eyebrow">Por qué esta rutina es la más conveniente</p>', unsafe_allow_html=True)
    st.markdown("Cada producto responde a tu combinación única de hidratación, sensibilidad, "
                "pigmentación y envejecimiento. La rutina de **mañana** protege tu piel durante "
                "el día y la de **noche** la repara y renueva mientras descansas.")
    st.divider()

    # MEJORA 4 — Rutinas AM/PM con explicación por producto
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### ☀️ Mañana')
        for i, (paso, prod, cod) in enumerate(am, 1):
            st.markdown(f'<span class="paso-num">{i}. {paso}</span>', unsafe_allow_html=True)
            st.markdown(prod)
            if cod in EXPLICACION_PRODUCTO:
                with st.expander("¿Por qué?"):
                    st.caption(EXPLICACION_PRODUCTO[cod])
    with col2:
        st.markdown('### 🌙 Noche')
        for i, (paso, prod, cod) in enumerate(pm, 1):
            st.markdown(f'<span class="paso-num">{i}. {paso}</span>', unsafe_allow_html=True)
            st.markdown(prod)
            if cod in EXPLICACION_PRODUCTO:
                with st.expander("¿Por qué?"):
                    st.caption(EXPLICACION_PRODUCTO[cod])

    # MEJORA 2 — Confianza del modelo por categoría
    st.divider()
    st.markdown('<p class="eyebrow">Confianza del modelo por categoría</p>', unsafe_allow_html=True)
    filas = st.columns(4)
    for idx, cat in enumerate(CATEGORIAS):
        c = confianzas.get(cat)
        if c is not None:
            with filas[idx % 4]:
                st.markdown(f"**{cat.capitalize()}** {chip_confianza(c)}", unsafe_allow_html=True)

    # MEJORA 3 — Descarga PDF
    st.divider()
    try:
        pdf = generar_pdf(perfil, am, pm)
        st.download_button("⬇︎  Descargar mi rutina en PDF", data=pdf,
                           file_name=f"rutina_skincare_{perfil}.pdf",
                           mime="application/pdf", use_container_width=True)
    except Exception:
        st.caption("Para habilitar la descarga en PDF, añade 'reportlab' al requirements.txt.")

    st.markdown("<p style='font-size:0.72rem;font-style:italic;color:#E8A0B4;"
                "letter-spacing:0.02em;margin-top:0.8rem;'>"
                "Recomendación generada por un modelo XGBoost entrenado sobre perfiles "
                "dermatológicos autorreportados. Para necesidades clínicas, consulta a un "
                "dermatólogo.</p>", unsafe_allow_html=True)
