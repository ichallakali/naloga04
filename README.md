# Meme Generator (Dockerized Flask App)

This project is a simple **Meme Generator** web application built with **Python**, **Flask**, and **Pillow**, and packaged to run inside a **Docker** container.

The user can:
- upload an image via a web form,
- enter top and bottom text (classic meme format),
- generate a new image with the text rendered on top of the original,
- view the generated meme directly in the browser.

---

## Technologies

- **Language**: Python 3
- **Web framework**: Flask
- **Image processing**: Pillow
- **Containerization**: Docker (optionally docker-compose)

---

## How it works (processing steps)

1. The user selects an image file and enters top and bottom text in the HTML form.
2. Flask receives the uploaded file and temporarily saves it in the `static/memes` directory.
3. Using Pillow, the app opens the image, draws the text (with outline) at the top and bottom of the image, and saves a new JPEG file (the meme).
4. The app then returns an HTML page that displays the generated meme via an `<img>` tag pointing to `static/memes/...`.

---

## Running locally (without Docker)

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py

Docker run commands

docker build -t meme-generator .
docker run -p 5000:5000 meme-generator

