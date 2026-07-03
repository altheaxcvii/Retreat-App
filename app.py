import streamlit as st
import time
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime
import io

@st.cache_resource
def get_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    return client.open("RO Retreat 2026").worksheet("Sheet1")

@st.cache_resource
def get_stations():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open("RO Retreat 2026").worksheet("Stations")
    group_data = sheet.row_values(2)
    headers = sheet.row_values(1)
    stationinfo = dict(zip(headers, group_data))
    return stationinfo

@st.cache_resource
def get_drive_service():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    return build("drive", "v3", credentials=creds)


def upload_photo(uploaded_file, folder_id, filename):
    drive = get_drive_service()
    file_metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    media = MediaIoBaseUpload(
        io.BytesIO(uploaded_file.getvalue()),
        mimetype=uploaded_file.type,
        resumable=False
    )
    file = drive.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    return file["id"]

def unlockhint(stageno):
    if stageno == '1':
        picture = st.camera_input("📸 Take a team photo! Line up from the first person who joined RO to the most recent member to unlock the next hint.")
        if picture:
            if st.button('Unlock hint'):
                upload_photo(picture, "1oo3VegWPYtbg_0xeyl0jVO4FPiI5gfNT", f"{st.session_state.group_data['Group Name']}_stage1_{datetime.now():%Y%m%d%H%M%S}.jpg")
    
def stationdetails(stationno, stageno):
    stationinfo = get_stations()
    if stationno == "1":
        with st.expander(f"🗺️ Your clue for stage {stageno}"):
            st.text(f"{stationinfo['Station 1 Prompt 1']}")
            st.warning("🙅🏻‍♀️ Please don't outsource your brain to AI. We believe in you.")
            st.warning('🧋 If ChatGPT solves this for you, your team owes the Retreat team bubble tea.')
        with st.expander(f"💡 Need another hint?"):
            if st.session_state.hint=='TRUE':
                st.image(f"{stationinfo['Station 1 Prompt 2']}", caption='Good luck!😂')
            else:
                unlockhint(stageno)
        station1pw = st.text_input("What is the word you see on the board?", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station1pw.strip().upper() == stationinfo['Station 1 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1 
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')

    if stationno == "2":
        with st.expander(f"🧩 Primary clue for stage {stageno}"):
            st.text(f"{stationinfo['Station 2 Prompt 1']}")
        with st.expander(f"🚪 Bonus clue"):
            st.image(f"{stationinfo['Station 2 Prompt 2']}", caption='Extra hint')
        station2pw = st.text_input("What does PASS operate?", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station2pw.strip().upper() == stationinfo['Station 2 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1 
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')
    
    if stationno == "3":
        st.write(f"Here's the hint for your stage {stationno}: {stationinfo['Station 3 Prompt 1']}")
        station3pw = st.text_input("What is the word you see on the wall?", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station3pw.strip().upper() == stationinfo['Station 3 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1 
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')

    if stationno == "4":
        st.write(f"Here's the hint for your stage {stationno}: {stationinfo['Station 4 Prompt 1']}")
        station4pw = st.text_input("What is the word you see on the wall?", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station4pw.strip().upper() == stationinfo['Station 4 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1 
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')

    if stationno == "5":
        st.write(f"Here's the hint for your stage {stationno}: {stationinfo['Station 5 Prompt 1']}")
        st.write(f"Here's another hint for your stage {stationno}: {stationinfo['Station 5 Prompt 2']}")
        station5pw = st.text_input("What is the weight of the machine?", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station5pw.strip().upper() == stationinfo['Station 5 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')

    if stationno == "6":
        with st.expander(f"💡 Small Hint for your stage {stageno}"):
            col1, col2 = st.columns(2)
            with col1:
                st.text(f"{stationinfo['Station 6 Prompt 1.1']}")
            with col2:
                st.text(f"{stationinfo['Station 6 Prompt 1.2']}")
            st.write("Clue: ✺☁ ⚑☾ ☯⌬ ☼⌬ ☯⌬ ⚑☾ ⌬◇ ☼⌬ ✺☁ ✺☁")
        with st.expander(f"🚨 Bigger Hint"):
            st.image(f"{stationinfo['Station 6 Prompt 2']}", caption='Extra hint')
        station6pw = st.text_input("The courier waits where orange doors sleep. Do not seek the name. Seek its language. Only those who crack the courier's alphabet will know where the next clue lies.", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station6pw.strip().upper() == stationinfo['Station 6 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1 
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')

    if stationno == "7":
        st.write(f"Here's the hint for your stage {stationno}: {stationinfo['Station 7 Prompt 1']}")
        station7pw = st.text_input("What is the word you see on the wall?", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station7pw.strip().upper() == stationinfo['Station 7 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1 
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')

    if stationno == "8":
        st.write(f"Here's the hint for your stage {stationno}: {stationinfo['Station 8 Prompt 1']}")
        station8pw = st.text_input("What is the word you see on the wall?", placeholder='Enter your answer')
        if st.button("Submit Password"):
            if station8pw.strip().upper() == stationinfo['Station 8 Password']:
                st.balloons()
                st.success('CONGRATS ON UNLOCKING THE NEXT HINT! Moving you to the next page...', icon='🎉')
                st.session_state.currentstage += 1 
                sheet = get_sheet()
                sheet.update_cell(st.session_state.grouprow, 3, st.session_state.currentstage)
                sheet.update_cell(st.session_state.grouprow, 9, False)
                st.session_state.hint = False
                time.sleep(3)
                st.rerun()
            else:
                st.error('Wrong Password, please try again...', icon='🙅🏻‍♂️')

st.set_page_config(page_title='RO Retreat 2026', page_icon='🔎')
st.image("Assets/banner.jpg")
#st.header('📍 RO Retreat 2026')

if 'currentstage' not in st.session_state:
    st.session_state.currentstage = 0

if st.session_state.currentstage > 0:
    with st.expander('You may need this 😊'):
        st.markdown("[🗺️ SIT Map to help you Navigate](https://www.singaporetech.edu.sg/campus-wayfinder)")
        st.markdown("[🎵 Don't get stressed](https://youtu.be/z27LnN6SeK4?si=iD08iTwACo5KkrFy&t=46)")

if st.session_state.currentstage == 0:
    groupcode = st.text_input('🔐 Unlock your mission by entering your group code', max_chars=3)
    if st.button('Submit group code'):
        groupcodedict = {'abc':'grp1',
                         'def':'grp2',
                         'ghi':'grp3',
                         'jkl':'grp4',
                         'mno':'grp5',
                         'pqr':'grp6',
                         'stu':'grp7'}
        if groupcode in groupcodedict:
            st.session_state.groupcode = groupcodedict[groupcode]
            
            sheet = get_sheet()
            st.session_state.grouprow = sheet.find(str(st.session_state.groupcode)).row

            group_data = sheet.row_values(st.session_state.grouprow)
            headers = sheet.row_values(1)
            st.session_state.group_data = dict(zip(headers, group_data))

            if int(st.session_state.group_data['Current Stage']) > 0:
                st.success('Teleporting you back to where you left off!')
                st.session_state.currentstage = int(st.session_state.group_data['Current Stage'])
                st.session_state.hint = st.session_state.group_data['Hint']
            else:
                st.success("You've unlocked the hint to your next stage!")
                st.info("🔓 Unlocking the doors for you, please wait...")
                st.session_state.currentstage = 0.5
            #time.sleep(3)
            st.rerun()
        else:
            st.error('Invalid Code, Please Try Again!')

if st.session_state.currentstage == 0.5:
    grpname = st.text_input('Enter a group name')
    if st.button('Submit group name'):
        if grpname.strip():
            st.session_state.currentstage = 1
            sheet = get_sheet()
            sheet.update_cell(st.session_state.grouprow, 3, 1)
            sheet.update_cell(st.session_state.grouprow, 2, grpname.strip())
            group_data = sheet.row_values(st.session_state.grouprow)
            headers = sheet.row_values(1)
            st.session_state.group_data = dict(zip(headers, group_data))
            st.session_state.hint = st.session_state.group_data['Hint']
            st.rerun()
        else:
            st.error('Please enter a name')

if st.session_state.currentstage == 1:
    st.header(f'🎉 Welcome, {st.session_state.group_data['Group Name']}!')
    st.write('Your adventure starts here.')
    st.write('Study the clue below and work together to identify the first location. Once you arrive, search carefully for the password and enter it here to unlock the next stage.')
    st.write("Good luck, you've got this!")
    stationdetails(st.session_state.group_data['Stage 1'], '1')

if st.session_state.currentstage == 2:
    st.header(f"🚀 Great job, {st.session_state.group_data['Group Name']}! One station down.")
    st.write('The next clue is waiting below. Head to the location, keep your eyes peeled for the password, and enter it here to continue your journey.')
    st.write("Every clue brings you one step closer to the finish!")
    stationdetails(st.session_state.group_data['Stage 2'], '2')

if st.session_state.currentstage == 3:
    st.header(f"🧩 You're making great progress, {st.session_state.group_data['Group Name']}!")
    st.write('Time for your next challenge. Follow the clue, locate the station, and uncover the password hidden there.')
    st.write("Work together, sometimes the smallest details hold the biggest clues.")
    stationdetails(st.session_state.group_data['Stage 3'], '3')

if st.session_state.currentstage == 4:
    st.header(f"💪 You're on a roll, {st.session_state.group_data['Group Name']}!")
    st.write('Only a little more to go. Solve the clue, find the next location, and discover the password waiting for your team.')
    st.write("Stay curious, stay observant, and enjoy the journey!")
    stationdetails(st.session_state.group_data['Stage 4'], '4')

if st.session_state.currentstage == 5:
    st.header(f"🏁 This is your last mission, {st.session_state.group_data['Group Name']}!")
    st.write('One final clue stands between you and the finish. Find the location, uncover the password, and unlock your final destination.')
    st.write("Finish strong, you've almost made it!")
    stationdetails(st.session_state.group_data['Stage 5'], '5')

if st.session_state.currentstage == 6:
    st.header(f'Congratulations, {st.session_state.group_data['Group Name']}! You may now proceed to the final destination!')
    with st.expander('👀 A whisper from your guide...'):
        st.write("Your next destination is a place reserved not for today's students, but yesterday's.")
    with st.expander('✨ The guide reveals a little more...'):
        st.write('Sodium hydroxide')
        st.write('Calcium hydroxide')
        st.write('Magnesium hydroxide')