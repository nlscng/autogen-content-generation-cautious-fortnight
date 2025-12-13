import streamlit as st
import asyncio
from writer import teamConfig, orchetrate

st.title("Agent Content Generation!!!")

chat = st.container()

prompt = st.chat_input("Enter a description of the content you want the team of agents to create")

if prompt:
    async def main():
        team = teamConfig(min_score_threshold=8)
        with chat:
            async for message in orchetrate(team, prompt):
                if message.startswith("**Writer**"):
                    with st.chat_message("ai"):
                        st.markdown(message)
                elif message.startswith("**Content Critic**"):
                    with st.chat_message("human"):
                        st.markdown(message)
                elif message.startswith("**SEO Critic**"):
                    with st.chat_message("human"):
                        st.markdown(message)
                elif message.startswith("**User**"):
                    with st.chat_message("user"):
                        st.markdown(message)
                elif message.startswith('**Termination**'):
                    with st.chat_message("ai"):
                        st.markdown(message)
                    
    with st.spinner("Agents are working..."):
        asyncio.run(main())
        st.success("Content generation complete!")