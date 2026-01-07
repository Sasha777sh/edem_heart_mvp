import re

def sanitize_personal_data(text):
    """
    Remove or mask personal data before sending to AI.
    
    Protects:
    - ФИО (Full names)
    - ИНН (Tax ID)
    - СНИЛС (Insurance number)
    - Passport numbers
    - Phone numbers
    - Email addresses
    - Bank card numbers
    """
    if not text:
        return text
    
    # Phone numbers (various formats)
    # +7 (999) 123-45-67, 8-999-123-45-67, etc.
    text = re.sub(r'\+?[78][\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}', '[ТЕЛЕФОН]', text)
    
    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # ИНН (12 or 10 digits)
    text = re.sub(r'\b\d{10}\b', '[ИНН]', text)
    text = re.sub(r'\b\d{12}\b', '[ИНН]', text)
    
    # СНИЛС (XXX-XXX-XXX XX)
    text = re.sub(r'\b\d{3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}\b', '[СНИЛС]', text)
    
    # Passport (4 digits + 6 digits)
    text = re.sub(r'\b\d{4}\s?\d{6}\b', '[ПАСПОРТ]', text)
    
    # Bank card numbers (16 digits)
    text = re.sub(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', '[КАРТА]', text)
    
    # Russian full names (Иванов Иван Иванович pattern)
    # This is tricky - we'll mask only if 3 capitalized words in a row
    text = re.sub(r'\b([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)ович|овна|евич|евна\b', '[ФИО]', text, flags=re.IGNORECASE)
    
    # Addresses (улица, дом, квартира patterns)
    text = re.sub(r'\bул\.\s+[А-ЯЁа-яё\s]+,?\s+д\.\s*\d+', '[АДРЕС]', text, flags=re.IGNORECASE)
    
    return text

def is_safe_to_send(text):
    """
    Check if text contains obvious personal data.
    Returns (is_safe, reason)
    """
    if not text:
        return True, None
    
    # Check for passport series/numbers
    if re.search(r'\b\d{4}\s?\d{6}\b', text):
        return False, "Обнаружен номер паспорта"
    
    # Check for ИНН
    if re.search(r'\b\d{12}\b', text):
        return False, "Обнаружен ИНН"
    
    # Check for СНИЛС
    if re.search(r'\b\d{3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}\b', text):
        return False, "Обнаружен СНИЛС"
    
    # Check for credit cards
    if re.search(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', text):
        return False, "Обнаружен номер карты"
    
    return True, None

# Test cases
if __name__ == "__main__":
    test_texts = [
        "Мой ИНН 123456789012 и телефон +7 (999) 123-45-67",
        "Email: ivan@example.com, карта 1234 5678 9012 3456",
        "Иванов Иван Иванович, паспорт 1234 567890",
        "Контракт на квартиру по ул. Ленина, д. 5"
    ]
    
    for text in test_texts:
        print(f"\nOriginal: {text}")
        print(f"Sanitized: {sanitize_personal_data(text)}")
        safe, reason = is_safe_to_send(text)
        print(f"Safe: {safe}, Reason: {reason}")
