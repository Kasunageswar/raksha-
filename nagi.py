import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import time
from datetime import datetime
import pytz
import threading
import queue
import base64

# Initialize session state variables
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'emergency_contacts' not in st.session_state:
    st.session_state.emergency_contacts = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'last_location' not in st.session_state:
    st.session_state.last_location = None
if 'messages' not in st.session_state:
    st.session_state.messages = {}
if 'location_queue' not in st.session_state:
    st.session_state.location_queue = queue.Queue()
if 'danger_zones' not in st.session_state:
    st.session_state.danger_zones = [
        {"name": "Dark Alley", "lat": 40.7128, "lon": -74.0060, "radius": 0.01},
        {"name": "Isolated Park", "lat": 40.7500, "lon": -73.9967, "radius": 0.02},
    ]

# Updated Color scheme
PRIMARY_COLOR = "#E6E6FA"  # Light Purple (Lavender)
SECONDARY_COLOR = "#9370DB"  # Medium Purple
ACCENT_COLOR = "#4B0082"  # Indigo
TEXT_COLOR = "#4B0082"  # Indigo for text

def set_page_config():
    st.set_page_config(
        page_title="RAKSHA: Women's Safety App",
        page_icon="🛡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {PRIMARY_COLOR};
            color: {TEXT_COLOR};
        }}
        .stButton>button {{
            color: {PRIMARY_COLOR};
            background-color: {SECONDARY_COLOR};
            border: 2px solid {ACCENT_COLOR};
        }}
        .stTextInput>div>div>input {{
            color: {TEXT_COLOR};
        }}
        .sos-button {{
            font-size: 24px;
            padding: 20px 40px;
            background-color: red;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }}
        .stSelectbox>div>div>div {{
            background-color: {PRIMARY_COLOR};
            color: {TEXT_COLOR};
        }}
        .stTab {{
            background-color: {SECONDARY_COLOR};
            color: {PRIMARY_COLOR};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def login_page():
    st.subheader("Login to RAKSHA")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

def register_page():
    st.subheader("Register for RAKSHA")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    if st.button("Register"):
        if new_username in st.session_state.users:
            st.error("Username already exists")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Registration successful! Please log in.")

def simulate_gps():
    while True:
        lat = random.uniform(40.7000, 40.7500)
        lon = random.uniform(-74.0100, -73.9500)
        st.session_state.location_queue.put((lat, lon))
        time.sleep(5)

def update_location():
    simulate_gps()

def safe_routes(start_lat, start_lon, dest_lat, dest_lon):
    # This is a placeholder function. In a real app, you'd implement actual routing logic.
    return [
        [start_lat, start_lon],
        [(start_lat + dest_lat) / 2, (start_lon + dest_lon) / 2],
        [dest_lat, dest_lon]
    ]

def get_scream_audio():
    # This is a placeholder. In a real app, you'd host an actual audio file.
    audio_placeholder = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//tQwAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAACAAABhgC1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1//tQxAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAAEAAAI7AEJCQkJCYmJiYmJigoKCgoKDg4ODg4OSkpKSkpKnp6enp6fPz8/Pz8/m5ubm5ub/////////////////////////////////"
    return base64.b64decode(audio_placeholder)

def play_scream_sound():
    audio_file = get_scream_audio()
    st.audio(audio_file, format='audio/mp3')

def fake_call():
    st.write("Initiating fake call...")
    time.sleep(2)
    st.write("Incoming call from: Mom")
    st.button("Answer")
    st.button("Decline")

def check_danger_zones(lat, lon):
    for zone in st.session_state.danger_zones:
        distance = ((lat - zone['lat'])**2 + (lon - zone['lon'])**2)**0.5  # Corrected distance calculation
        if distance <= zone['radius']:
            return zone['name']
    return None

def emergency_services_quickdial():
    st.subheader("Emergency Services Quick Dial")
    if st.button("📞 Police"):
        st.write("Dialing 911...")
    if st.button("🚑 Ambulance"):
        st.write("Dialing 911...")
    if st.button("🚒 Fire Department"):
        st.write("Dialing 911...")

def safety_quiz():
    st.subheader("Safety Knowledge Quiz")
    score = 0
    questions = [
        {
            "question": "What should you do if you feel you're being followed?",
            "options": ["Keep walking quietly", "Run as fast as you can", "Head to a well-lit, populated area", "Confront the follower"],
            "correct": 2
        },
        {
            "question": "Which of these is NOT a good safety practice when using ride-sharing apps?",
            "options": ["Verify the driver's identity", "Share your trip details with a friend", "Sit in the front seat", "Check the vehicle's make and model"],
            "correct": 2
        },
        {
            "question": "What's the best way to hold your keys for self-defense?",
            "options": ["In your pocket", "In your purse", "Between your fingers", "In a closed fist with one key extended"],
            "correct": 3
        }
    ]
    for i, q in enumerate(questions):
        st.write(f"Q{i+1}: {q['question']}")
        answer = st.radio(f"Select your answer for Q{i+1}:", q['options'], key=f"q{i}")
        if st.session_state[f"q{i}"] == q['correct']:
            score += 1
    
    if st.button("Submit Quiz"):
        st.write(f"Your score: {score}/{len(questions)}")
        if score == len(questions):
            st.success("Great job! You're well-prepared for staying safe.")
        else:
            st.info("Good effort! Review the correct answers to improve your safety knowledge.")

def main_app():
    st.title(f"Welcome to RAKSHA, {st.session_state.username}")
    
    menu = ["Home", "Live Tracking", "Safe Routes", "Emergency Contacts", "Safety Tips", "Messaging", "Scream Alert", "Fake Call", "Emergency Services", "Safety Quiz"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.write("Welcome to RAKSHA: Your Personal Safety Companion. Use the menu to access different features.")
        st.markdown(f'<h3 style="color:{ACCENT_COLOR};">Stay safe and connected with RAKSHA!</h3>', unsafe_allow_html=True)
        
        if st.button("SOS", key="sos_button", help="Click in case of emergency"):
            st.error("SOS ALERT SENT TO ALL EMERGENCY CONTACTS")
            if st.session_state.last_location:
                lat, lon = st.session_state.last_location
                st.write(f"Last known location: Lat {lat:.4f}, Lon {lon:.4f}")
            st.markdown(f'<h2 style="color:{ACCENT_COLOR};">Stay calm. Help is on the way!</h2>', unsafe_allow_html=True)
    
    elif choice == "Live Tracking":
        st.subheader("Your Current Location")
        if not st.session_state.last_location:
            st.warning("Fetching location...")
            threading.Thread(target=update_location).start()
        lat, lon = st.session_state.location_queue.get() if not st.session_state.location_queue.empty() else (None, None)
        st.session_state.last_location = (lat, lon)
        st.write(f"Latitude: {lat}, Longitude: {lon}")
        
        map_center = [lat, lon] if lat and lon else [40.7128, -74.0060]
        folium_map = folium.Map(location=map_center, zoom_start=14)
        folium.Marker(location=map_center, popup="You are here!").add_to(folium_map)
        for zone in st.session_state.danger_zones:
            folium.Circle(location=[zone['lat'], zone['lon']], radius=zone['radius']*1000, color='red', fill=True, fill_opacity=0.5, popup=zone['name']).add_to(folium_map)
        folium_static(folium_map)
        
        if lat and lon:
            danger_zone = check_danger_zones(lat, lon)
            if danger_zone:
                st.warning(f"You are entering a danger zone: {danger_zone}")
    
    elif choice == "Safe Routes":
        st.subheader("Find Safe Routes")
        start_lat = st.number_input("Start Latitude", value=40.7128)
        start_lon = st.number_input("Start Longitude", value=-74.0060)
        dest_lat = st.number_input("Destination Latitude", value=40.7306)
        dest_lon = st.number_input("Destination Longitude", value=-73.9352)
        
        if st.button("Get Safe Route"):
            route = safe_routes(start_lat, start_lon, dest_lat, dest_lon)
            st.write("Safe Route Coordinates:")
            for point in route:
                st.write(f"Latitude: {point[0]}, Longitude: {point[1]}")
    
    elif choice == "Emergency Contacts":
        st.subheader("Manage Emergency Contacts")
        contact_name = st.text_input("Contact Name")
        contact_number = st.text_input("Contact Number")
        if st.button("Add Contact"):
            st.session_state.emergency_contacts[contact_name] = contact_number
            st.success(f"Added {contact_name} to emergency contacts.")
        
        if st.button("Show Contacts"):
            st.write("Emergency Contacts:")
            for name, number in st.session_state.emergency_contacts.items():
                st.write(f"{name}: {number}")
    
    elif choice == "Safety Tips":
        st.subheader("Safety Tips")
        st.write("1. Stay aware of your surroundings.")
        st.write("2. Trust your instincts.")
        st.write("3. Avoid isolated areas.")
        st.write("4. Keep your phone charged.")
        st.write("5. Use safety apps to stay connected.")
    
    elif choice == "Messaging":
        st.subheader("Messaging")
        recipient = st.text_input("Recipient")
        message = st.text_area("Message")
        if st.button("Send Message"):
            if recipient and message:
                st.session_state.messages[recipient] = message
                st.success("Message sent!")
            else:
                st.error("Please enter both recipient and message.")
    
    elif choice == "Scream Alert":
        st.subheader("Scream Alert")
        if st.button("Play Scream Sound"):
            play_scream_sound()
    
    elif choice == "Fake Call":
        st.subheader("Fake Call")
        if st.button("Initiate Fake Call"):
            fake_call()
    
    elif choice == "Emergency Services":
        emergency_services_quickdial()
    
    elif choice == "Safety Quiz":
        safety_quiz()

set_page_config()

# Main app flow
if st.session_state.logged_in:
    main_app()
else:
    login_or_register = st.sidebar.radio("Select", ("Login", "Register"))
    if login_or_register == "Login":
        login_page()
    else:
        register_page()
