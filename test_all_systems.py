import asyncio
import os
from dotenv import load_dotenv
from backend.field_reader import FieldReader

# Load Env
load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"🔑 API Key Loaded: {'Yes' if key else 'NO'}")

async def test_mode(mode_name, input_text):
    print(f"\n🧪 TESTING MODE: {mode_name.upper()}...")
    try:
        reader = FieldReader()
        # Mocking user_id as 0 for test
        response = await reader.get_field("test_field", input_text, mode=mode_name)
        if response and len(response) > 10:
            print(f"✅ {mode_name.upper()}: SUCCESS")
            print(f"   Response Preview: {response[:50]}...")
        else:
            print(f"❌ {mode_name.upper()}: EMPTY RESPONSE")
    except Exception as e:
        print(f"❌ {mode_name.upper()}: FAILED - {e}")

async def main():
    print("🚀 STARTING FINAL SYSTEM CHECK\n" + "="*30)
    
    tasks = [
        test_mode("alex_sales", "Я хочу купить виллу на бали, есть 200к. Что посоветуешь?"),
        test_mode("avito", "Продаю Айфон 14 про, экран разбит, батарея 90%, цена 40к"),
        test_mode("angry", "Вы уроды, верните деньги! Сервис говно!"),
        test_mode("ex", "Привет, хочу забрать свои вещи, когда можно?"),
        test_mode("boss", "Я проспал работу, придумай отмазку"),
        test_mode("toast", "День рождения друга, ему 30 лет, он программист"),
        test_mode("dome", "Tech specs for Airform")
    ]
    
    await asyncio.gather(*tasks)
    print("\n" + "="*30 + "\n🏁 CHECK COMPLETE")

if __name__ == "__main__":
    asyncio.run(main())
