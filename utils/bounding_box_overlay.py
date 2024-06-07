from PIL import Image, ImageDraw, ImageFont
import re
import os
import glob

def BoundingBoxOverlay(image_path, response_text):
    """
    1. バウンディングボックスの処理:
      matchesリストからバウンディングボックスの情報を1つずつ取り出します。各バウンディングボックス情報は、ラベルと4つの座標値 (y_min, x_min, y_max, x_max) から成ります。
      取り出した座標値を整数に変換します。
    
    2. 座標の百分率変換:
      1000x1000の空間内の座標値を、それぞれ1000で割ることで百分率に変換します。これにより、x_min_pct, y_min_pct, x_max_pct, y_max_pctが得られます。
    
    3. 四角形の描画:
      百分率に変換した座標値を使って、実際の画像上でのピクセル単位の座標を計算します。
      具体的には、x_min_pct * image_widthやy_min_pct * image_heightなどの計算を行い、これを使用してdraw.rectangleメソッドで四角形を描画します。四角形の枠線の色は赤 (outline="red") に設定し、線の幅は2ピクセル (width=2) に設定します。
    
    4. ラベルの描画:
      百分率に変換した座標値を使って、ラベルのテキストの描画位置を計算します。ラベルは四角形の上部に描画されます。
      draw.textメソッドを使用して、計算された位置にラベルのテキストを描画します。テキストの色は赤 (fill="red") に設定します。
    """

    output_path = "output_image_with_bounding_boxes.png"

    # クリーンアップ
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
            print(f"Deleted: {output_path}")
            print()
            print()
        except Exception as e:
            print(f"Failed to delete {output_path}: {e}")
            print()
            print()
    else:
        print(f"File not found: {output_path}")
        print()
        print()

    # Load image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 画像の幅と高さを取得
    image_width, image_height = image.size
    
    # Specify a Japanese font (adjust the path to a valid Japanese font file on your system)
    font_path = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
    font = ImageFont.truetype(font_path, 20)
    
    # Find all bounding boxes in the text
    pattern = r'\[(.*?)\]\((\d+)\s(\d+)\s(\d+)\s(\d+)\)'
    matches = re.findall(pattern, response_text)

    # print(matches)  # [('さらに表示', '204', '101', '246', '143'), ('Tweetリンクの共有ボタン', '903', '871', '926', '896')]

    for match in matches:
        # ラベルと座標を抽出
        label, y_min, x_min, y_max, x_max = match
        y_min, x_min, y_max, x_max = int(y_min), int(x_min), int(y_max), int(x_max)

        print("=== 取得したバウンディングボックス ====")
        print(label, y_min, x_min, y_max, x_max)
        print()
        print()
        
        # 1000x1000の空間から百分率に変換
        x_min_pct = x_min / 1000
        y_min_pct = y_min / 1000
        x_max_pct = x_max / 1000
        y_max_pct = y_max / 1000

        # 変換後の座標を表示（オプション）
        print("=== 百分率に変換したバウンディングボックス ====")
        print(label, y_min_pct, x_min_pct, y_max_pct, x_max_pct)
        print()
        print()

        # 四角形を描画
        draw.rectangle(
            [
                x_min_pct * image_width, y_min_pct * image_height, 
                x_max_pct * image_width, y_max_pct * image_height
            ],
            outline="red", width=2
        )

        # ラベルを描画
        draw.text(
            (x_min_pct * image_width, y_min_pct * image_height - 20), 
            label, font=font, fill="red"
        )
    
    # RGBAモードの場合、RGBに変換
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # 画像を保存する
    image.save(output_path)