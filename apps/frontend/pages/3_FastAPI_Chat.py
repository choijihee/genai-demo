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

####### Welcome Message for the Bot Service #################
WELCOME_MESSAGE = """
안녕하세요! \U0001F44B

저는 여러분을 돕기 위해 설계된 스마트 가상 비서인 Jarvis입니다.
저와 소통하는 방법은 아래와 같습니다.

질문에 효과적으로 답변할 수 있는 다양한 플러그인과 도구가 준비되어 있습니다. 사용 가능한 옵션은 다음과 같습니다.

1. \U0001F4A1 **chatgpt**: 이 도구를 사용하면 제가 학습한 데이터를 기반으로 저만의 지식을 활용할 수 있습니다. (제 훈련 데이터는 2021년까지만 제공된다는 점에 유의하세요.)

2. \U0001F50D **docsearch**: 이 도구를 사용하면 전문 검색 엔진 색인을 검색할 수 있습니다. 여기에는 Azure 서비스 소개 Docs 자료가 포함되어 있습니다. (Azure AI Service)

모든 출처에서 필요한 정보를 제공하고 답변을 도출하는 데 사용한 출처도 언급합니다. 이렇게 하면 정보의 출처를 투명하게 파악하고 제가 어떻게 답변에 도달했는지 이해할 수 있습니다.

제 기능을 최대한 활용하려면 질문할 때 제가 어떤 도구를 사용했으면 좋겠는지 구체적으로 언급해 주세요. 예를 들면..

```
chatgpt, pandas를 사용하여 URL에서 원격 파일을 읽으려면 어떻게 해야 하나요?
docsearch, chloroquine이 정말 코로나 바이러스에 효과가 있나요?
```

궁금한 점이 있으면 언제든지 질문하고 활용하고 싶은 도구를 지정해 주세요. 제가 도와드리겠습니다!

---
"""
###########################################################
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

url = "https://webapp-backend-botid-3h6aqgwxxzpak-staging.azurewebsites.net" + "/agent/stream_events"


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

    st.markdown(
    """
    <style>
        .stChatMessage {
            text-align: right;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI", avatar='https://blobstorage3h6aqgwxxzpak.blob.core.windows.net/icon/sk_logo.png'):
        response = st.write_stream(consume_api(url, user_query, session_id, user_id))

    st.session_state.chat_history.append(AIMessage(content=response))