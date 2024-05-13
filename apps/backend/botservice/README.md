<h1 align="center">
Backend Web Application - Bot API + Bot Service
</h1>

This bot has been created using [Bot Framework](https://dev.botframework.com).

Services and tools used:

- Azure App Service (Web App) - Chatbot API 호스팅
- Azure Bot Service - 다양한 채널을 통한 커뮤니케이션 관리 서비스

## Deploy Bot To Azure Web App

다음은 봇을 다음과 같은 여러 채널에 노출할 수 있는 Azure 봇 서비스와 연결된 Azure Wep 앱으로 봇 API를 실행하는 단계입니다: 웹 채팅, MS Teams, Twilio, SMS, 이메일, Slack 등을 포함한 여러 채널에 봇을 노출합니다.

1. Azure Portal에서: Azure Active Directory-> 앱 등록에서 멀티테넌트 앱 등록(서비스 주체)을 만들고, 시크릿을 생성하고 값을 기록합니다.

2. 아래 버튼을 클릭하여 봇 웹 앱과 봇 서비스를 배포하고 1단계에서 얻은 앱 등록 ID와 시크릿 값을 노트북에서 사용한 다른 모든 환경 변수와 함께 입력합니다.

[![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fendingone%2FAzure-AI-Search-Azure-OpenAI-Workbench%2Fmain%2Fapps%2Fbackend%2Fazuredeploy-backend.json)

3. 터미널에서 다음 명령을 실행하여 봇의 코드를 압축합니다. (** app/backend/ 폴더 경로 안에 위치해 있어야 합니다.**):
```bash
zip -j backend.zip ../../common/* ./*
```
4. Azure CLI를 사용하여 2단계에서 만든 Azure 앱 서비스에 봇 코드를 배포합니다.
```bash
az login -i
az webapp deployment source config-zip --resource-group "<resource-group-name>" --name "<name-of-backend-app-service>" --src "backend.zip"
```
**Note**:  `An error occured during deployment. Status Code: 401` 에러가 발생했을 때 ?! **Solution**:  위의 `az webapp deploy` 명령을 실행하기 전에 백엔드 Azure 웹 앱의 기본 인증이 `기본 인증 켜짐`으로 설정되어 있는지 확인합니다. Azure 포털에서 이 설정을 찾을 수 있습니다: '구성->일반 설정'에서 찾을 수 있습니다.
명령을 실행한 후 여러 번 재시도한다는 메시지가 표시되더라도 이미 zip 파일이 업로드되어 빌드 중이므로 걱정하지 마세요.

5. Azure 포털에서: **5분 정도 기다린 후** 2단계에서 만든 Azure Bot Service로 이동하여 봇을 테스트합니다: **웹 채팅에서 테스트**를 클릭합니다. 

6. Azure 포털에서: 봇 서비스에서 **Channels**을 클릭하여 여러 채널(팀 포함)을 추가합니다. 

7. apps/frontend 폴더로 이동하여 README.md의 단계에 따라 봇을 사용하는 프런트엔드 애플리케이션을 배포합니다.

## Reference documentation

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Samples code](https://github.com/microsoft/BotBuilder-Samples)
- [Bot Framework Python SDK](https://github.com/microsoft/botbuilder-python/tree/main)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Channels and Bot Connector Service](https://docs.microsoft.com/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)
