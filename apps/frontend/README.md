<h1 align="center">
Frontend Web Application - Search + Web Bot Channel
</h1>

스트림릿을 사용하여 봇 서비스 채널을 노출하는 간단한 UI.
검색 환경도 포함됩니다.
 
## Deploy in Azure Web App Service

1. 아래 버튼을 클릭하여 프런트엔드 Azure 웹 애플리케이션을 배포합니다.

[![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fendingone%2FAzure-AI-Search-Azure-OpenAI-Workbench%2Fmain%2Fapps%2Ffrontend%2Fazuredeploy-frontend.json)

2. 터미널에서 다음 명령을 실행하여 봇의 코드를 압축합니다. ( apps/frontend/ 폴더 경로 안에 위치해 있어야 합니다.):
```bash
zip frontend.zip ./*
zip frontend.zip ./pages/*
zip -j frontend.zip ../../common/*
```
3. Azure CLI를 사용하여 2단계에서 만든 Azure App Service에 프런트엔드 코드를 배포합니다.
```bash
az login -i
az webapp deployment source config-zip --resource-group "<resource-group-name>" --name "<name-of-frontend-app-service>" --src "frontend.zip"
```

**Note**: `An error occured during deployment. Status Code: 401`에러가 발생하는 경우.. **Solution**:  위의 `az webapp deploy` 명령을 실행하기 전에 백엔드 Azure 웹 앱의 기본 인증이 `기본 인증 켜짐`으로 설정되어 있는지 확인하세요. 이 설정은 Azure 포털에서 찾을 수 있습니다: '구성->일반 설정'에서 찾을 수 있습니다.
명령을 실행한 후 여러 번 재시도한다는 메시지가 표시되더라도 이미 zip 파일이 업로드되어 빌드 중이므로 걱정하지 마세요.

4.  몇 분(5~10분)이 지나면 앱이 작동합니다. Azure 포털로 이동하여 URL을 가져옵니다.

## Troubleshoot

1. 웹앱이 성공적으로 배포되었지만 애플리케이션이 시작되지 않은 경우
   1. Azure Portal로 이동합니다. Azure portal -> Your Webapp -> Settings -> Configuration -> General Settings
   2. 시작 명령에 다음이 있는지 확인합니다.  python -m streamlit run Home.py --server.port 8000 --server.address 0.0.0.0

2. If running locally fails with error "TypeError: unsupported operand type(s) for |: 'type' and '_GenericAlias'"
Check your list of conda environments and activate one with Python 3.10 or higher
For example, if you are running the app on an Azure ML compute instance:
    ```
    conda env list
    conda activate azureml_py310_sdkv2
    ```




