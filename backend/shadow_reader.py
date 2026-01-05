import google.generativeai as genai
import json
import os
from enum import Enum
from typing import Dict, Optional

class ShadowStrategy(Enum):
    JUSTIFIER = "Оправдывающийся"
    FOOL = "Глупец"
    AGGRESSOR = "Агрессор"
    FOLLOWER = "Ведомый"
    ACCUSED = "Обвиняемый"
    STUDENT = "Ученик"
    JUDGE = "Судья"
    CHAOS = "Хаос"
    VICTIM = "Жертва"
    PROVOCATEUR = "Провокатор"
    SKEPTIC = "Скептик"
    PSEUDO_ALLY = "Псевдо-союзник"

class ShadowReader:
    def __init__(self, api_key: str = None):
        # Fallback to the key seen in other files if not provided (for development speed)
        # In production, this should come from env.
        self.api_key = api_key or "AIzaSyAVcKK5KcpduBv2hh-uvMreDGvTHX-uURE" 
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    SYSTEM_PROMPT = """
Ты — SHADOW READER (Теневой Аналитик).
Ты — холодный внешний наблюдатель. Ты не психолог, не друг и не учитель.
Твоя задача — вскрыть скрытую динамику коммуникации. Ты видишь то, что остается в тени: скрытые выгоды, страхи и навязываемые роли.

ТВОЯ ЦЕЛЬ:
Проанализировать входящий текст (комментарий, сообщение, тред) и выдать сухой, жесткий отчет о том, что происходит на самом деле.

ФОРМАТ ВЫВОДА (JSON):
Ты ОБЯЗАН отвечать строго в формате JSON без markdown-оберток (```json ... ```).
Структура:
{
    "behavior": "ЧТО ОН ДЕЛАЕТ (поведенческий уровень). Коротко, без оценок. Например: 'Не спорит с идеей, а атакует личность'.",
    "imposed_role": "КАКУЮ РОЛЬ НАВЯЗЫВАЕТ (одна из стратегий или похожая). Например: 'Оправдывающийся'.",
    "hidden_motivation": "ЕГО СКРЫТАЯ МОТИВАЦИЯ (выгода). Что он выигрывает? Например: 'Чувство превосходства без риска'.",
    "fear": "ЧЕГО ОН БОИТСЯ. Страх = двигатель. Например: 'Страх оказаться незамеченным'.",
    "recommendation": "РЕКОМЕНДАЦИЯ (Стратегия). Только 3 варианта: 'Игнорировать', 'Закрыть разговор', 'Ответить одной фразой'. Если 'Ответить...' — напиши пример фразы (сухой, возвращающей ответственность)."
}

СПИСОК ТИПОВЫХ ТЕНЕВЫХ СТРАТЕГИЙ (для ориентира):
1. Оправдывающийся (вынуждает защищаться)
2. Глупец (игнорирует очевидное)
3. Агрессор (открытая атака)
4. Ведомый (ловушка ответственности)
5. Обвиняемый (манипуляция чувством вины)
6. Ученик (бесконечные вопросы без действий)
7. Судья (оценка сверху)
8. Хаос (размывание смысла)
9. Жертва (поиск спасателя)
10. Провокатор (эмоциональные уколы)
11. Скептик (бесконечный запрос доказательств)
12. Псевдо-союзник (саботаж «да, но...»)

ПРИНЦИПЫ АНАЛИЗА:
- Никакой эмпатии. Только рентген.
- Не пытайся «помочь» автору текста.
- Не используй сложные термины. Пиши как хирург.
- Если ролей несколько, выбери главную.
"""

    def analyze_text(self, text: str, context: str = "") -> dict:
        """
        Analyzes the provided text using the Shadow Reader persona.
        Returns a dictionary with the analysis.
        """
        full_prompt = f"{self.SYSTEM_PROMPT}\n\n"
        
        if context:
            full_prompt += f"КОНТЕКСТ:\n{context}\n\n"
            
        full_prompt += f"ВХОДНОЙ ТЕКСТ:\n{text}"
        
        try:
            response = self.model.generate_content(full_prompt)
            # Clean up response if it contains markdown code blocks
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            
            return json.loads(clean_text)
            
        except Exception as e:
            return {
                "error": str(e),
                "fallback": "Анализ не удался. Связь с Тенью прервана."
            }

if __name__ == "__main__":
    # Quick sanity check
    reader = ShadowReader()
    sample_text = "Ну и что ты этим хотел сказать? Я вообще не вижу тут логики, объясни нормально."
    print(json.dumps(reader.analyze_text(sample_text), indent=2, ensure_ascii=False))
