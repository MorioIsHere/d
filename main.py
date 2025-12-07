from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from PIL import Image
import os
import math

app = FastAPI()

# create public folder if not exists
os.makedirs("public", exist_ok=True)

# serve static files for generated images
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.post("/makeImage")
async def make_image(request: Request):
    try:
        data = await request.json()
        width = data.get("width")
        rgb = data.get("rgb")

        if not width or not rgb:
            return JSONResponse({"error": "Missing width or rgb"}, status_code=400)

        height = math.ceil(len(rgb) / width)

        img = Image.new("RGB", (width, height))
        pixels = img.load()

        for i, (r, g, b) in enumerate(rgb):
            x = i % width
            y = i // width
            pixels[x, y] = (r, g, b)

        filename = f"{uuid4()}.png"
        filepath = os.path.join("public", filename)

        img.save(filepath, "PNG")

        host = request.headers.get("host")
        protocol = "https"
        url = f"{protocol}://{host}/public/{filename}"

        return {"url": url}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)