from fastapi import FastAPI, Header, HTTPException, Request, status
from pydantic import BaseModel
from dotenv import load_dotenv
import hmac, os

load_dotenv()

app = FastAPI()



# # تعريف نموذج البيانات المتوقع استقباله من سلة (الإصدار V1)
# class SallaWebhookPayload(BaseModel):
#     event: str | None = None
#     merchant: int | None = None
#     created_at: str | None = None
#     data: dict | None = None  # تفاصيل الفاتورة أو الطلب




@app.post("/new-order")
async def receive_salla_webhook(
    request: Request,
    x_api_key_v2: str | None = Header(None, alias="x-api-key-v2")
):
    # 1. التحقق من مفتاح الأمان (API Key) المطابق لما وضُع في لوحة تحكم سلة
    EXPECTED_API_KEY = os.getenv("SALLA_API_KEY")
    print(EXPECTED_API_KEY)

    if not EXPECTED_API_KEY or not x_api_key_v2 or not hmac.compare_digest(x_api_key_v2, EXPECTED_API_KEY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")
    
    # 2. استقبال البيانات بصيغة JSON
    try:
        payload = await request.json()
        print("Raw Payload", payload)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload"
        )
    
    # 3. معالجة البيانات (مثل إرسال المنتج الرقمي للعميل، تخزينها في قاعدة البيانات، إلخ)
    # print("Received Salla Webhook Data:", payload)
    
    # استخراج بعض التفاصيل كمثال
    event_type = payload.get("event")
    order_data = payload.get("data", {})
    
    # TODO: أضف منطق تسليم المنتجات الرقمية هنا
    
    # 4. الرد على سلة بأن العملية تمت بنجاح (ضروري لكي لا تقوم سلة بإعادة إرسال الويب هوك)
    return {"status": "success", "message": "Webhook received successfully"}


@app.get("/")
def read_root():
    return {"message": "Salla API, V1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("salla-api:app", host="0.0.0.0", port=8711, reload=True)# dev
    # uvicorn.run(app, host="0.0.0.0", port=8711)# prod
