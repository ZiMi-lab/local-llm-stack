from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List
import os
import shutil

app = FastAPI()

# Seznam tokenů se načítá z proměnné prostředí BACKEND_VALID_TOKENS,
# kterou si uživatel definuje v .env (odkazy dole).
#
# Např. .env může obsahovat:
#   BACKEND_VALID_TOKENS="asdjklhasdkjhasd==, asdasdkjyhasdkjh=="
#
# V kódu se tokeny rozdělí podle čárek a uloží do seznamu.
tokens_str = os.environ.get("BACKEND_VALID_TOKENS", "")
VALID_TOKENS = [token.strip() for token in tokens_str.split(",") if token.strip()]

@app.post("/upload")
async def upload_files(
    token: str = Form(...),
    target_dir: str = Form(...),
    files: List[UploadFile] = File(...)
):
    # Ověříme, zda token patří do seznamu
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")

    upload_path = os.path.join("/uploads", target_dir)
    os.makedirs(upload_path, exist_ok=True)

    ulozene_soubory = []
    for file in files:
        destination = os.path.join(upload_path, file.filename)
        with open(destination, "wb") as f:
            shutil.copyfileobj(file.file, f)
        ulozene_soubory.append(file.filename)

    return {"status": "ok", "uploaded": ulozene_soubory}
