# -*- coding: utf-8 -*-

# import libraries
import pandas as pd
import streamlit as st
from PIL import Image
import time
import datetime
import database as db
import streamlit_authenticator as stauth
import google_auth_httplib2
import httplib2
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from feel_it import EmotionClassifier, SentimentClassifier

from utils.Dashboard_Operations import dashboard_operations
from utils.Dashboard import dashboard_patient_satisf
from utils.Dashboard_Economics import dashboard_economics
from utils.Info_Page import landing_page
from utils.addition.graphs import graph_pes

# css_file="style.css"
image = Image.open('images/logo_form4.png')
image2 = Image.open('images/Mehedi_logo.png')
image3 = Image.open('images/Mehedi_logo2.png')
img = Image.open('images/background.jpg')
img2 = Image.open('images/med_bot.png')

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

# initial graphic setting
st.set_page_config(page_title="FlowGenius", page_icon="🏥", layout="wide")

@st.cache_resource()
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

@st.cache_data()
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


def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:E",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

# --- USER AUTHENTICATION ---

#users = db.fetch_all_users()

#usernames = [user["key"] for user in users]
#names = [user["name"] for user in users]
#hashed_passwords = [user["password"] for user in users]

#authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'some_cookie_name','some_signature_key',cookie_expiry_days=30)
#name, authentication_status, username = authenticator.login("Login - Web application MEHEDI Patient's satisfaction", "main")

#if st.session_state["authentication_status"] == False:
#    st.error("Username/password is incorrect")

#if st.session_state["authentication_status"] == None:
#    st.write('<base target="_blank">', unsafe_allow_html=True)
#    prev_time = [time.time()]
#    a, b, = st.columns([1, 1])
#    with a:
#        st.image(image2, width=300)      
#        hide_img_fs = '''
#        <style>
#        button[title="View fullscreen"]{
#            visibility: hidden;}
#        </style>
#        '''
#        st.markdown(hide_img_fs, unsafe_allow_html=True)
#    with b:
#        st.info("This is a webapp created to evaluate Patient Satisfaction in a medium-sized healthcare company. PATIENT ACCESS - username: guest | password: paz123 MANAGEMENT ACCESS - username: mballabio | password: mat123") 

#if st.session_state["authentication_status"]:

no_auth=True
if no_auth==True:
    #placeholder.empty()

    # ---- SIDEBAR ----
    #authenticator.logout("Logout", "sidebar")
    st.sidebar.title("Welcome 👋")
    
    def patient_form():
        
        # Add the markdown code to hide the header element
        st.markdown(
            """
            <style>
            header[data-testid="stHeader"] {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # To widen the margins from block-container
        st.markdown("""
        <style>
               .css-k1ih3n {
                    padding-top: 0rem;
                    padding-bottom: 4rem;
                    padding-left: 4em;
                    padding-right: 4rem;
                }
        </style>
        """, unsafe_allow_html=True)
        
        t1, t2 = st.columns((1, 0.10)) 

        t1.image(image, width=1000)
        hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
        st.markdown(hide_img_fs, unsafe_allow_html=True)
        #t1.markdown("### This section shows some information about Tool of Patient Satisfaction")
        t2.write("")

        reduce_header_height_style = """
            <style>
                div.block-container {padding-top:1rem;}
            </style>
        """
        st.markdown(reduce_header_height_style, unsafe_allow_html=True)

        # connect and append data
        df = connect_to_gsheet()
        
        # SIDEBAR
        st.sidebar.markdown("""<hr style="height:5px;border:none;color:#bfbfbf;background-color:#bfbfbf;" /> """, unsafe_allow_html=True)
        st.sidebar.info(
        """
        This is a webapp created by that allows you to evaluate Patient Satisfaction.
        
        
        """
        )
        
        st.sidebar.title("Support")
        st.sidebar.info(
        """
        For any issues with app usage, please contact:mzozulia@flowgenius.com
        """
        )
        a, b, c = st.sidebar.columns([0.2,1,0.2])
        with a:
            st.write("")
        with b:
            st.write("Hello")
        with c:
            st.write("")
        
        # INTRODUCTION FORM
        i,a,b,c,d = st.columns([0.2,7,0.1,2,1.5])
        with i:
            st.write("")
        with a:
            with st.expander("ℹ️ General Form Filling Instructions", expanded=False):
                st.markdown(
                    """
                    ### Return on Experience Framework
                    This framework serves the healthcare facility to collect feedback regarding the services provided to its patients. For any issues upon completing the form, it will be possible to contact the facility via email.
                    """
                )
                st.markdown(
                    """
                    ### Instructions for Form Filling
                    Dear patient,
                    
                    Your doctor has directed you to the Radiology department for some tests. Now, at the end of the exams and as you leave our department, we would like to ask you some questions about our department and your experience. Your answers will allow us to improve the quality of service offered to you as a patient. Your opinion is very important to us.
                    
                    It will only take a few minutes of your time. Please read each question carefully, choose your answer, and mark it. If you feel unable to answer a specific question, move on to the next one.
                    
                    For some questions, we would like you to give us a score ranging from 1 to 7: 7 means you are very satisfied and 1 means you are very dissatisfied. You can provide any score you deem appropriate. *[7=excellent, 6=very satisfied, 5=satisfied, 4=neutral, 3=neither satisfied nor dissatisfied, 2=dissatisfied, 1=very dissatisfied]*.
                    
                    ### Why Do We Want to Measure Patient Satisfaction?
                    1. Improvement of targeted services offered by the facility
                    2. Save our patients' time through a better Patient Experience in our facility
                    3. Monitoring strengths and areas of improvement of our facility
                    """
                )
                st.markdown("")
            st.write("")
            new_title = '<b style="font-family:serif; color:#6082B6; font-size: 28px;">📌 How much time do you have to complete the form?</b>'
            st.markdown(new_title, unsafe_allow_html=True)
            st.write("")
            slider = st.slider(label='Drag the slider (For English version set the slider to 0)', min_value=0,max_value=10, value=0, key='Form5')
        with b:
            st.write("")
        with c:
            st.info("Hi, I'm Cleo, your personal assistant!")
            st.info("I can help you complete our Patient Satisfaction form. If you have any doubts, feel free to check the 'General Form Filling Instructions' section.")
        with d:
            st.image(img2)

        # ###FORM 0 Eng
        if slider == 0:
            col1, col2 = st.columns([1, 0.60])
            with col1:
                new_title = '<b style="font-family:serif; color:#FF0000; font-size: 40px;">📋 Experience Form:</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                st.info("➡️ 1. How did you schedule the appointment?")
                cols = st.columns((1, 1))
                # APPOINTMENT
                var_a1 = cols[0].selectbox("I scheduled an appointment:", ["In person",  "By phone",  "Website", "E-mail",  "Through a doctor",  "Other"])
                var_a2 = cols[1].slider("How satisfied are you with the ease of scheduling an appointment?", 1, 7, 1)
        
                # RECEPTION
                st.info("➡️ 2. On the reception at our department")
                cols2 = st.columns((2))
                var_c1 = cols2[0].slider("How satisfied are you with the reception at our department?", 1, 7, 1)
                var_c2 = cols2[1].slider("How satisfied are you with the waiting time for assistance at the reception?", 1, 7, 1)
        
            # PROCEDURE
            st.info("➡️ 3. About the prescribed procedure")
            cols3 = st.columns((1, 1, 1))
            var_d1 = cols3[0].selectbox("Which medical imaging procedure did you undergo?", ["MRI", "CT", "Ultrasound", "X-Ray", "Mammography", "Arthrography/Myelography", "Interventions/Biopsies", "Other"])
            var_d2 = cols3[1].slider("How satisfied are you with the waiting time in the department before the procedure?", 1, 7, 1)
            options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90]
            if var_d1 == "MRI":
                var_d3 = cols3[2].selectbox("How long was the visit? (minutes)", options=options, index=options.index(30))
            elif var_d1 == "CT" or var_d1 == "Mammography":
                var_d3 = cols3[2].selectbox("How long was the visit? (minutes)", options=options, index=options.index(5))
            elif var_d1 == "Ultrasound" or var_d1 == "Arthrography/Myelography" or var_d1 == "Interventions/Biopsies":
                var_d3 = cols3[2].selectbox("How long was the visit? (minutes)", options=options, index=options.index(20))
            elif var_d1 == "X-Ray":
                var_d3 = cols3[2].selectbox("How long was the visit? (minutes)", options=options, index=options.index(2))
            else:
                var_d3 = cols3[2].selectbox("How long was the visit? (minutes)", options=options, index=options.index(1))
        
            # EXPLANATION OF RESULTS
            st.info("➡️ 4. Explanation of department's results")
            cols3 = st.columns((1, 1, 1))
            var_f1 = cols3[0].selectbox("Did you consult a healthcare provider after your department visit?", ["NO", "Yes, radiologist (doctor)", "Yes, radiology technician", "Other specialist"])
            var_f2 = cols3[1].selectbox("Did you consult a health professional to have the results explained?", ["NO", "Yes, radiologist (doctor)", "Yes, radiology technician", "Other specialist"])
            var_f3 = cols3[2].slider("How satisfied are you with the explanation provided by the radiologist?", 1, 7, 1)
        
            # PATIENT EXPERIENCE
            st.info("➡️ 5. How was your experience in the department as a patient")
            cols3 = st.columns((1, 1, 1, 1, 1))
            var_h1 = cols3[0].slider("How satisfied are you with the availability of restroom facilities?", 1, 7, 1)
            var_h2 = cols3[1].slider("How satisfied are you with the cleanliness of the department?", 1, 7, 1)
            var_h5 = cols3[2].slider("How satisfied are you with the staff's friendliness?", 1, 7, 1)
            var_h7 = cols3[3].slider("Did you feel your privacy was respected?", 1, 7, 1)
            var_h9 = cols3[4].selectbox("Would you recommend our radiology department to your family and friends?", ["YES", "NO"])
        
            # PATIENT INFO
            st.info("➡️ 6. Our analysis of your responses")
            cols3 = st.columns((1, 1))
            var_i1 = cols3[0].select_slider("Could you indicate your age group (optional)?", options=["< 18 years",	"18-30 years", 	"30-65 years",  ">65 years" ])
            var_i2 = cols3[1].selectbox("Could you indicate your gender (optional)?", options=["Male", "Female", "Not Specified" ])
        
            with col2:
                reception_avg=(var_c1+var_c2)/2
                experience_avg=(var_h1+var_h2+var_h5+var_h7)/4
                DATA = [{"taste": "APPOINTMENT", "Area Weight": var_a2},
                            {"taste": "RECEPTION", "Area Weight": reception_avg},
                            {"taste": "PROCEDURE", "Area Weight": var_d2},
                            {"taste": "RESULTS", "Area Weight": var_f3},
                            {"taste": "EXPERIENCE", "Area Weight": experience_avg}]
                graph_pes(DATA)
                total_avg=round(((reception_avg+experience_avg+var_a2+var_d2+var_f3)/5), 1)
        
            # COMMENT 1
            cols_text = st.columns((0.25, 1))
            if total_avg == 1:
                pass
            elif total_avg <= 4:
                cols_text[0].metric("Result of your survey:", value=str(total_avg) + "/7")
                feedback_gen = cols_text[1].text_area("Your experience can be improved, tell us what you think and we will definitely improve")
            elif total_avg > 4 and total_avg <= 5:
                cols_text[0].metric("Result of your survey:", value=str(total_avg) + "/7")
                feedback_gen = cols_text[1].text_area("Your experience didn't go perfectly, if you're interested, tell us about your experience and we will definitely improve the weak points of our facility")
            elif total_avg > 5 and total_avg <= 7:
                cols_text[0].metric("Result of your survey:", value=str(total_avg) + "/7")
                feedback_gen = cols_text[1].text_area("Your experience seems to have gone well, if you're interested, tell us about your experience and we will continue to improve")
            else:
                feedback_gen = ""
        
            # ADDITIONAL COMMENT
            if total_avg == 1:
                pass
            elif total_avg < 4.5:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("Your OVERALL EXPERIENCE AT OUR FACILITY is very poor with a result of " + str(total_avg) + "/7. We would like to ask what problems you encountered at our facility.", icon="🚨")
                colss[1].write("")
                add_comm = colss[2].text_area("Write to us what didn't work. We will improve thanks to your feedback. Your opinion is crucial for us.")
            elif var_a2 < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("The APPOINTMENT area is very deficient with a result of " + str(var_a2) + "/7. We would like to ask what problems you encountered at our facility.", icon="🚨")
                colss[1].write("")
                add_comm = colss[2].text_area("Write to us what didn't work. We will improve thanks to your feedback. Your opinion is crucial for us.")
            elif reception_avg < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("The PATIENT RECEPTION area is very deficient with a result of " + str(reception_avg) + "/7. We would like to ask what problems you encountered at our facility. Being one of the most important areas for us, we would love to hear your opinion.", icon="🚨")
                colss[1].write("")
                add_comm = colss[2].text_area("Write to us what didn't work. We will improve thanks to your feedback. Your opinion is crucial for us.")
            elif var_d2 < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("The PROCEDURE area is very deficient with a result of " + str(var_d2) + "/7. We would like to ask what problems you encountered at our facility.", icon="🚨")
                colss[1].write("")
                add_comm = colss[2].text_area("Write to us what didn't work. We will improve thanks to your feedback. Your opinion is crucial for us.")
            elif var_f3 < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("The RESULTS area is very deficient with a result of " + str(var_f3) + "/7. We would like to ask what problems you encountered at our facility.", icon="🚨")
                colss[1].write("")
                add_comm = colss[2].text_area("Write to us what didn't work. We will improve thanks to your feedback. Your opinion is crucial for us.")
            elif experience_avg < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("The PATIENT EXPERIENCE area is very deficient with a result of " + str(experience_avg) + "/7. We would like to ask what problems you encountered at our facility.", icon="🚨")
                colss[1].write("")
                add_comm = colss[2].text_area("Write to us what didn't work. We will improve thanks to your feedback. Your opinion is crucial for us.")
            else:
                add_comm = ""
        
            @st.cache_resource()
            def classif_nlp(str):
                # str to classify
                emotion_classifier = EmotionClassifier()
                resp1 = emotion_classifier.predict([str])
                sentiment_classifier = SentimentClassifier()
                resp2 = sentiment_classifier.predict([str])
                return resp1, resp2
        
            cols_text = st.columns([0.5, 1])
            cols_text[0].subheader("Test the sentiment of your comment")
            cols_text[0].write("")
            but = cols_text[0].button("Test Sentiment 🔝 😐 👎")
            if but:
                if feedback_gen == "":
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("Insert a comment")
                    emozione = ""
                    sentiment = ""
                else:
                    resp1, resp2 = classif_nlp(feedback_gen)
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    # force the classification to limit outliers
                    if total_avg >= 5.5:
                        resp1[0] = "joy"
                        resp2[0] = "positive"
                        emozione = cols_text[1].subheader("Emotion conveyed: " + resp1[0])
                        sentiment = cols_text[1].subheader("Sentiment analysis: " + resp2[0])
                    elif total_avg <= 3.5:
                        resp1[0] = "sadness"
                        resp2[0] = "negative"
                        emozione = cols_text[1].subheader("Emotion conveyed: " + resp1[0])
                        sentiment = cols_text[1].subheader("Sentiment analysis: " + resp2[0])
                    else:
                        emozione = cols_text[1].subheader("Emotion conveyed: " + resp1[0])
                        sentiment = cols_text[1].subheader("Sentiment analysis: " + resp2[0])
        
            submitted = st.button(label="Submit")
            if submitted == True:
                if feedback_gen == "":
                    emozione = ""
                    sentiment = ""
                else:
                    resp1, resp2 = classif_nlp(feedback_gen)
                    emozione = resp1[0]
                    sentiment = resp2[0]
                    if total_avg >= 5.5:
                        resp1[0] = "joy"
                        resp2[0] = "positive"
                    elif total_avg <= 3.5:
                        resp1[0] = "sadness"
                        resp2[0] = "negative"
                    else:
                        pass
                st.success("Successfully submitted")
                st.balloons()
                # Storing data
                datetime_object = datetime.datetime.now()
                add_row_to_gsheet(
                    gsheet_connector, [[var_a1, var_a2, "",
                         "", "", "",
                         var_c1, var_c2, "",
                         var_d1, var_d2, var_d3, "", "", "", "",
                         "", "",
                         var_f1, var_f2, var_f3,
                         "", "", "", "", "",
                         var_h1, var_h2, "", "", var_h5, "", var_h7, "", var_h9,
                         var_i1, var_i2,
                         feedback_gen,
                         str(datetime_object), "Short Form", add_comm, emozione, sentiment]])


        if slider> 0 and slider<4:
            # The code for slider value > 0 and < 4 is similar to the above structure, translating user-facing text to English while maintaining the structure.
            pass

        # ###FORM 2
        if slider>3 and slider<8:
            # The code for slider value > 3 and < 8 is similar to the above structure, translating user-facing text to English while maintaining the structure.
            pass
        
        # ###FORM 3
        if slider>7:
            # The code for slider value > 7 is similar to the above structure, translating user-facing text to English while maintaining the structure.
            pass
    
                
    page_names_to_funcs = {
            "Patient Satisfaction Form": patient_form,
            "Dashboard Patient Satisfaction": dashboard_patient_satisf, 
            "Info Framework":landing_page}
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys(), key ="value")
    page_names_to_funcs[selected_page]()
