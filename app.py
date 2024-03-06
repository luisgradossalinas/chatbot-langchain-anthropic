import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image

st.set_page_config(
    page_title = "Chatbot usando Anthropic Claude 3",
    page_icon = "🖥"
)

with st.sidebar:
    
    st.title("Chatbot usando Anthropic - Claude 3")

    image = Image.open('logo-arc.png')
    st.image(image, caption = 'LangChain, Streamlit y Anthropic')

    anthropic_api_key = st.sidebar.text_input("Ingrese tu API Key de Anthropic y Enter para habilitar el chatbot", key = "chatbot_api_key", type = "password")
    "[Genera tu  API Key en Anthropic - $5 de regalo nos dan para usar su API](https://console.anthropic.com/login)"
    "[Ver el código](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

msg_chatbot = """
        Soy un chatbot que está integrado con Claude 3.

        ### Preguntas frecuentes
        
        - ¿Quién eres?
        - ¿Cómo funcionas?
        - ¿Cuál es tu capacidad o límite de conocimientos?
        - ¿Puedes ayudarme con mi tarea/trabajo/estudio?
        - ¿Tienes emociones o conciencia?
        - Lo que desees
"""

#Store the LLM Generated Reponese
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content" : msg_chatbot}]
    
# Diplay the chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear the Chat Messages
def clear_chat_history():
    st.session_state.messages = [{"role" : "assistant", "content": msg_chatbot}]

# Create a Function to generate
def generate_response(input):
    
    llm = ChatAnthropic(
        model_name = "claude-3-opus-20240229",
        anthropic_api_key = anthropic_api_key, 
        temperature = 0
    )

    prompt = ChatPromptTemplate.from_template("Responde la siguiente pregunta : {question}")
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    return chain.invoke({"question" : input})

st.sidebar.button('Limpiar historial de chat', on_click = clear_chat_history)

if anthropic_api_key:

    prompt = st.chat_input("Ingresa tu pregunta")
    if prompt:
        st.session_state.messages.append({"role": "user", "content":prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generar una nueva respuesta si el último mensaje no es de un assistant, sino un user
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Esperando respuesta, dame unos segundos."):
                
                response = generate_response(prompt)
                placeholder = st.empty()
                full_response = ''
                
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)

        message = {"role" : "assistant", "content" : full_response}
        st.session_state.messages.append(message) #Agrega elemento a la caché de mensajes de chat.
