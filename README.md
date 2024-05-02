# Generative AI Chatbot Demo 

by: Azure AI Search + Azure OpenAI + Bot Framework + Langchain + CosmosDB + Document Intelligence SDK

조직에는 여러 위치에 흩어져 있는 다양한 유형의 데이터를 이해할 수 있는 "Multi-Channel Smart Chatbot"과 "Search Engine"이 필요합니다.
또한, 대화형 챗봇은 문의에 대한 답변과 함께 출처 및 답변을 얻은 방법과 출처에 대한 설명도 제공할 수 있어야 합니다. 즉, 비즈니스 데이터에 대한 질문을 해석하고, 이해하고, 답변할 수 있는 **Private하고 안전한 ChatGPT**를 조직에 제공하고자 하는 것입니다. 

Workbench의 목표는 RAG 패턴 기반의 GPT 사용 사례를 신속하게 빌드하기 위한 지침을 제공하고 자체 환경에서 자체 데이터를 사용하여 Azure 서비스로 빌드한 구성을 기반으로 증명하는 것입니다.
결과물은 다음과 같습니다.

1. Bot Framework로 구성된 여러 채널에 노출되는 Backend Bot API (Web Chat, MS Teams, SMS, Email, Slack, etc)
2. Frontend 웹 애플리케이션 (with, Search & Bot UI)

이 리포지토리는 <span style="color:red">OpenAI 기반 스마트 검색 엔진</span>을 구축하는 방법을 단계별로 알려드리기 위해 만들어졌습니다.
각 노트북은 RAG 패턴을 구현하기 위한 Step-by-Step으로 구성되어 있으며, 마지막에는 애플리케이션을 구축하는 것으로 끝납니다.

---
**2주간 POC 진행 시 고객 사전 준비 사항**
* Azure 구독(Subscription)
* GPT-4를 포함한 Azure Open AI 사용을 위한 액세스 요청 및 승인이 완료되어 있어야 합니다. <span style="color:red">만일 고객이 GPT-4에 대한 액세스 허용이 불가능한 경우, Workshop POC 기간 동안 SK C&C에서 OpenAI 리소스를 대여할 수 있습니다.</span>
* SK C&C 담당자는 고객의 Azure AD에 Geust로 추가되는 것이 권고 사항이지만, 불가능한 경우 고객이 SK C&C 담당자에게 corporate ID를 발급해야 합니다.
* 고객의 Azure 테넌트(Tenent)에 <span style="color:red">Workshop POC</span>을 위한 리소스 그룹(Resource Group)을 설정해야 합니다.
* 고객 담당자와 SK C&C 담당자는 <span style="color:red">Workshop PoC</span> 5주 전에 모든 것을 설정할 수 있도록 리소스 그룹(Resource Group)에 대한 기여자(Contributor) 권한이 있어야 합니다.
* Storage Account 리소스는 리소스 그룹(Resource Group)에 생성되어야 합니다.
* 고객의 데이터/문서는 <span style="color:red">Workshop PoC 기간</span> 2주 전에 Storage Account의 Blob Storage에 업로드 되어야 합니다.at least two weeks prior to 
* 멀티 테넌트 앱 등록(Service Principal)은 고객이 생성해야 합니다. (생성 시 Client ID와 Secret Value는 저장해두어야 합니다.)
* 고객은 Bot이 올바르게 응답하기를 원하는 10~20개의 질문(쉬움 ~ 어려움)을 SK C&C에 제공해야 합니다.
* <span style="color:red">Workshop PoC</span> 진행 시 IDE 협업 및 표준화를 위해 Jupyter Lab을 갖춘 Azure Machine Learning 컴퓨팅 인스턴스가 사용됩니다.
   * 참고: Azure Machine Learning 작업 영역에 Core 컴퓨팅 할당량이 충분한지 확인해야 합니다. 

---
# 아키텍처
<span style="color:red">*※ The below need to be udated.*</span><br>
![Architecture](./images/GPT-Smart-Search-Architecture2.jpg "Architecture")

## User Flow
1. 사용자가 질의를 합니다.
2. App에서 OpenAI GPT-4 LLM은 사용자 입력에 따라 사용할 소스를 결정하기 위해 Smart Prompt를 사용합니다.
3. 현재 아래와 같은 PDF 소스가 이용 가능합니다.:
   * 3a. Azure AI Search은 Blob Storage에서 가져온 AI로 풍부하게 가공된 문서를 포함하고 있습니다.:
       - Azure AI Studio 기술 문서 PDF
4. App은 소스로부터 결과를 검색하여 답을 작성합니다.
5. 질문과 답변은 추가 분석을 위해 Cosmos DB에 영구 메모리로 저장됩니다.
6. 답변이 사용자에게 전달됩니다. 

---
## 데모 링크
<span style="color:red">*※ The below need to be udated.*</span><br>
https://webapp-frontend-3h6aqgwxxzpak.azurewebsites.net/


---

## 🔧**기능**

   - [Bot Framework](https://dev.botframework.com/) 및 [Bot Service](https://azure.microsoft.com/en-us/products/bot-services/) 를 사용하여 Bot API 백엔드를 호스팅하고 이를 MS Teams를 포함한 여러 채널에 노출할 수 있습니다.
   - 100% Python 코드로 구성되어 있습니다.
   - [Azure AI Services](https://azure.microsoft.com/en-us/products/cognitive-services/)를 사용하여 구조화되지 않은 문서(이미지에 대한 OCR, 청킹 및 자동화된 벡터화)를 인덱싱하고 강화합니다.
   - Azure AI Search의 하이브리드 검색 기능을 사용하여 최상의 의미론적 답변을 제공합니다(텍스트 및 벡터 검색 결합).
   - Azure OpenAI, 벡터 저장소와 상호 작용하고 프롬프트 구성 및 에이전트 생성을 위한 wrapper로 [LangChain](https://langchain.readthedocs.io/en/latest/)을 사용합니다.
   - 다국어에 대한 수집, Index 및 이해
   - 멀티 Index -> 다중 검색 Index
   - [Azure AI Document Intelligence SDK (former Form Recognizer)](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview?view=doc-intel-3.0.0)를 사용하여 복잡하고 큰 PDF 문서를 구문 분석합니다.
   - CosmosDB를 영구 메모리로 사용하여 사용자 대화를 저장합니다.
   - [Streamlit](https://streamlit.io/)Streamlit을 사용하여 Python으로 Frontend 웹 애플리케이션을 구축합니다.
   

---

## **POC 실행 단계**

참고: (사전 준비 사항) Azure OpenAI 리소스가 생성되어 있어야 합니다.

1. 이 레포지토리를 Fork 합니다.
2. Azure OpenAI Studio에서 아래의 모델들을 배포합니다. (이전 모델들은 이 PoC에서 동작하지 않을 수 있습니다.):
   - "gpt-35-turbo-1106 (or newer)" 
   - "gpt-4-turbo-1106  (or newer)"
   - "text-embedding-ada-002 (or newer)"
3. 이 PoC의 모든 리소스가 포함될 리소스 그룹을 생성합니다. Azure OpenAI 는 다른 리소스 그룹 또는 다른 구독에 있을 수 있습니다.
4. Notebook(Azure AI Search, Azure AI Services, etc)을 실행하는데 필요한 모든 Azure 인프라를 실행하려면 아래의 링크를 클릭하세요.:

<span style="color:red">*※ The below need to be udated.*</span><br>
[![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fendingone%2FAzure-AI-Search-Azure-OpenAI-Workbench%2Fmain%2Fazuredeploy.json) 

**참고**: 만일 이전에 `Azure AI Services Multi-Service account` 리소스를 생성한 적이 없다면 Azure Portal에서 수동으로 계정을 만들어 Responsible AI 약관을 읽고 동의하세요. 배포가 완료되면 삭제한 후 위의 배포 버튼을 사용하세요.

5. Fork된 레포지토리를 AML 컴퓨팅 인스턴스에 복제합니다. 저장소가 비공개인 경우 아래의 문제 해결 섹션에서 비공개 저장소를 복제하는 방법을 참조하세요.

6. **Python 3.10 conda 환경** 이상에서 노트북을 실행해야 합니다.
7. 컴퓨터에 종속성을 설치합니다(노트북을 실행할 동일한 conda 환경에서 아래 pip 명령을 수행해야 합니다. 예를 들어 AML 컴퓨팅 인스턴스에서 다음을 실행합니다.):
```
conda activate azureml_py310_sdkv2
pip install -r ./common/requirements.txt
```

일부 pip 종속성 오류가 발생할 수 있지만 괜찮습니다. 오류에 관계없이 라이브러리가 올바르게 설치되었습니다.

8. 4단계에서 생성된 서비스의 고유한 값으로 `credentials.env` 파일을 편집합니다.
9. **노트북을 순서대로 실행합니다.** 

