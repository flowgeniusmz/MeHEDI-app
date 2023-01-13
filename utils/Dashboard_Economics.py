import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

#from Patient_Form import form_pazienti

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8"
SHEET_NAME = "Database_Operations"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector

def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df

df_operations=connect_to_gsheet()

def dashboard_economics():
    
    st.title("Dashboard MedTech Economics")
    expander = st.expander("See all records")
    with expander:
        st.write(f"Open original [Google Sheet]({GSHEET_URL})")
        st.dataframe(get_data(df_operations))
    
    st.markdown("""**Questa sezione mostra i risultati dell'analisi utilizzando i dati delle operations di MeHedi""")
    
    g1, g2 = st.columns(2)
    g1.metric(label = "Fatturato mensile", value = ("505.000€"), delta = ("20.000€"))
    g2.metric(label = "Costi menisili",
    value = ("202.300 €"),
    delta = ("10.000€"))

    col1, col2 = st.columns(2)

    with col1:
        st.header("Economics")
        st.image("https://www.slideteam.net/media/catalog/product/cache/1280x720/d/a/dashboard_depicting_hospital_kpi_with_treatment_costs_slide01.jpg")

    with col2:
        st.header("Health data")
        st.image("https://www.datapine.com/images/hospital-kpi-dashboard.png")
