from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI

# اقرأ الـ API Key من متغيرات البيئة
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()

# السماح لصفحة GitHub Pages أو أي موقع آخر بالاتصال بالـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يفضّل لاحقًا تحديد دومين موقعك فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RushdRequest(BaseModel):
    category: str
    description: str

@app.post("/rushd")
async def get_rushd_advice(req: RushdRequest):
    """
    API بسيط يستقبل (category + description) ويرجع رد عربي من رُشد.
    """
    # نبني برومبت منظم بالعربي
    system_prompt = """
    أنت مساعد استشارات قيادية عربي باسم (رُشد).
    أسلوبك عملي، داعم، وواضح. تخاطب القائدة بصيغة المؤنث.
    المطلوب منك:
    - أن تلخّصي فهمك للموقف في سطرين.
    - أن تقدمي من 3 إلى 6 نقاط عملية واضحة (خطوات أو زوايا تفكير).
    - أن تختمي بخطوة صغيرة يمكن تنفيذها خلال 24 ساعة.
    لا تذكري أنك نموذج ذكاء اصطناعي، ولا تكتبي أكواد، اكتبي نصًا عربيًا فقط.
    """

    user_prompt = f"""
    التصنيف: {req.category}
    وصف الموقف:
    {req.description}
    """

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",  # أو gpt-4.1 أو gpt-5.1 حسب خطتك
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.4,
        max_tokens=700,
    )

    answer = completion.choices[0].message.content
    return {"answer": answer}
