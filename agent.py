import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
        if not api_key:
            st.error("Groq API key not set.")
            st.stop()
        _client = Groq(api_key=api_key)
    return _client

# Centralized model configuration
MODEL = "llama-3.3-70b-versatile"


def _create_chat_completion(messages):
    """Helper function to create chat completion with error handling."""
    try:
        client = get_client()
        # Use stream=True to get a generator of response chunks
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            temperature=0.2,
            max_tokens=2048,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        # Catch all exceptions including API errors
        st.error(f"An error occurred: {e}")

def clarification_agent(question):
    """
    Agent that checks if the question is clear enough to answer.
    Only asks for clarification when absolutely necessary.
    """
    messages = [
        {"role": "system", "content": "You are a helpful teaching assistant. Your role is to analyze a student's question for clarity. Only ask for clarification if the question is truly impossible to answer or critically ambiguous. For questions that can be reasonably interpreted (even if slightly vague), respond with 'The question is clear.' Be generous in your interpretation and assume the most common or obvious meaning. Only ask clarifying questions when absolutely necessary."},
        {"role": "user", "content": f"Student's question: '{question}'"}
    ]
    return _create_chat_completion(messages)

def solution_agent(question):
    """
    Agent that provides a comprehensive, step-by-step solution.
    Makes reasonable assumptions if the question is slightly vague.
    """
    messages = [
        {"role": "system", "content": "You are an expert tutor. Your goal is to provide a comprehensive, step-by-step solution to the student's homework question. If the question is slightly vague, make reasonable assumptions about what the student is asking (and mention those assumptions). Start by explaining the core concepts, then walk through the solution process. Be clear, thorough, and encouraging."},
        {"role": "user", "content": f"Provide a detailed solution for this question: {question}"}
    ]
    return _create_chat_completion(messages)

def quality_assurance_agent(solution):
    """
    Agent that reviews the solution for accuracy and clarity.
    Provides constructive feedback.
    """
    messages = [
        {"role": "system", "content": "You are a meticulous quality assurance assistant. Your task is to review a provided solution for accuracy, clarity, and completeness. Identify any errors, logical fallacies, or areas that could be explained better. Provide constructive feedback. If the solution is perfect, state that it is accurate and well-explained."},
        {"role": "user", "content": f"Please review the following solution:\n\n---\n{solution}\n---"}
    ]
    return _create_chat_completion(messages)

def concise_answer_agent(solution):
    """
    Agent that summarizes the detailed solution into a concise answer.
    Extracts the key result or main point.
    """
    messages = [
        {"role": "system", "content": "You are an expert summarizer. Your job is to distill a detailed solution into a concise, easy-to-understand final answer. Extract the key result or main point and present it clearly. Keep it brief but informative."},
        {"role": "user", "content": f"Summarize the final answer from this detailed solution:\n\n---\n{solution}\n---"}
    ]
    return _create_chat_completion(messages)