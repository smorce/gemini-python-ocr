# my_project/utils/extract.py：マークダウンからJSONを抽出する関数を含みます。
# my_project/utils/image_processing.py：画像とテキストに基づいてAPIリクエストを行い、レスポンスを処理する関数を含みます。
# my_project/utils/svg.py：ポイントリストからSVGパスを生成する関数を含みます。
# my_project/main.py：上記の関数を使用する例を示しています。

from utils.extract import extract_json_from_markdown
from utils.image_processing import predict_image
from bounding_box_overlay import BoundingBoxOverlay
# from utils.svg import get_svg_path_from_stroke

import base64
from io import BytesIO
from PIL import Image, ImageDraw

# 使用例
if __name__ == "__main__":

    mime_type = "image/jpeg"           # 元のコードは "image/png"
    prompt = "画像に存在するオブジェクトについてのストーリーを日本語で教えて下さい。画像に「さらに表示」と「Tweetリンクの共有ボタン」のオブジェクトがある場合、オブジェクトを参照するときは、その名前とバウンディングボックスを以下の書式で入力してください: [object name](y_min x_min y_max x_max)."
    active_model = "flash"     # "pro"
    image_path = "path_to_your_image.jpg"  # ここに画像のパスを指定


    image = Image.open(image_path)
    # キャンバスの作成（ここでは既存の画像を使用）
    draw = ImageDraw.Draw(image)
    # キャンバスの内容をJPEG形式のバイトデータとして取得
    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=50)
    image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    result = predict_image(mime_type, image_data, prompt, active_model)
    print(result)
    BoundingBoxOverlay(image_path, result)
