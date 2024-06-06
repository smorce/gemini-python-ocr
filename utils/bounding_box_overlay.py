# 以下に、BoundingBoxOverlayのPython実装を修正して、predict_imageのレスポンスを使用するようにし、バウンディングボックスを入力画像に描画してPILで表示するようにします。

import json
from PIL import Image, ImageDraw, ImageFont
from my_project.utils.extract import extract_json_from_markdown

def BoundingBoxOverlay(image_path, response):
    formatted = []
    try:
        raw_extracted = extract_json_from_markdown(response)
        name_counts = {}
        edited = []

        for line in raw_extracted.split("\n"):
            name = line.split(":")[0].strip().split('"')[1]
            if name:
                if name in name_counts:
                    name_counts[name] += 1
                    edited.append(line.replace(name, f"{name}_{name_counts[name]}"))
                else:
                    name_counts[name] = 1
                    edited.append(line)
            else:
                edited.append(line)

        raw_extracted_unique = "\n".join(edited)
        json_data = json.loads(raw_extracted_unique)
        box_keys = json_data.keys()

        for key in box_keys:
            coords = json_data[key]
            formatted.append({
                "name": key,
                "coords": {
                    "x": coords[1] / 1000,
                    "y": coords[0] / 1000,
                    "width": (coords[3] - coords[1]) / 1000,
                    "height": (coords[2] - coords[0]) / 1000,
                }
            })
    except Exception as e:
        print(e)

    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Draw bounding boxes
    for obj in formatted:
        coords = obj["coords"]
        left = coords["x"] * image.width
        top = coords["y"] * image.height
        right = left + coords["width"] * image.width
        bottom = top + coords["height"] * image.height

        draw.rectangle([left, top, right, bottom], outline="red", width=2)
        draw.text((left, bottom), obj["name"], fill="red", font=font)

    image.show()
