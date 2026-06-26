import streamlit as st
import time
import gspread
from google.oauth2.service_account import Credentials


st.set_page_config(page_title='RO Retreat 2026', page_icon='🔎')
st.header('📍 RO Retreat 2026')

if 'currentstage' not in st.session_state:
    st.session_state.currentstage = 0

if st.session_state.currentstage == 0:
    groupcode = st.text_input('🔐 Unlock your mission by entering your group code', max_chars=3)
    if st.button('Submit group code'):
        groupcodedict = {'abc':1,
                         'def':2,
                         'ghi':3,
                         'jkl':4,
                         'mno':5,
                         'pqr':6,
                         'stu':7}
        if groupcode in groupcodedict:
            st.session_state.groupcode = groupcodedict[groupcode]
            
            st.success("You've unlocked the hint to your next stage!")
            st.info("Moving you to the next stage...")
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=scope
            )

            client = gspread.authorize(creds)

            sheet = client.open("RO Retreat 2026").worksheet("Sheet1")
            cell = sheet.find(str(st.session_state.groupcode))
            row = cell.row

            group_data = sheet.row_values(row)
            headers = sheet.row_values(1)

            group_data = dict(zip(headers, group_data))

            st.session_state.group_data = group_data
            st.session_state.currentstage = 1
            time.sleep(10)
            st.rerun()
        else:
            st.error('Invalid Code, Please Try Again!')

if st.session_state.currentstage == 1:
    st.header(f'Welcome to Stage 1, {st.session_state.group_data['Group Name']}!')
    st.write('Your team is tasked to look for the first location with the hint below, and enter the password to get the hint for the next location!')