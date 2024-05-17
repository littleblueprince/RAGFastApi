from fastapi import FastAPI, File, UploadFile, Request,HTTPException
from typing import List


app = FastAPI()


@app.get("/")
async def root():
    return "hello world!"


# @app.post("/extract_pdf")
# async def extract_pdf(request: Request):
#     data = await request.json()
#     pdf_file_path = data.get('pdf_file_path')
#     return process_pdf(pdf_file_path)


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    file_details = []
    print(len(files))
    for file in files:
        # 检查文件是否以 .pdf 结尾
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF.")
        # 保存文件到指定目录
        contents = await file.read()
        file_location = f"./data/pdf_data/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(contents)

        # 将文件详情添加到列表中
        file_details.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "file_location": file_location
        })

    return {"file_details": file_details}
