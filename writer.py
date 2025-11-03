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
        name="WriterAgent",
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