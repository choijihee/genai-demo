import streamlit as st
import urllib
import os
import re
import time
import random
from operator import itemgetter
from collections import OrderedDict
from langchain_core.documents import Document
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from utils import get_search_results
from prompts import DOCSEARCH_PROMPT

st.set_page_config(page_title="SK C&C Gen.AI Demo", page_icon='https://blobstorage3h6aqgwxxzpak.blob.core.windows.net/icon/sk_logo.png', layout="wide")
# Add custom CSS styles to adjust padding
st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://blobstorage3h6aqgwxxzpak.blob.core.windows.net/icon/gai_demo_logo_wh.png);
                background-repeat: no-repeat;
                background-size: contain;
                padding-top: 80px;
                background-position: 20px 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.header("GPT Smart Search Engine")


def clear_submit():
    st.session_state["submit"] = False


# with st.sidebar:
#     st.markdown("""# Instructions""")
#     st.markdown("""
# Azure AI Service(OpenAI, AI Studio)에 대해 궁금한 것을 검색하세요. 

# For example:
# - Azure OpenAI 의 최신 기능을 알려줘. 
    
#     \nData Source(Docs PDF)에서 찾은 검색 결과를 기반으로 답변하기 때문에 공개적인 ChatGPT와 다르다는 것을 알 수 있습니다. 
#     """)

coli1, coli2= st.columns([3,1])
with coli1:
    query = st.text_input("Ask a question to your enterprise data lake", value= "What is Contoso Electronics's mission?", on_change=clear_submit)

button = st.button('Search')



if (not os.environ.get("AZURE_SEARCH_ENDPOINT")) or (os.environ.get("AZURE_SEARCH_ENDPOINT") == ""):
    st.error("Please set your AZURE_SEARCH_ENDPOINT on your Web App Settings")
elif (not os.environ.get("AZURE_SEARCH_KEY")) or (os.environ.get("AZURE_SEARCH_KEY") == ""):
    st.error("Please set your AZURE_SEARCH_ENDPOINT on your Web App Settings")
elif (not os.environ.get("AZURE_OPENAI_ENDPOINT")) or (os.environ.get("AZURE_OPENAI_ENDPOINT") == ""):
    st.error("Please set your AZURE_OPENAI_ENDPOINT on your Web App Settings")
elif (not os.environ.get("AZURE_OPENAI_API_KEY")) or (os.environ.get("AZURE_OPENAI_API_KEY") == ""):
    st.error("Please set your AZURE_OPENAI_API_KEY on your Web App Settings")
elif (not os.environ.get("BLOB_SAS_TOKEN")) or (os.environ.get("BLOB_SAS_TOKEN") == ""):
    st.error("Please set your BLOB_SAS_TOKEN on your Web App Settings")

else: 
    os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"]
    
    MODEL = os.environ.get("AZURE_OPENAI_MODEL_NAME")
    llm = AzureChatOpenAI(deployment_name=MODEL, temperature=0.5, max_tokens=1500)
                           
    if button or st.session_state.get("submit"):
        if not query:
            st.error("Please enter a question!")
        else:
            # Azure Search

            try:
                # indexes = ["cogsrch-index-files", "cogsrch-index-csv"]
                indexes = ["cogsrch-index-files"]
                k = 6  
                ordered_results = get_search_results(query, indexes, k=k, reranker_threshold=1, sas_token=os.environ['BLOB_SAS_TOKEN'])            

                st.session_state["submit"] = True
                # Output Columns
                placeholder = st.empty()

            except Exception as e:
                st.markdown("Not data returned from Azure Search, check connection..")
                st.markdown(e)
            
            if "ordered_results" in locals():
                try:
                    top_docs = []
                    for key,value in ordered_results.items():
                        location = value["location"] if value["location"] is not None else ""
                        top_docs.append(Document(page_content=value["chunk"], metadata={"source": location, "score":value["score"]}))
                        add_text = "Reading the source documents to provide the best answer... ⏳"

                    # LLM Search Answer 로직 제거
                    # if "add_text" in locals():
                    #     with st.spinner(add_text):
                    #         if(len(top_docs)>0):
                    #             chain = (
                    #                 DOCSEARCH_PROMPT  # Passes the 4 variables above to the prompt template
                    #                 | llm   # Passes the finished prompt to the LLM
                    #                 | StrOutputParser()  # converts the output (Runnable object) to the desired output (string)
                    #             )
    
                    #             answer = chain.invoke({"question": query, "context":top_docs})
                                
                    #         else:
                    #             answer = {"output_text":"No results found" }
                    # else:
                    #     answer = {"output_text":"No results found" }


                    with placeholder.container():

                        # Search 의 Answer 결과 출력 제거

                        # st.markdown("#### Answer")
                        # st.markdown(answer, unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown("#### Search Results")

                        if(len(top_docs)>0):
                            for key, value in ordered_results.items():
                                location = value["location"] if value["location"] is not None else ""
                                title = str(value['title']) if (value['title']) else value['name']
                                score = str(round(value['score']*100/4,2))
                                st.markdown("[" + title +  "](" + location + ")" + "  (Score: " + score + "%)")
                                st.markdown(value["caption"])
                                st.markdown("---")

                except Exception as e:
                    st.error(e)
