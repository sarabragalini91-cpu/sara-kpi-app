import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Sara KPI", layout="centered")

SHEET_ID = "1BoU7ADi3BZKFqP9tYVE3LeaZ3FPndmVh0TgRM9cBTOg"
TAB_NAME = "2026"

def clean(val):
    if val is None or val == "":
        return 0.0
    val = str(val).replace("€", "").replace(".", "").replace(",", ".").strip()
    return float(val)

@st.cache_data(ttl=10)
def load_data():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    service_account_info = dict(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
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
        "Royalties": clean(sheet.acell("N37").value),
        "Cross selling": clean(sheet.acell("N43").value),
    }

    data["Totale"] = sum(data.values())
    return data

data = load_data()

st.title("📊 Sara KPI")

st.metric("💰 Totale", f"€ {int(data['Totale'])}")

st.divider()

for k, v in data.items():
    if k != "Totale":
        st.write(f"**{k}**: € {int(v)}")
