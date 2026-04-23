import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Sara KPI", layout="centered")

SHEET_ID = "1BoU7ADi3BZKFqP9tYVE3LeaZ3FPndmVh0TgRM9cBTOg"
TAB_NAME = "2026"
OBIETTIVO = 5000

st_autorefresh(interval=30000, key="kpi_refresh")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top, #431407 0%, #111827 48%, #020617 100%);
}

.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 900;
    margin-bottom: 4px;
    color: #fff7ed;
    text-shadow: 0 0 22px rgba(249,115,22,.75);
}

.subtitle {
    text-align: center;
    color: #fed7aa;
    font-size: 15px;
    margin-bottom: 24px;
}

.total-card {
    background: linear-gradient(135deg, #111827, #2b0b02);
    border: 1px solid rgba(249,115,22,.75);
    border-radius: 34px;
    padding: 36px;
    text-align: center;
    box-shadow: 0 0 55px rgba(249,115,22,.35);
    margin-bottom: 22px;
}

.total-number {
    font-size: 82px;
    font-weight: 900;
    color: #f97316;
    line-height: 1;
    text-shadow: 0 0 24px rgba(249,115,22,.75);
}

.level {
    text-align: center;
    font-size: 28px;
    font-weight: 900;
    margin: 24px 0 10px 0;
    color: #fff7ed;
}

.phrase {
    text-align: center;
    font-size: 20px;
    color: #facc15;
    font-weight: 900;
    margin-bottom: 25px;
}

.grid-card {
    background: rgba(17, 24, 39, .94);
    border: 1px solid rgba(249,115,22,.25);
    border-radius: 22px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 0 18px rgba(0,0,0,.25);
}

.kpi-row {
    display: flex;
    justify-content: space-between;
    font-size: 18px;
    font-weight: 800;
}

.value {
    color: #fdba74;
}

.small {
    text-align:center;
    color:#fed7aa;
    font-size:13px;
}

.fire {
    position: fixed;
    bottom: -40px;
    animation: rise 3.2s linear infinite;
    font-size: 34px;
    z-index: 999999;
    opacity: .85;
}

@keyframes rise {
    0% { transform: translateY(0) scale(.8) rotate(0deg); opacity: .2; }
    30% { opacity: .95; }
    100% { transform: translateY(-110vh) scale(1.35) rotate(360deg); opacity: 0; }
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
        return "👑 GOD MODE — STAI DOMINANDO"
    if totale >= 7000:
        return "🔥 MODALITÀ BESTIA"
    if totale >= 5000:
        return "🚀 OBIETTIVO SFONDATO"
    if totale >= 3000:
        return "💣 STAI SPACCANDO TUTTO"
    return "⚡ MOTORE ACCESO"


def play_fire_sound():
    components.html(
        """
        <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function beep(freq, start, duration) {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = "square";
            osc.frequency.value = freq;
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime + start);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + start + duration);
            osc.start(audioCtx.currentTime + start);
            osc.stop(audioCtx.currentTime + start + duration);
        }

        beep(500, 0, 0.15);
        beep(750, 0.18, 0.15);
        beep(1000, 0.36, 0.22);
        </script>
        """,
        height=0,
    )


frasi = [
    "Non è fortuna: è sistema.",
    "Ogni vendita del team adesso fa rumore.",
    "Cash flow attivo. Continua così.",
    "La macchina sta girando.",
    "Ancora una botta e cambi livello.",
    "Regina delle commissioni in caricamento.",
    "Qui non si lavora: si conquista.",
    "Il CRM piange, tu incassi.",
    "Modalità fatturato: ACCESA.",
]

if "audio_attivo" not in st.session_state:
    st.session_state.audio_attivo = False

data = load_data()
totale = data["Totale"]

if "last_total" not in st.session_state:
    st.session_state.last_total = totale

diff = totale - st.session_state.last_total

st.markdown('<div class="main-title">🔥 SARA KPI APP 🔥</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Aggiornamento automatico ogni 30 secondi · modalità tamarra attiva</div>', unsafe_allow_html=True)

if st.button("🔊 ATTIVA SUONI TAMARRI", use_container_width=True):
    st.session_state.audio_attivo = True
    st.toast("Audio attivato. Ora quando salgono i soldi si sente 🔥", icon="🔊")
    play_fire_sound()

if diff > 0:
    st.toast(f"🔥 BOOM! Nuova entrata: +{euro(diff)}", icon="💸")
    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:30px;
            font-weight:900;
            color:#facc15;
            margin:18px 0;
            text-shadow: 0 0 18px rgba(250,204,21,.7);
        ">
            + {euro(diff)} RILEVATI 🔥
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.audio_attivo:
        play_fire_sound()

st.markdown('<div class="total-card">', unsafe_allow_html=True)
st.markdown(f'<div class="total-number">{euro(totale)}</div>', unsafe_allow_html=True)

st.progress(min(totale / OBIETTIVO, 1.0))

manca = max(OBIETTIVO - totale, 0)
if manca > 0:
    st.markdown(
        f'<div class="small">Obiettivo {euro(OBIETTIVO)} · Mancano {euro(manca)}</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="small">💥 OBIETTIVO RAGGIUNTO · ORA SI ALZA L’ASTICELLA</div>',
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="level">{livello(totale)}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="phrase">💸 {random.choice(frasi)}</div>', unsafe_allow_html=True)

if st.button("🔄 AGGIORNA ORA", use_container_width=True):
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
            unsafe_allow_html=True,
        )

for i, left in enumerate([6, 16, 28, 42, 57, 70, 84, 94]):
    st.markdown(
        f'<div class="fire" style="left:{left}%; animation-delay:{i*0.35}s;">🔥</div>',
        unsafe_allow_html=True,
    )

st.session_state.last_total = totale
