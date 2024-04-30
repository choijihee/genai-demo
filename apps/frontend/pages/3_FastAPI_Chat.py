import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langserve import RemoteRunnable
import uuid
import requests
import json
import sys
import time
import random
from common.prompts import WELCOME_MESSAGE
# Env variables needed by langchain
os.environ["OPENAI_API_VERSION"] = os.environ.get("AZURE_OPENAI_API_VERSION")

# app config
st.set_page_config(page_title="FastAPI Backend Bot", page_icon="🤖", layout="wide")

with st.sidebar:
    st.markdown("""# Instructions""")
    st.markdown("""

이 Chatbot은 독립적인 Backend Azure Web App에서 호스팅되며 LangServe를 사용하여 만들어졌습니다.

다음의 도구/플러그인을 이용할 수 있습니다.

- 일반적인 지식을 위한 ChatGPT (***질문에 @chatgpt 를 사용하세요***)
- Azure 특정 서비스 문서의 지식 검색 - Azure OpenAI, AI Studio (***질문에 @docsearch 를 사용하세요***)

참고: @로 시작하는 도구 이름을 사용하지 않으면 봇이 자체 지식이나 사용 가능한 도구를 사용하여 질문에 답변하려고 시도합니다.
    """)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)


# ENTER HERE YOUR LANGSERVE FASTAPI ENDPOINT
# for example: "https://webapp-backend-botid-zf4fwhz3gdn64-staging.azurewebsites.net"

url = "https://<name-of-backend-app-service>-staging.azurewebsites.net" + "/agent/stream_events"


def get_or_create_ids():
    """Generate or retrieve session and user IDs."""
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = str(uuid.uuid4())
    return st.session_state['session_id'], st.session_state['user_id']

    
def consume_api(url, user_query, session_id, user_id):
    """Uses requests POST to talk to the FastAPI backend, supports streaming."""
    headers = {'Content-Type': 'application/json'}
    config = {"configurable": {"session_id": session_id, "user_id": user_id}}
    payload = {'input': {"question": user_query}, 'config': config}
    
    with requests.post(url, json=payload, headers=headers, stream=True) as response:
        try:
            response.raise_for_status()  # Raises an HTTPError if the response is not 200.
            for line in response.iter_lines():
                if line:  # Check if the line is not empty.
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        # Extract JSON data following 'data: '.
                        json_data = decoded_line[len('data: '):]
                        try:
                            data = json.loads(json_data)
                            if "event" in data:
                                kind = data["event"]
                                if kind == "on_chat_model_stream":
                                    content = data["data"]["chunk"]["content"]
                                    if content:  # Ensure content is not None or empty.
                                        yield content  # Two newlines for a paragraph break in Markdown.
                                elif kind == "on_tool_start":
                                        tool_inputs = data['data'].get('input')
                                        if isinstance(tool_inputs, dict):
                                            # Joining the dictionary into a string format key: 'value'
                                            inputs_str = ", ".join(f"'{v}'" for k, v in tool_inputs.items())
                                        else:
                                            # Fallback if it's not a dictionary or in an unexpected format
                                            inputs_str = str(tool_inputs)
                                        yield f"Searching Tool: {data['name']} with input: {inputs_str} ⏳\n\n"
                                elif kind == "on_tool_end":
                                        yield "Search completed.\n\n"
                            elif "content" in data:
                                # If there is immediate content to print, with added Markdown for line breaks.
                                yield f"{data['content']}\n\n"
                            elif "steps" in data:
                                yield f"{data['steps']}\n\n"
                            elif "output" in data:
                                yield f"{data['output']}\n\n"
                        except json.JSONDecodeError as e:
                            yield f"JSON decoding error: {e}\n\n"
                    elif decoded_line.startswith('event: '):
                        pass
                    elif ": ping" in decoded_line:
                        pass
                    else:
                        yield f"{decoded_line}\n\n"  # Adding line breaks for plain text lines.
        except requests.exceptions.HTTPError as err:
            yield f"HTTP Error: {err}\n\n"
        except Exception as e:
            yield f"An error occurred: {e}\n\n"


# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content=WELCOME_MESSAGE)]

    
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI", avatar='https://blobstorage3h6aqgwxxzpak.blob.core.windows.net/icon/sk_logo.png'):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input

session_id, user_id = get_or_create_ids()

user_query = st.chat_input("메세지를 여기에 입력하세요...")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI", avatar='https://blobstorage3h6aqgwxxzpak.blob.core.windows.net/icon/sk_logo.png'):
        response = st.write_stream(consume_api(url, user_query, session_id, user_id))

    st.session_state.chat_history.append(AIMessage(content=response))