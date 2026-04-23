import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import time

st.set_page_config(page_title="Sara KPI", layout="centered")

# ===== STYLE =====
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.big-number {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
}
.green {
    color: #00ff88;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: #1c1f26;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== CONFIG =====
SHEET_ID = "1BoU7ADi3BZKFqP9tYVE3LeaZ3FPndmVh0TgRM9cBTOg"
TAB_NAME = "2026"

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

    fisso = clean(sheet.acell("C5").value)
    indiretto_cu = clean(sheet.acell("C8").value)
    indiretto_venditori = clean(sheet.acell("C11").value)
    geko = clean(sheet.acell("C14").value)
    rinnovi = clean(sheet.acell("M20").value)
    referral = clean(sheet.acell("M26").value)
    vendita_cnp = clean(sheet.acell("M32").value)
    royalties = clean(sheet.acell("M38").value)
    cross = clean(sheet.acell("M44").value)

    totale = (
        fisso + indiretto_cu + indiretto_venditori +
        geko + rinnovi + referral + vendita_cnp +
        royalties + cross
    )

    return {
        "totale": totale,
        "fisso": fisso,
        "indiretto_cu": indiretto_cu,
        "indiretto_venditori": indiretto_venditori,
        "geko": geko,
        "rinnovi": rinnovi,
        "referral": referral,
        "vendita_cnp": vendita_cnp,
        "royalties": royalties,
        "cross": cross
    }

data = load_data()

# ===== FRASI =====
frasi = [
    "💣 Stai spaccando tutto",
    "🔥 Sei una macchina da guerra",
    "💸 Cash flow attivo",
    "🚀 Livello successivo",
    "👑 Regina delle commissioni",
    "📈 Crescita costante"
]

frase_random = random.choice(frasi)

# ===== HEADER =====
st.markdown("## 📊 Sara KPI")

# ===== TOTALE =====
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="big-number green">€ {:,.0f}</div>'.format(data["totale"]).replace(",", "."), unsafe_allow_html=True)

# PROGRESS BAR
obiettivo = 5000
progress = min(data["totale"] / obiettivo, 1.0)
st.progress(progress)

mancante = obiettivo - data["totale"]
if mancante > 0:
    st.caption(f"Obiettivo €{obiettivo} · Mancano €{int(mancante)}")
else:
    st.success("💥 OBIETTIVO RAGGIUNTO")

st.markdown('</div>', unsafe_allow_html=True)

# ===== FRASE MOTIVAZIONALE =====
st.markdown(f"### {frase_random}")

# ===== SUONO (quando aggiorni) =====
if st.button("🔄 Aggiorna KPI"):
    st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3")
    st.rerun()

# ===== DETTAGLIO =====
st.markdown('<div class="card">', unsafe_allow_html=True)

st.write(f"Fisso: € {data['fisso']}")
st.write(f"Indiretto CU: € {data['indiretto_cu']}")
st.write(f"Indiretto Venditori: € {data['indiretto_venditori']}")
st.write(f"GEKO Gold: € {data['geko']}")
st.write(f"Rinnovi: € {data['rinnovi']}")
st.write(f"Referral: € {data['referral']}")
st.write(f"Vendita CNP: € {data['vendita_cnp']}")
st.write(f"Royalties: € {data['royalties']}")
st.write(f"Cross selling: € {data['cross']}")

st.markdown('</div>', unsafe_allow_html=True)
