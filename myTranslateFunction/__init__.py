import logging
import azure.functions as func
import requests, uuid

# Azure Translator 金鑰、端點、區域
key = "6aad8d69b17f41bb8b59af496716426f"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "eastus"

# Azure Translator API
path = '/translate'
constructed_url = endpoint + path


def main(req: func.HttpRequest) -> func.HttpResponse:
    src = req.params.get('src')
    text = req.params.get('text')
    dst = req.params.get('dst')

    if not src or not text or not dst:
        return "參數, 來源: 來源語言, 文字: 要翻譯的文字, 目標: 要轉換的語言."
    
    params = {
        'api-version': '3.0',
        'from': f'{src}',
        'to': f'{dst}'
    }
        
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
        
    # You can pass more than one object in body.
    body = [{
        'text': f'{text}'
    }]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    result = response.json()
    return func.HttpResponse(f"{result}",status_code=200)