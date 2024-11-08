import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from io import BytesIO

# Configure Google Generative AI
genai.configure(api_key="AIzaSyCJ_toTzdFF5nsBDKiIrbzkuYJ3-LjVu7M")  # Replace with your actual API key

# Define generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1024
}

# Initialize Speech Recognition
recognizer = sr.Recognizer()

# Streamlit page settings
st.set_page_config(page_title="Generative AI Chatbot", layout="wide", initial_sidebar_state="collapsed")
st.title("🤖 Generative AI Chatbot")

# Dark theme styling
st.markdown("<style>body { background-color: #1e1e1e; color: #ffffff; }</style>", unsafe_allow_html=True)
st.markdown("""
    <style>
        .stApp { background-color: #1e1e1e; color: white; }
        .stButton>button {
            background-color: #3d5afe;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #536dfe;
            color: white;
        }
        .stTextInput>input {
            background-color: #2b2b2b;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for voice input option
with st.sidebar:
    st.header("Settings")
    use_voice = st.checkbox("Enable Voice Input")

# Function to handle audio file input
def process_audio(audio_file):
    audio_data = sr.AudioFile(audio_file)
    with audio_data as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.warning("Could not understand the audio")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
    return None

# Prompt input section
st.subheader("Enter your prompt:")

# Display audio file uploader if voice input is enabled
prompt = ""
if use_voice:
    st.write("Upload an audio file for voice input:")
    uploaded_audio = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])
    if uploaded_audio is not None:
        st.success("Audio file uploaded!")
        prompt = process_audio(uploaded_audio)

# Display text input for prompt
text_input = st.text_area("Prompt", prompt, height=150)

# Generate response on button click
if st.button("Generate Response"):
    if text_input:
        st.info("Generating response...")
        try:
            # Generate response using Generative AI
            model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
            response = model.generate_content(text_input)
            response_text = response.text

            st.subheader("AI Response:")
            st.write(response_text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt or use the voice input.")

# Footer
st.markdown("---")
st.markdown("<center><small>Powered by Google Generative AI API</small></center>", unsafe_allow_html=True)
