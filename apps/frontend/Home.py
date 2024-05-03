import streamlit as st

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

st.image("https://blobstorage3h6aqgwxxzpak.blob.core.windows.net/icon/sk_logo.png", width=70)
st.header("Generative AI Chatbot (SK C&C)")

st.markdown("---")
st.markdown("""
    
    안녕하세요! 검색 서비스와 챗 서비스를 제공하는 AI Chatgot 입니다. 

    이 엔진은 미리 업로드한 PDF 파일에서 정보를 찾아냅니다.

    소스의 위치는 [Github Repo](https://github.com/endingone/Azure-AI-Search-Azure-OpenAI-Workbench) 입니다. 
    
    **👈
    문서 검색을 이용하려면 'Search'를, 대화형 기반의 챗 서비스를 이용하려면 'WebChat'을 선택하세요! 


"""
)
st.markdown("---")
