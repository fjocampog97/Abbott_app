import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI , OpenAI
from langchain_openai import OpenAI
from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain_experimental.utilities import PythonREPL
from langchain.agents.agent_types import AgentType
import os
import sys
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import threading
import time
from io import BytesIO
import pyaudio

os.environ["OPENAI_API_KEY"] = "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"

def initialize_csv_agent():

    # Obtiene la ruta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta completa al archivo CSV dentro del directorio 'data'
    csv_path = os.path.join(script_dir, 'data', 'Datos_abbott_Vf.csv')
    OpenAI.api_key = "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"
    agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        csv_path,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True
    )
    return agent


# Inicializar el agente
agent = initialize_csv_agent()


# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Función para enviar un mensaje
def send_message(user_input_text):
    # Mostrar mensaje del usuario
    st.write(f"**Usuario:** {user_input_text}")

    # Mostrar mensaje "pensando"
    thinking_msg = st.empty()
    thinking_msg.write("**REP.AI:** Pensando...")

    # Obtener respuesta del agente y traducirla
    response = agent.run(user_input_text)
    response = GoogleTranslator(source='english', target='spanish').translate(response)

    # Actualizar mensaje "pensando" con la respuesta del agente
    thinking_msg.write(f"**REP.AI:** {response}")

    # Reproducir respuesta en audio
    play_audio(response)

# Función para reproducir audio
def play_audio(response):
    tts = gTTS(text=response, lang='es')
    tts.save("response.mp3")
    st.audio("response.mp3", format='audio/mp3')

# Función para iniciar grabación de voz
def start_voice_recording():
    with sr.Microphone() as source:
        st.write("**Escuchando...**")
        audio = recognizer.listen(source, timeout=5)
    try:
        st.write("**Reconociendo...**")
        user_input_text = recognizer.recognize_google(audio, language="es-ES")
        st.write(f"**Usuario:** {user_input_text}")
        send_message_voice(user_input_text)
    except sr.UnknownValueError:
        st.write("**No se pudo entender el audio**")
    except sr.RequestError as e:
        st.write(f"**Error al solicitar resultados:** {e}")

# Función para enviar mensaje de voz
def send_message_voice(user_input_text):
    st.write("**REP.AI:** Pensando...")  # Mostrar que está pensando
    response = agent.run(user_input_text)
    response = GoogleTranslator(source='english', target='spanish').translate(response)
    st.write(f"**REP.AI:** {response}")  # Mostrar la respuesta
    play_audio(response)  # Reproducir la respuesta en audio

def main():
    st.title("REP.AI Asistente de citas visitadores médicos Abbott")
    st.sidebar.title("Como quieres comunicarte con REP.AI")

    # Opciones para enviar mensaje de texto
    st.sidebar.subheader("Mensaje de texto")
    user_input_text = st.sidebar.text_input("Escribe tu mensaje:")
    if st.sidebar.button("Enviar"):
        send_message(user_input_text)

    # Opciones para enviar mensaje de voz
    st.sidebar.subheader("Mensaje de voz")
    if st.sidebar.button("Hablar"):
        start_voice_recording()

if __name__ == "__main__":
    main()
