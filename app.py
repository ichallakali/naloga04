import os
import uuid

from flask import Flask, render_template, request, url_for
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

GENERATED_DIR = os.path.join("static", "memes")
os.makedirs(GENERATED_DIR, exist_ok=True)

DEFAULT_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def draw_text_with_outline(draw, position, text, font, fill="white", outline="black", stroke_width=3):
    draw.text(
        position,
        text,
        font=font,
        fill=fill,
        stroke_fill=outline,
        stroke_width=stroke_width,
        anchor="mm",
    )


def create_meme(image_path, top_text, bottom_text):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    try:
        font_size = int(height / 10)
        font = ImageFont.truetype(DEFAULT_FONT_PATH, font_size)
    except OSError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    draw_text_with_outline(
        draw,
        position=(width / 2, height * 0.1),
        text=top_text,
        font=font,
    )

    draw_text_with_outline(
        draw,
        position=(width / 2, height * 0.9),
        text=bottom_text,
        font=font,
    )

    filename = f"meme_{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(GENERATED_DIR, filename)
    img.save(output_path, format="JPEG")

    return filename


@app.route("/", methods=["GET", "POST"])
def index():
    meme_url = None

    if request.method == "POST":
        file = request.files.get("image")
        top_text = request.form.get("top_text", "")
        bottom_text = request.form.get("bottom_text", "")

        if file and file.filename:
            temp_path = os.path.join(GENERATED_DIR, f"upload_{uuid.uuid4().hex}.jpg")
            file.save(temp_path)

            meme_filename = create_meme(temp_path, top_text, bottom_text)
            meme_url = url_for("static", filename=f"memes/{meme_filename}")

            try:
                os.remove(temp_path)
            except OSError:
                pass

    return render_template("index.html", meme_url=meme_url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
