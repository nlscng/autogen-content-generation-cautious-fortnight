from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.base import TerminationCondition, TerminatedException
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, StopMessage, ToolCallExecutionEvent
from autogen_core import Component

import asyncio
import os
import pydantic
from pydantic import BaseModel

class ContentFeedback(BaseModel):
    grammar: int
    clarity: int
    style: int
    todo: str

class SEOFeedback(BaseModel):
    seo_score: int
    todo: str


async def main():
    model = OpenAIChatCompletionClient(
        model="gpt-4.1",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    writer_agent = AssistantAgent(
        name="writer_agent",
        description="""A writer agent that writes content and improve the written content based on 
        the given topic and feedback from the critic agents.""",
        system_message=
        """You are a writer agent. You will be given a topic, and you need to write
        some content based on the topic. You will be collaborating with a content
        critic agent, and an SEO critic agent. These agents will provide feedback
        and score your content. You should address their feedback and improve your 
        content based on their suggestions. Your goal is to produce high-quality
        content that meets the criteria set by the critic agent and SEO critic agent.
        If both of the critic agents give you a minimum score of 9 in all the scores,
        you should regenerate the content, and then you should exactly say 'TERMINATE'.""",
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
        write the text yourself. Your goal is to help the writer agent improve the quality of the text.
        If the minimum score of all the scores is 9 or above, leave the to-do list empty.""",
        model_client = model,
        output_content_type=ContentFeedback
    )

    seo_critic_agent = AssistantAgent(
        name="seo_critic_agent",
        description="""An SEO-critic agent that provides feedback on the SEO aspects of the content written
        by the writer agent.""", 
        system_message="""You are an SEO critic agent. You will be given a piece of text and you need to
        provide scores from 0 to 10 on the SEO of the text. You should also provide a to-do list of improvements
        for the writer agent to improve the SEO of the text. You should never write the text yourself. 
        If the minimum score of all the scores is 9 or above, leave the to-do list empty.""",
        model_client = model,
        output_content_type=SEOFeedback
    )

    selector_prompt = """You are in a team of content generation agents. The following roles are
    available: {roles}. 
    
    Read the following conversation. Then select the next role from {participants}
    to speak. Only return the role.
    
    {history}
    
    If a critic agent has some to-do list for the writer agent, the writer agent should address it in
    the next message and that same critic agent should review the writer agent's message afterwards.

    Read the above conversation. Then select the next role from {participants} to speak. Only return the 
    role."""

    termination = TextMentionTermination(text="TERMINATE") | MaxMessageTermination(max_messages=15)

    team = SelectorGroupChat(
        participants=[writer_agent, content_critic_agent, seo_critic_agent],
        model_client=model,
        selector_prompt=selector_prompt,
        termination_condition=termination,
        custom_message_types=[StructuredMessage[ContentFeedback], StructuredMessage[SEOFeedback]]
    )

    task = "Write a short paragraph about the importance of AI in modern technology."
    await Console(team.run_stream(task=task))

if __name__ == "__main__":
    asyncio.run(main())