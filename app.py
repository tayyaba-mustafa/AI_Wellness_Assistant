import os
from groq import Groq
import streamlit as st
from gtts import gTTS
import datetime
import matplotlib.pyplot as plt

# Set your Groq API Key
API_KEY = "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"  # Replace with your actual key
if not API_KEY:
    st.error("API Key is missing. Please provide a valid GROQ_API_KEY.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Global storage for reminders and progress tracking
reminders = []
progress = {"mood": [], "fitness": [], "meditation": []}

# Function to interact with Gemma2-9b-it model
def query_gemma2(prompt, model="gemma2-9b-it"):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    return response.choices[0].message.content

# Mood tracking function
def analyze_mood(user_input):
    prompt = f"Analyze the mood from the following input and provide suggestions: '{user_input}'"
    response = query_gemma2(prompt)
    progress["mood"].append((user_input, response))
    return response

# Fitness plans function
def generate_fitness_plan(user_input):
    prompt = f"Generate a personalized fitness plan based on this input: '{user_input}'"
    response = query_gemma2(prompt)
    progress["fitness"].append((user_input, response))
    return response

# Meditation techniques function
def voice_guided_meditation():
    prompt = "Provide relaxation techniques for guided meditation."
    response = query_gemma2(prompt)
    
    # Convert text response to audio
    tts = gTTS(text=response, lang="en")
    audio_file = "meditation.mp3"
    tts.save(audio_file)  # Save audio to file
    
    progress["meditation"].append(response)
    return response, audio_file

# Reminder function
def set_reminder(reminder_text, time):
    reminder = {"text": reminder_text, "time": time}
    reminders.append(reminder)
    return f"Reminder set: '{reminder_text}' at {time}"

# Progress tracking function
def show_progress():
    mood_count = len(progress["mood"])
    fitness_count = len(progress["fitness"])
    meditation_count = len(progress["meditation"])
    
    # Generate a bar chart
    labels = ["Mood", "Fitness", "Meditation"]
    values = [mood_count, fitness_count, meditation_count]
    
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=["#ff9999", "#66b3ff", "#99ff99"])
    ax.set_title("Progress Overview")
    ax.set_ylabel("Number of Activities")
    
    return fig

# Streamlit UI
st.title("🧘‍♀️ AI Wellness Assistant 🧘‍♂️")
st.markdown("""
Welcome to the **AI Wellness Assistant**! This tool helps you track your mood, generate fitness plans, and enjoy voice-guided meditation.  
### Features:
- 🌈 **Mood Tracking**  
- 🏋️ **Fitness Plans**  
- 🧘‍♂️ **Voice-Guided Meditation**  
- 🔔 **Set Reminders**  
- 📊 **Progress Tracking**
""")

# Sidebar for navigation
with st.sidebar:
    st.header("Select a Feature:")
    option = st.radio(
        "Choose an option:",
        ["Mood Tracking", "Fitness Plans", "Voice-Guided Meditation", "Set Reminder", "Progress Tracking"]
    )

# Main Content
if option == "Mood Tracking":
    st.subheader("🌈 Mood Tracking")
    user_input = st.text_input("Enter how you are feeling today:")
    if st.button("Analyze Mood"):
        if user_input:
            response = analyze_mood(user_input)
            st.success(f"🤔 Mood Analysis: {response}")
        else:
            st.warning("Please enter your mood.")

elif option == "Fitness Plans":
    st.subheader("🏋️ Fitness Plans")
    user_input = st.text_input("Describe your fitness goals or current routine:")
    if st.button("Generate Fitness Plan"):
        if user_input:
            response = generate_fitness_plan(user_input)
            st.success(f"💪 Your Fitness Plan: {response}")
        else:
            st.warning("Please describe your fitness goals.")

elif option == "Voice-Guided Meditation":
    st.subheader("🧘‍♂️ Voice-Guided Meditation")
    if st.button("Start Meditation"):
        meditation_text, meditation_audio = voice_guided_meditation()
        st.success(f"🧘 Meditation Tips: {meditation_text}")
        st.audio(meditation_audio)

elif option == "Set Reminder":
    st.subheader("🔔 Set Reminder")
    reminder_text = st.text_input("Reminder Text:")
    reminder_time = st.text_input("Time (e.g., 14:00):")
    if st.button("Set Reminder"):
        if reminder_text and reminder_time:
            response = set_reminder(reminder_text, reminder_time)
            st.success(response)
        else:
            st.warning("Please provide both reminder text and time.")

elif option == "Progress Tracking":
    st.subheader("📊 Progress Tracking")
    fig = show_progress()
    st.pyplot(fig)
    st.markdown("Track your activities and keep improving! 🚀")

# Footer
st.markdown("---")
st.markdown("🌟 **Developed with ❤️ using Generative AI and Streamlit** 🌟")
