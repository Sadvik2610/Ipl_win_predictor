import streamlit as st
import pickle as pkl
import pandas as pd
import time

# Page config with wide layout
st.set_page_config(layout="wide")

# 🎨 Custom CSS for background image, overlay, and animated heading
st.markdown("""
    <style>
        .stApp {
            background: url('https://static.vecteezy.com/system/resources/thumbnails/040/344/638/small/ai-generated-an-empty-artificial-field-with-a-light-beam-free-photo.jpg') no-repeat center center fixed;  /* Background image URL */
            background-size: cover;  /* Ensure the image covers the whole screen */
            color: white;
        }

        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent black overlay */
            z-index: -1;
        }

        /* Animated IPL Prediction System heading */
        .stTitle {
            color: white !important;
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            animation: colorChange 5s infinite;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Adding a shadow for extra effect */
        }

        @keyframes colorChange {
            0% {
                color: #FF5733; /* Red */
            }
            25% {
                color: #33FF57; /* Green */
            }
            50% {
                color: #3357FF; /* Blue */
            }
            75% {
                color: #FF33A1; /* Pink */
            }
            100% {
                color: #FF5733; /* Red */
            }
        }

        .arrow-container {
            position: relative;
            width: 100%;
            height: 100px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .arrow-animation {
            position: absolute;
            left: -100%;  /* Initially off-screen */
            animation: slideIn 3s forwards;  /* Slide animation */
            font-size: 2em;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 20px;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        }

        @keyframes slideIn {
            0% {
                left: -100%;  /* Start off-screen to the left */
            }
            100% {
                left: 50%;  /* Move to the center (or right side) */
                transform: translateX(-50%);
            }
        }

        /* Add styles to the title and headers */
        .stButton>button {
            background-color: #007BFF;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Overlay for background image
st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)

# 🏆 Title with animated color
st.title("🏏 IPL Win Predictor", anchor="top")

# 📦 Load data and model
teams = pkl.load(open('team.pkl', 'rb'))
cities = pkl.load(open('city.pkl', 'rb'))
model = pkl.load(open('model.pkl', 'rb'))

# 🔘 First row inputs
col1, col2, col3 = st.columns(3)
with col1:
    batting_team = st.selectbox('Select the batting team', (teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', (teams))
with col3:
    selected_city = st.selectbox('Select the host city',(cities))

# 🎯 Target input
target = st.number_input('🎯 Target Score', min_value=0, max_value=720, step=1)

# ⏱ Match progress inputs
col4, col5, col6 = st.columns(3)
with col4:
    score = st.number_input('🏏 Current Score', min_value=0, max_value=720, step=1)
with col5:
    overs = st.number_input('⏱ Overs Done', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")
with col6:
    wickets_fell = st.number_input('❌ Wickets Fell', min_value=0, max_value=10, step=1)

# 🔮 Prediction logic
if st.button('Predict Probabilities'):
    # Simulate a short delay to let the animation run
    time.sleep(1)

    # Calculation for predictions
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    wickets = 10 - wickets_fell
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6 / balls_left) if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'Score': [score],
        'Wickets': [wickets],
        'Remaining Balls': [balls_left],
        'target_left': [runs_left],
        'crr': [crr],
        'rrr': [rrr]
    })

    # 🎯 Predict probabilities
    result = model.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    # 🎨 Determine colors based on win probability
    batting_color = "#4CAF50" if win > loss else "#FF4136"
    bowling_color = "#4CAF50" if loss > win else "#FF4136"

    # 🌟 Arrow animation with result coming in from the left
    st.markdown(f"""
        <div class="arrow-container">
            <div class="arrow-animation" style="background-color:{batting_color};">
                {batting_team} - {round(win * 100)}%
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="arrow-container">
            <div class="arrow-animation" style="background-color:{bowling_color};">
                {bowling_team} - {round(loss * 100)}%
            </div>
        </div>
    """, unsafe_allow_html=True)
