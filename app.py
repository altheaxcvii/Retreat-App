import streamlit as st
import time
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

if 'currentstage' not in st.session_state:
    st.session_state.currentstage = 0
    st.session_state.buttonstate = False
    st.session_state.wrongpwmsg = False

if st.session_state.wrongpwmsg == True:
    st.toast('Wrong Password, please try again...', icon='🙅🏻‍♂️', duration='long')
    st.session_state.wrongpwmsg = False

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
def get_logs():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    return client.open("RO Retreat 2026").worksheet("Logs")

def log_action(group_name, action, answer):
    logs = get_logs()
    logs.append_row([
        group_name,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        action,
        answer])

def hintstatus(change, grouprow):
    sheet = get_sheet()
    if change == "Unlocked":
        sheet.update_cell(grouprow, 9, "TRUE")
        st.session_state.hint = "TRUE"
        buttonstatechange("Enabled")
    if change == "Locked":
        sheet.update_cell(grouprow, 9, "FALSE")
        st.session_state.hint = "FALSE"

def buttonstatechange(buttonstate):
    if buttonstate == "Enabled":
        st.session_state.buttonstate = False
    if buttonstate == "Disabled":
        st.session_state.buttonstate = True

def unlockhint(stageno):
    if stageno == '1':
        st.write('🪑 So you think you know the office well? As a team, come to a best guess on how many chairs are there in the RO office space to unlock this hint.')
        chairs = st.number_input('How many chairs do your team thinks there are?', min_value=1, max_value=100)
        if st.button('Record our guess!', disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            log_action(st.session_state.group_data['Group Name'], "Unlocked Stage 1 Extra Hint", chairs)
            hintstatus("Unlocked", st.session_state.grouprow)
            st.rerun()

    if stageno == '2':
        st.write("📸 Take a team photo! Line up from the first person who joined RO to the most recent member to unlock this hint.")
        st.write("Post it on RO Whatsapp Chat to proceed.")
        if st.button('Photo sent!', disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            log_action(st.session_state.group_data['Group Name'], "Unlocked Stage 2 Extra Hint", "Check WA Grp for Photo")
            hintstatus("Unlocked", st.session_state.grouprow)
            st.rerun()

    if stageno == '3':
        st.write("🍜 Every team member should share their favourite place to eat near the office to unlock this hint.")
        food = st.text_input('As a team, submit one recommendation that everyone should try.')
        if st.button('Share our recommendation!', disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            log_action(st.session_state.group_data['Group Name'], "Unlocked Stage 3 Extra Hint", food)
            hintstatus("Unlocked", st.session_state.grouprow)
            st.rerun()

    if stageno == '4':
        st.write("🎖️ To unlock this hint, work together to invent a fictional RO award and decide who should receive it!")
        award = st.text_input('We will like to give out ____ to ____.')
        if st.button('Submit our award!', disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            log_action(st.session_state.group_data['Group Name'], "Unlocked Stage 4 Extra Hint", award)
            hintstatus("Unlocked", st.session_state.grouprow)
            st.rerun()

    if stageno == '5':
        st.write("🪄 As a team, discuss the following scenario and agree on one option.")
        st.write("Don't worry—it's purely hypothetical! 😄")
        topchoice = st.selectbox("Which deal would your team accept to unlock the next hint?", ['Never receive another email, but every message becomes a Teams call',
                                                                                                'Permanent WFH, but your camera must always stay on',
                                                                                                'Free lunch every office day, but your boss chooses what you eat',
                                                                                                "You get your own private office, but there's no air-conditioning",
                                                                                                'Get one extra month of annual leave every year, but your team choose all your leave dates'])
        if st.button('We made our choice!', disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            log_action(st.session_state.group_data['Group Name'], "Unlocked Stage 5 Extra Hint", topchoice)
            hintstatus("Unlocked", st.session_state.grouprow)
            st.rerun()

    if stageno == '6':
        st.write("📸 Take a dramatic team selfie to unlock this final hint.")
        st.write("Post it on RO Whatsapp Chat to proceed.")
        if st.button('Photo sent!', on_click=buttonstatechange("Disabled")):
            log_action(st.session_state.group_data['Group Name'], "Unlocked Stage 6 Extra Hint", "Check WA Grp for Photo")
            hintstatus("Unlocked", st.session_state.grouprow)
            st.rerun()

def completestage(grouprow):
    sheet = get_sheet()
    st.session_state.currentstage += 1
    sheet.update_cell(grouprow, 3, st.session_state.currentstage)
    time.sleep(2)
    buttonstatechange("Enabled")
    st.rerun()

def wrongpw():
    buttonstatechange("Enabled")
    st.session_state.wrongpwmsg = True
    st.rerun()

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
        if st.button("Submit Password", disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            if station1pw.strip().upper() == stationinfo['Station 1 Password']:
                st.balloons()
                st.toast(f'CONGRATS ON CLEARING STAGE {stageno}! Please wait...', icon='🎉', duration='long')
                log_action(st.session_state.group_data['Group Name'], f"Cleared stage {stageno}", f"Station {stationno}")
                hintstatus("Locked", st.session_state.grouprow)
                completestage(st.session_state.grouprow)
            else:
                wrongpw()

    if stationno == "2":
        with st.expander(f"🧩 Primary clue for stage {stageno}"):
            st.text(f"{stationinfo['Station 2 Prompt 1']}")
        
        with st.expander(f"🚪 Bonus clue"):
            if st.session_state.hint=='TRUE':
                st.image(f"{stationinfo['Station 2 Prompt 2']}", caption='Extra hint')
            else:
                unlockhint(stageno)
            
        station2pw = st.text_input("What does PASS operate?", placeholder='Enter your answer')
        if st.button("Submit Password", disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            if station2pw.strip().upper() == stationinfo['Station 2 Password']:
                st.balloons()
                st.toast(f'CONGRATS ON CLEARING STAGE {stageno}! Please wait...', icon='🎉', duration='long')
                log_action(st.session_state.group_data['Group Name'], f"Cleared stage {stageno}", f"Station {stationno}")
                hintstatus("Locked", st.session_state.grouprow)
                completestage(st.session_state.grouprow)
            else:
                wrongpw()
    
    if stationno == "3":
        with st.expander(f'Hint 1: Find your destination for stage {stageno}'):
            st.image(stationinfo['Station 3 Prompt 1'], caption="Doesn't this look familiar?")

        with st.expander(f'Hint 2: Need a bigger nudge?'):
            if st.session_state.hint=='TRUE':
                st.write(f"{stationinfo['Station 3 Prompt 2']}")
            else:
                unlockhint(stageno)

        station3pw = st.text_input("What is the shirt color of the guy playing the erhu, and the photographer? Enter the answer as two separate words, with a space in between, no punctuations", placeholder='COLOR1 COLOR2')
        if st.button("Submit Password", disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            if station3pw.strip().upper() == stationinfo['Station 3 Password']:
                st.balloons()
                st.toast(f'CONGRATS ON CLEARING STAGE {stageno}! Please wait...', icon='🎉', duration='long')
                log_action(st.session_state.group_data['Group Name'], f"Cleared stage {stageno}", f"Station {stationno}")
                hintstatus("Locked", st.session_state.grouprow)
                completestage(st.session_state.grouprow)
            else:
                wrongpw()

    if stationno == "4":
        with st.expander('🎯 Step 1: Find your next location'):
            st.text(f"{stationinfo['Station 4 Prompt 1']}")
            st.image(stationinfo['Station 4 Image 1'])
            st.image(stationinfo['Station 4 Image 2'])
        
        with st.expander('💡 Step 2: Still searching?'):
            if st.session_state.hint=='TRUE':
                st.image(stationinfo['Station 4 Image 3'], caption=stationinfo['Station 4 Prompt 2'])
            else:
                unlockhint(stageno)

        station4pw = st.text_input("What is the password?", placeholder='Enter your answer')
        if st.button("Submit Password", disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            if station4pw.strip().upper() == stationinfo['Station 4 Password']:
                st.balloons()
                st.toast(f'CONGRATS ON CLEARING STAGE {stageno}! Please wait...', icon='🎉', duration='long')
                log_action(st.session_state.group_data['Group Name'], f"Cleared stage {stageno}", f"Station {stationno}")
                hintstatus("Locked", st.session_state.grouprow)
                completestage(st.session_state.grouprow)
            else:
                wrongpw()

    if stationno == "5":
        with st.expander('👀 A whisper from your guide...'):
            st.text(f"{stationinfo['Station 5 Prompt 1']}")
        
        with st.expander('✨ The guide reveals a little more...'):
            if st.session_state.hint=='TRUE':
                st.write(f"{stationinfo['Station 5 Prompt 2']}")
            else:
                unlockhint(stageno)

        station5pw = st.text_input("What is the weight of the machine?", placeholder='Enter your answer in xxxKG, no space in between please')
        if st.button("Submit Password", disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            if station5pw.strip().upper() == stationinfo['Station 5 Password']:
                st.balloons()
                st.toast(f'CONGRATS ON CLEARING STAGE {stageno}! Please wait...', icon='🎉', duration='long')
                log_action(st.session_state.group_data['Group Name'], f"Cleared stage {stageno}", f"Station {stationno}")
                hintstatus("Locked", st.session_state.grouprow)
                completestage(st.session_state.grouprow)
            else:
                wrongpw()

    if stationno == "6":
        with st.expander(f"💡 Small Hint for your stage {stageno}"):
            col1, col2 = st.columns(2)
            with col1:
                st.text(f"{stationinfo['Station 6 Prompt 1.1']}")
            with col2:
                st.text(f"{stationinfo['Station 6 Prompt 1.2']}")
            st.write("Clue: ✺☁ ⚑☾ ☯⌬ ☼⌬ ☯⌬ ⚑☾ ⌬◇ ☼⌬ ✺☁ ✺☁")

        with st.expander(f"🚨 Bigger Hint"):
            if st.session_state.hint=='TRUE':
                st.image(f"{stationinfo['Station 6 Prompt 2']}", caption='Extra hint')
            else:
                unlockhint(stageno)

        station6pw = st.text_input("The courier waits where orange doors sleep. Do not seek the name. Seek its language. Only those who crack the courier's alphabet will know where the next clue lies.", placeholder='Enter your answer')
        if st.button("Submit Password", disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            if station6pw.strip().upper() == stationinfo['Station 6 Password']:
                st.balloons()
                st.toast(f'CONGRATS ON CLEARING STAGE {stageno}! Please wait...', icon='🎉', duration='long')
                log_action(st.session_state.group_data['Group Name'], f"Cleared stage {stageno}", f"Station {stationno}")
                hintstatus("Locked", st.session_state.grouprow)
                completestage(st.session_state.grouprow)
            else:
                wrongpw()

    if stationno == "7":
        with st.expander(f'🏴‍☠️ Open Hint 1 for stage {stageno}'):
            st.text(f"{stationinfo['Station 7 Prompt 1']}")
            st.image(stationinfo['Station 7 Image 1'])
        
        with st.expander('💎 Still stuck? Open Hint 2'):
            if st.session_state.hint=='TRUE':
                st.image(stationinfo['Station 7 Prompt 2'], caption="Here's another clue!")
            else:
                unlockhint(stageno)

        station7pw = st.text_input("What is the password?", placeholder='Enter your answer')
        if st.button("Submit Password", disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
            if station7pw.strip().upper() == stationinfo['Station 7 Password']:
                st.balloons()
                st.toast(f'CONGRATS ON CLEARING STAGE {stageno}! Please wait...', icon='🎉', duration='long')
                log_action(st.session_state.group_data['Group Name'], f"Cleared stage {stageno}", f"Station {stationno}")
                hintstatus("Locked", st.session_state.grouprow)
                completestage(st.session_state.grouprow)
            else:
                wrongpw()

st.set_page_config(page_title='RO Retreat 2026', page_icon='🔎')
st.image("Assets/BANNER.png")

if st.session_state.currentstage >= 1:
    with st.expander('You may need this 😊'):
        st.markdown("[🗺️ SIT Map to help you Navigate](https://www.singaporetech.edu.sg/campus-wayfinder)")

if st.session_state.currentstage == 0:
    groupcode = st.text_input('🔐 Unlock your mission by entering your group code', max_chars=6)
    if st.button('Submit group code', disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
        groupcodedict = {'OFFICE':'grp1',
                         'POLICY':'grp2',
                         'DEGREE':'grp3',
                         'GRADES':'grp4',
                         'CAMPUS':'grp5',
                         'MODULE':'grp6',
                         'COHORT':'grp7',
                         'DEMOG1':'demo1',
                         'DEMOG2':'demo2',
                         'DEMOG3':'demo3',
                         'DEMOG4':'demo4',
                         'DEMOG5':'demo5'}
        if groupcode.upper() in groupcodedict:
            st.session_state.groupcode = groupcodedict[groupcode.upper()]
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
            time.sleep(2)
            buttonstatechange("Enabled")
            st.rerun()
        else:
            wrongpw()

if st.session_state.currentstage == 0.5:
    grpname = st.text_input('Enter a group name')
    if st.button('Submit group name', disabled=st.session_state.buttonstate, on_click=buttonstatechange("Disabled")):
        if grpname.strip():
            st.session_state.currentstage = 1
            sheet = get_sheet()
            sheet.update_cell(st.session_state.grouprow, 3, 1)
            sheet.update_cell(st.session_state.grouprow, 2, grpname.strip())
            group_data = sheet.row_values(st.session_state.grouprow)
            headers = sheet.row_values(1)
            st.session_state.group_data = dict(zip(headers, group_data))
            st.session_state.hint = st.session_state.group_data['Hint']
            buttonstatechange("Enabled")
            st.rerun()
        else:
            buttonstatechange("Enabled")
            st.rerun()

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
    with st.expander('😄 A very generous hint'):
        st.write("Your next destination is a place reserved not for today's students, but yesterday's.")
    
    with st.expander('✨ In case you need a bit more help...'):
        if st.session_state.hint=='TRUE':
            st.write('Sodium hydroxide')
            st.write('Calcium hydroxide')
            st.write('Magnesium hydroxide')
        else:
            unlockhint('6')
