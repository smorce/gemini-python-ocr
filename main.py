# my_project/utils/extract.py：マークダウンからJSONを抽出する関数を含みます。
# my_project/utils/image_processing.py：画像とテキストに基づいてAPIリクエストを行い、レスポンスを処理する関数を含みます。
# my_project/main.py：上記の関数を使用する例を示しています。

from utils.extract import extract_json_from_markdown
from utils.image_processing import predict_image
from utils.bounding_box_overlay import BoundingBoxOverlay

import argparse
import base64
from io import BytesIO
from PIL import Image, ImageDraw


def main(mime_type, prompt, active_model, image_path):

    image = Image.open(image_path)
    # RGBAモードの場合、RGBに変換
    if image.mode == 'RGBA':
      image = image.convert('RGB')
    # キャンバスの作成（ここでは既存の画像を使用）
    draw = ImageDraw.Draw(image)
    # キャンバスの内容をJPEG形式のバイトデータとして取得
    buffered = BytesIO()
    # 画像を保存する
    image.save(buffered, format="JPEG", quality=50)
    image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    result = predict_image(mime_type, image_data, prompt, active_model)
    print("result:")
    print(result)
    print()
    print()

    # レスポンスの内容を表示（"text"キーを含む部分のみ）
    # "text"キーを含む部分をフィルタリングして表示
    all_texts = []
    for candidate in result.get('candidates', []):
        for part in candidate.get('content', {}).get('parts', []):
            if 'text' in part:
                all_texts.append(part['text'])
    
    # すべてのテキストを結合して表示
    full_text = ''.join(all_texts)
    # print(full_text)
    BoundingBoxOverlay(image_path, full_text)



# 使用例
if __name__ == "__main__":

    # mime_type で指定できるタイプ
    # application/pdf
    # audio/mpeg
    # audio/mp3
    # audio/wav
    # image/png
    # image/jpeg
    # text/plain
    # video/mov
    # video/mpeg
    # video/mp4
    # video/mpg
    # video/avi
    # video/wmv
    # video/mpegps
    # video/flv


    # 引数
    parser = argparse.ArgumentParser(description="Process an image with specified prompt and active model.")
    parser.add_argument("--prompt", type=str, default="画像に存在するオブジェクトについてのストーリーを日本語で教えて下さい。画像に「さらに表示」と「Tweetリンクの共有ボタン」のオブジェクトがある場合、オブジェクトを参照するときは、その名前とバウンディングボックスを以下の書式で入力してください: [object name](y_min x_min y_max x_max).", help="The prompt for the image.")
    parser.add_argument("--active_model", type=str, default="flash", help="The active model name.")    # "pro"
    parser.add_argument("--image_path", type=str, default="スクリーンショット.png", help="The path to the image file.")

    args = parser.parse_args()


    # デフォルト
    mime_type = "image/jpeg"           # [image/png, image/jpeg]  元のコードは image/png だった。PNGファイルを解析する場合でも image/jpeg で OK なのでこれはいじらない
    # prompt  = "What is the position of the objects present in the image? Output objects in JSON format with both object names and positions as a JSON object: { name: [y_min, x_min, y_max, x_max] }. Put the annswer in a JSON code block."
    
    
    main(mime_type, args.prompt, args.active_model, args.image_path)