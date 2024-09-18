from fastapi import APIRouter, HTTPException, Body
from app.utils import scrape_url, extract_pdf_text, find_most_relevant
import uuid
from fastapi import File, UploadFile

router = APIRouter()

db = {}

@router.post("/process_url")
async def process_url(url: str = Body(..., embed=True)):
    try:
        content = await scrape_url(url)
        chat_id = str(uuid.uuid4())
        db[chat_id] = content 
        return {"chat_id": chat_id, "message": "URL content processed and stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error processing the URL.")




@router.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        content = await extract_pdf_text(file.file)
        chat_id = str(uuid.uuid4())
        db[chat_id] = content
        return {"chat_id": chat_id, "message": "PDF content processed and stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error processing the PDF.")



@router.post("/chat")
async def chat(chat_id: str = Body(..., embed=True), question: str = Body(..., embed=True)):
    try:
        if chat_id not in db:
            raise HTTPException(status_code=404, detail="Chat ID not found.")
        
        content = db[chat_id]
        relevant_response = find_most_relevant(content, question)
        
        return {"response": relevant_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error in chat processing.")
