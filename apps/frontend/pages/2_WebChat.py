import os
import streamlit as st
import streamlit.components.v1 as components

# From here down is all the StreamLit UI.
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

# with st.sidebar:
#     st.markdown("""# Instructions""")
#     st.markdown("""

# 이 Chatbot은 독립적인 Backend Azure Web App에서 호스팅되며 봇 프레임워크 SDK를 사용하여 만들어졌습니다.
# (봇 인터페이스는 Azure에서 호스팅되는 Bot Service 앱의 창일 뿐입니다.)

# 다음의 도구/플러그인을 이용할 수 있습니다.

# - 일반적인 지식을 위한 ChatGPT (***질문에 @chatgpt 를 사용하세요***)
# - Azure 특정 서비스 문서의 지식 검색 - Azure OpenAI, AI Studio (***질문에 @docsearch 를 사용하세요***)

# 참고: @로 시작하는 도구 이름을 사용하지 않으면 봇이 자체 지식이나 사용 가능한 도구를 사용하여 질문에 답변하려고 시도합니다.
#     """)
    
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)


BOT_DIRECTLINE_SECRET_KEY = os.environ.get("BOT_DIRECTLINE_SECRET_KEY")

components.html(
f"""
<html>
  <head>
    <script
      crossorigin="anonymous"
      src="https://cdn.botframework.com/botframework-webchat/latest/webchat.js"
    ></script>
    <script crossorigin="anonymous" src="https://unpkg.com/markdown-it@10.0.0/dist/markdown-it.min.js"></script>
     <style>
      html,
      body {{
          height: 100%;
          background-image: linear-gradient( #FFFFFF,#FFFFFF);
          color: antiquewhite;
          font-family: 'Segoe UI', Calibri, sans-serif;
      }}

      body {{
        padding-left: 5px;
      }}

      #webchat {{
        height: 100%;
        width: 100%;
      }}
      .webchat__stacked-layout--from-user{{
        background-color: 'white';
      }}
      
    </style>
  </head>
  <body>
    <div id="webchat" role="main"></div>
    <script>
      // Set  the CSS rules.
      const styleSet = window.WebChat.createStyleSet({{
          bubbleBackground: 'transparent',
          bubbleBorderColor: 'antiquewhite',
          bubbleBorderRadius: 5,
          bubbleBorderStyle: 'solid',
          bubbleBorderWidth: 0,
          bubbleTextColor: 'black',

          userAvatarBackgroundColor: 'rgba(255, 140, 0)',
          bubbleFromUserBackground: 'transparent', 
          bubbleFromUserBorderColor: 'antiquewhite',
          bubbleFromUserBorderRadius: 5,
          bubbleFromUserBorderStyle: 'solid',
          bubbleFromUserBorderWidth: 0,
          bubbleFromUserTextColor: 'black',

          notificationText: 'black',

          bubbleMinWidth: 400,
          bubbleMaxWidth: 720,

          botAvatarBackgroundColor: 'antiquewhite',
          avatarBorderRadius: 2,
          avatarSize: 40,

          rootHeight: '100%',
          rootWidth: '100%',
          backgroundColor: 'rgba(255, 255, 255)',

          hideUploadButton: 'true'
      }});
      // After generated, you can modify the CSS rules.
      // Change font family and weight. 
      styleSet.textContent = {{
          ...styleSet.textContent,
          fontWeight: 'regular'
      }};

      // Set the avatar options. 
      const avatarOptions = {{
          botAvatarInitials: '.',
          userAvatarInitials: 'Me',
          botAvatarImage: 'https://blobstorage3h6aqgwxxzpak.blob.core.windows.net/icon/sk_logo.png',
          
          }};
      const markdownIt = window.markdownit({{html:true}});
      window.WebChat.renderWebChat(
        {{
          directLine: window.WebChat.createDirectLine({{
            token: '{BOT_DIRECTLINE_SECRET_KEY}'
          }}),
          renderMarkdown: markdownIt.render.bind(markdownIt),
          styleSet, styleOptions: avatarOptions,
          locale: 'en-US'
        }},
        document.getElementById('webchat')
      );
    </script>
  </body>
</html>
""", height=800)
