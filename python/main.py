import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import PlainTextResponse, JSONResponse

from llm import (
    setup_and_load_models,
    transcribe_audio,
    generate_new_shopping_list_item,
)

app = FastAPI()
language_model, tokenizer, whisper_pipe = setup_and_load_models()


@app.post(
    path="/media",
    response_class=JSONResponse,
)
async def post_media_file(file: UploadFile):
    """
    Receive File, store to disk & return it
    """
    with open(file.filename, "wb") as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
        print(
            f"Received file named {file.filename} containing {len(file_bytes)} bytes. "
        )
        transcribed_content = transcribe_audio(whisper_pipe, file.filename)
        new_shopping_list_item = generate_new_shopping_list_item(
            language_model, tokenizer, transcribed_content
        )
        return {"new_item": new_shopping_list_item.strip()}


@app.get(
    path="/local",
    response_class=PlainTextResponse
)
async def post_file_name(file_name: str):
    """
    Receive a local file name, load it from disk & return it
    """
    print(f"Received file name {file_name}")
    transcribed_content = transcribe_audio(whisper_pipe, f"../{file_name}")
    new_shopping_list_item = generate_new_shopping_list_item(
        language_model, tokenizer, transcribed_content
    )
    return new_shopping_list_item.strip()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
