import requests
import json

def predict_image(mime_type: str, image_data: str, prompt: str, active_model: str) -> dict:
    GOOGLE_API_KEY = ""

    # APIエンドポイントのURL
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}"
        if active_model == "flash"
        else
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GOOGLE_API_KEY}"
    )

    # ヘッダーとデータの設定
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "systemInstruction": {
          "parts": [
            {
              "text": "あなたはとても賢いAIアシスタントです"
            }
          ]
        },
        "contents": {
          "role": "user",
          "parts": [
            {
              "inlineData": {
                "mimeType": mime_type,
                "data": image_data
              }
            },
            {
              "text": prompt
            }
          ]
        },
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 2048,
            "topP": 1.0,
            "topK": 32
        }
    }

    # リクエストを送信
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if response.ok:
            return result
        else:
            fetch_error = Exception(result.get('error', {}).get('message', 'Unknown error'))
            fetch_error.fetch_result = result
            raise fetch_error
    except Exception as error:
        if hasattr(error, 'fetch_result'):
            print(f"HTTP request failed with status code {error.fetch_result.get('error', {}).get('code', 'Unknown')}", error.fetch_result)
            return error.fetch_result
        return {
            "error": {
                "message": str(error)
            }
        }