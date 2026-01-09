import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv
from typing import Dict, Optional, Union

load_dotenv()

from backend.prompts import (
    COLD_SYSTEM_PROMPT,
    RED_FLAG_SYSTEM_PROMPT,
    DREAM_SYSTEM_PROMPT,
    MED_SYSTEM_PROMPT,
    PAPER_SYSTEM_PROMPT,
    REELS_SYSTEM_PROMPT,
    RED_FLAG_PREMIUM_PROMPT,
    DREAM_PREMIUM_PROMPT,
    MED_PREMIUM_PROMPT,
    PAPER_PREMIUM_PROMPT,
    PSYCHO_SYSTEM_PROMPT,
    PSYCHO_PREMIUM_PROMPT,
    PROMPT_SYSTEM_PROMPT,
    PROMPT_PREMIUM_PROMPT,
    MARKETPLACE_SYSTEM_PROMPT,
    MARKETPLACE_PREMIUM_PROMPT,
    DOME_SYSTEM_PROMPT,
    DOME_PREMIUM_PROMPT,
    ALEX_SALES_PROMPT,
    ALEX_PREMIUM_PROMPT,
    RISK_SCANNER_SYSTEM_PROMPT,
    RISK_SCANNER_SYSTEM_PROMPT,
    RISK_AUDITOR_PREMIUM_PROMPT,
    AVITO_WRITER_PROMPT,
    ANGRY_CLIENT_PROMPT,
    MESSAGE_TO_EX_PROMPT,
    MESSAGE_TO_BOSS_PROMPT,
    TOAST_MASTER_PROMPT
)
from backend.privacy import sanitize_personal_data, is_safe_to_send

class FieldReader:
    def __init__(self, api_key: str = None):
        # 1. Try env var first
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            print("⚠️ FieldReader Error: No GEMINI_API_KEY found in env or .env!")
            # Do NOT use a hardcoded key in production
        else:
            genai.configure(api_key=self.api_key)
            
        self.model = genai.GenerativeModel('gemini-2.0-flash') # Updated to latest stable model

    def _get_prompt(self, mode: str) -> str:
        # FACTORY MODES
        if mode == "reels": return REELS_SYSTEM_PROMPT
        
        # PREMIUM MODES
        if mode == "red_flag_premium": return RED_FLAG_PREMIUM_PROMPT
        if mode == "dream_premium": return DREAM_PREMIUM_PROMPT
        if mode == "med_premium": return MED_PREMIUM_PROMPT
        if mode == "paper_premium": return PAPER_PREMIUM_PROMPT
        if mode == "psycho_premium": return PSYCHO_PREMIUM_PROMPT
        if mode == "prompts_premium": return PROMPT_PREMIUM_PROMPT
        if mode == "market_premium": return MARKETPLACE_PREMIUM_PROMPT
        if mode == "dome_premium": return DOME_PREMIUM_PROMPT
        if mode == "alex_premium": return ALEX_PREMIUM_PROMPT

        # STANDARD MODES
        if mode == "red_flag": return RED_FLAG_SYSTEM_PROMPT
        if mode == "dream": return DREAM_SYSTEM_PROMPT
        if mode == "med": return MED_SYSTEM_PROMPT
        if mode == "paper": return PAPER_SYSTEM_PROMPT
        if mode == "psycho": return PSYCHO_SYSTEM_PROMPT
        if mode == "prompts": return PROMPT_SYSTEM_PROMPT
        if mode == "market": return MARKETPLACE_SYSTEM_PROMPT
        if mode == "dome": return DOME_SYSTEM_PROMPT
        if mode == "alex_sales": return ALEX_SALES_PROMPT
        if mode == "alex_sales": return ALEX_SALES_PROMPT
        
        # MASS MARKET MODES
        if mode == "avito": return AVITO_WRITER_PROMPT
        if mode == "angry": return ANGRY_CLIENT_PROMPT
        if mode == "ex": return MESSAGE_TO_EX_PROMPT
        if mode == "boss": return MESSAGE_TO_BOSS_PROMPT
        if mode == "toast": return TOAST_MASTER_PROMPT

        if mode == "contract": return COLD_SYSTEM_PROMPT
        
        return COLD_SYSTEM_PROMPT # Default

    def download_file(self, file_id: str, bot_token: str) -> bytes:
        """
        Downloads a file from Telegram by file_id.
        """
        # 1. Get File Path
        get_file_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        r = requests.get(get_file_url)
        if r.status_code != 200:
            raise Exception("Failed to get file info from Telegram")
        
        file_path = r.json()['result']['file_path']
        
        # 2. Download Content
        download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        file_content = requests.get(download_url).content
        return file_content

    async def analyze_content(self, text: str = "", media_content: bytes = None, mime_type: str = None, mode: str = "red_flag") -> dict:
        """
        Analyzes text OR media (image/pdf) using Gemini 1.5 Flash.
        """
        system_prompt = self._get_prompt(mode)
        
        content_parts = [system_prompt]
        
        if text:
            # Sanitize personal data before sending to AI
            safe, reason = is_safe_to_send(text)
            if not safe:
                print(f"⚠️ Privacy Warning: {reason}")
            
            sanitized_text = sanitize_personal_data(text)
            content_parts.append(f"ВХОДНОЙ ТЕКСТ:\n{sanitized_text}")
            
        if media_content and mime_type:
            content_parts.append("ПРОАНАЛИЗИРУЙ ЭТОТ ФАЙЛ (Скриншот или Документ):")
            # Create a Part object
            cookie_picture = {
                'mime_type': mime_type,
                'data': media_content
            }
            content_parts.append(cookie_picture)
        
        try:
            # Generate content
            response = self.model.generate_content(content_parts)
            
            # Simple Text Response (since prompts ask for formatted text, not always JSON)
            # If we need structured JSON, we should enforce it in prompts, but user wants Design/Text.
            # The prompts currently ask for a structured markdown report.
            return {"raw_text": response.text}
            
        except Exception as e:
            return {
                "error": str(e),
                "raw_text": f"⚠️ **Ошибка анализа:** {str(e)}. Попробуйте отправить текст."
            }

if __name__ == "__main__":
    reader = FieldReader()
    print("FieldReader Initialized.")
