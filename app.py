import streamlit as st
import asyncio
from writer import teamConfig, orchetrate

st.title("Agent Content Generation!!!")

chat = st.container()

prompt = st.chat_input("Enter a description of the content you want the team of agents to create")

if prompt:
    with chat:
        st.write("Hey! Generating content...")
        
