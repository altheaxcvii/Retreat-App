import streamlit as st
import time

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
            st.session_state.currentstage = 1
            st.success("You've unlocked the hint to your next stage!")
            st.info("Moving you to the next stage...")
            time.sleep(10)
            st.rerun()
        else:
            st.error('Invalid Code, Please Try Again!')