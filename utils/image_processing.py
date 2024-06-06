import requests
import json

def predict_image(mime_type: str, image_data: str, prompt: str, active_model: str) -> dict:
    Gemini_API_KEY = "自分のやつ。GitHubにはあげない"

    url = (
        "/api/flashGenerateResponseToTextAndImage"
        if active_model == "flash"
        else "/api/proGenerateResponseToTextAndImage"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Gemini_API_KEY}"
    }

    body = {
        "prompt": prompt,
        "imageData": image_data,
        "mimeType": mime_type
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
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
