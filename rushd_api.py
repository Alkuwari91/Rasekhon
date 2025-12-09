from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from openai import OpenAI

# إنشاء عميل OpenAI باستخدام المتغير البيئي
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    # فقط للـ debug في السيرفر (لن يظهر للمستخدم)
    print("⚠️ OPENAI_API_KEY is not set in environment variables")
client = OpenAI(api_key=api_key)

app = FastAPI()

# السماح للمتصفح بالوصول من أي دومين (ممكن تضيقينه لاحقًا)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # يفضَّل لاحقًا وضع دومين موقعك فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RushdRequest(BaseModel):
    category: str
    description: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "Rushd API is running"}

@app.post("/rushd")
async def get_rushd_advice(req: RushdRequest):
    """
    يستقبل (category + description) ويرجع رد عربي من رُشد.
    """
    system_prompt = """
    أنت مساعد استشارات قيادية عربي باسم (رُشد).
    أسلوبك عملي، داعم، وواضح. تخ
