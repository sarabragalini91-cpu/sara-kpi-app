import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh
import random

st.set_page_config(page_title="Sara KPI", layout="centered")

SHEET_ID = "1BoU7ADi3BZKFqP9tYVE3LeaZ3FPndmVh0TgRM9cBTOg"
TAB_NAME = "2026"
OBIETTIVO = 5000

# Auto-refresh ogni 30 secondi
st_autorefresh(interval=30000, key="kpi_refresh")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top, #182033 0%, #080b10 65%);
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 16px;
    margin-bottom: 24px;
}

.total-card {
    background: linear-gradient(135deg, #111827, #172033);
    border: 1px solid rgba(34,197,94,.55);
    border-radius: 30px;
    padding: 34px;
    text-align: center;
    box-shadow: 0 0 45px rgba(34,197,94,.22);
    margin-bottom: 22px;
}

.total-number {
    font-size: 78px;
    font-weight: 900;
    color: #4ade80;
    line-height: 1;
}

.level {
    text-align: center;
    font-size: 26px;
    font-weight: 900;
    margin: 24px 0 10px 0;
}

.phrase {
    text-align: center;
    font-size: 20px;
    color: #facc15;
    font-weight: 800;
    margin-bottom: 25px;
}

.grid-card {
    background: rgba(17, 24, 39, .92);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 20px;
    padding: 18px 20px;
    margin-bottom: 12px;
}

.kpi-row {
    display: flex;
    justify-content: space-between;
    font-size: 18px;
    font-weight: 800;
}

.value {
    color: #e5e7eb;
}

.small {
    text-align:center;
    color:#9ca3af;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

def clean(val):
    try:
        if val is None or val == "":
            return 0.0
        val = str(val).replace("€", "").replace(".", "").replace(",", ".").strip()
        return float(val)
    except:
        return 0.0

@st.cache_data(ttl=10)
def load_data():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        dict(st.secrets["gcp_service_account"]), scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(TAB_NAME)

    data = {
        "Fisso": clean(sheet.acell("C5").value),
        "Indiretto CU": clean(sheet.acell("C8").value),
        "Indiretto Venditori": clean(sheet.acell("C11").value),
        "GEKO Gold": clean(sheet.acell("C14").value),
        "Rinnovi": clean(sheet.acell("N20").value),
        "Referral": clean(sheet.acell("N26").value),
        "Vendita CNP": clean(sheet.acell("N32").value),
        "Royalties": clean(sheet.acell("N38").value),
        "Cross selling": clean(sheet.acell("N43").value),
    }
    data["Totale"] = sum(data.values())
    return data

def euro(v):
    return f"€ {int(v):,}".replace(",", ".")

def livello(totale):
    if totale >= 10000:
        return "👑 GOD MODE"
    if totale >= 7000:
        return "🔥 MODALITÀ BESTIA"
    if totale >= 5000:
        return "🚀 OBIETTIVO SFONDATO"
    if totale >= 3000:
        return "💣 STAI SPACCANDO TUTTO"
    return "⚡ MOTORE ACCESO"

frasi = [
    "Non è fortuna: è sistema.",
    "Ogni vendita del team adesso fa rumore.",
    "Cash flow attivo. Continua così.",
    "La macchina sta girando.",
    "Ancora una botta e cambi livello.",
    "Regina delle commissioni in caricamento."
]

data = load_data()
totale = data["Totale"]

if "last_total" not in st.session_state:
    st.session_state.last_total = totale

diff = totale - st.session_state.last_total

st.markdown('<div class="main-title">📊 SARA KPI APP</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Aggiornamento automatico ogni 30 secondi</div>', unsafe_allow_html=True)

if diff > 0:
    st.balloons()
    st.toast(f"💣 BOOM! Nuova entrata: +{euro(diff)}", icon="💸")
    st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3", autoplay=True)

st.markdown('<div class="total-card">', unsafe_allow_html=True)
st.markdown(f'<div class="total-number">{euro(totale)}</div>', unsafe_allow_html=True)
st.progress(min(totale / OBIETTIVO, 1.0))
manca = max(OBIETTIVO - totale, 0)
st.markdown(
    f'<div class="small">Obiettivo {euro(OBIETTIVO)} · Mancano {euro(manca)}</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="level">{livello(totale)}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="phrase">💸 {random.choice(frasi)}</div>', unsafe_allow_html=True)

if st.button("🔄 Aggiorna ora", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

for nome, valore in data.items():
    if nome != "Totale":
        st.markdown(
            f"""
            <div class="grid-card">
                <div class="kpi-row">
                    <span>{nome}</span>
                    <span class="value">{euro(valore)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.session_state.last_total = totale
