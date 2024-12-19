import random
import string

def generate_password(length: int = 12):
    if length < 8 or length > 20:
        raise ValueError("Длина пароля должна быть от 8 до 20 символов.")

    # Обязательные группы символов
    lowercase = random.choice(string.ascii_lowercase)  # Минимум одна строчная буква
    uppercase = random.choice(string.ascii_uppercase)  # Минимум одна заглавная буква
    digit = random.choice(string.digits)              # Минимум одна цифра
    special = random.choice("!@#$%^&*")               # Минимум один специальный символ

    # Оставшиеся символы
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining_length = length - 4
    other_characters = ''.join(random.choices(all_characters, k=remaining_length))

    # Собираем пароль и перемешиваем
    password = list(lowercase + uppercase + digit + special + other_characters)
    random.shuffle(password)

    return ''.join(password)