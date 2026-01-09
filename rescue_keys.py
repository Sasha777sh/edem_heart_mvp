import google.generativeai as genai
import os

KEYS = [
    "AIzaSyCk-wQrBF2waR5QkVT8L4nM1iI2Dvhfs_I",
    "AIzaSyCWOh5jhFXqj1zC_LKCB3UquqOLPDu-PUI",
    "AIzaSyDHncv5whBK5b9I6NNgeA98VWHeGtnhwVI"
]

print(f"Testing {len(KEYS)} keys for survival...")

for i, key in enumerate(KEYS):
    print(f"\n--- Testing Key #{i+1}: ...{key[-4:]} ---")
    genai.configure(api_key=key)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Ping")
        print(f"✅ ALIVE! Response: {response.text.strip()}")
        print(f"!!! FOUND VALID KEY: {key} !!!")
        exit(0)
    except Exception as e:
        print(f"❌ DEAD: {e}")

print("\n❌❌❌ ALL KEYS ARE DEAD.")
exit(1)
