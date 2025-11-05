from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import os


async def main():
    model = OpenAIChatCompletionClient(
        model="gpt-4.1",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    writer_agent = AssistantAgent(
        name="writer_agent",
        system_message=
        """You are a writer agent. You will be given a topic, and you need to write
        some content based on the topic. You will be collaborating with a content
        critic agent, and an SEO critic agent. These agents will provide feedback
        and score your content. You should address their feedback and improve your 
        content based on their suggestions. Your goal is to produce high-quality
        content that meets the criteria set by the critic agent and SEO critic agent.""",
        model_client = model
    )
    ## We will try the Selector group chat pattern from autogen_agentchat, instead of
    ## previously used round robin group chat pattern.
    ## https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/selector-group-chat.html

    content_critic_agent = AssistantAgent(
        name="content_critic_agent",
        description="""A content-critic agent that provides feedback on the content written 
        by the writer agent.""",
        system_message="""You are a content critic agent. You will be given a piece of text and you need to
        provide scores from 0 to 10 on the grammar, clarity, style of the text. You should also provide a
        to-do list of improvements for the writer agent to improve the text. You should never
        write the text yourself. Your goal is to help the writer agent improve the quality of the text.""",
        model_client = model
    )

    seo_critic_agent = AssistantAgent(
        name="seo_critic_agent",
        description="""An SEO-critic agent that provides feedback on the SEO aspects of the content written
        by the writer agent.""", 
        system_message="""You are an SEO critic agent. You will be given a piece of text and you need to
        provide scores from 0 to 10 on the SEO of the text. You should also provide a to-do list of improvements
        for the writer agent to improve the SEO of the text. You should never write the text yourself. Be """
        model_client = model
    )