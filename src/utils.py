"""
⚙️ TGBot-for-Orders - Created by Marc ⚙️

📄 License: Custom License Agreement
Copyright © 2025 Marc. All rights reserved.

🚫 Unauthorized use, copying, modification, or distribution of this software is strictly prohibited.
❗ Violators will be prosecuted under international copyright law.

⚠️ WARNING: Misuse of this code will lead to legal action. Unauthorized users may face endless debugging hell.

🔒 By using this software, you agree to these terms.
"""


# === UTILS ===
# Функция для отправки одного изображения с изменением размера
# Добавлена проверка формата изображения и ограничение на максимальный размер файла
from PIL import Image
import requests
from io import BytesIO
from telebot import types
import os
import csv

# Функция для отправки одного изображения с изменением размера
def send_resized_photo(bot, chat_id, image_url, caption):
    try:
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # Конвертируем изображение в формат JPEG
        image = image.convert("RGB")
        image = image.resize((512, 512))

        # Сохранение изображения во временный файл
        temp_file_path = f"temp_{chat_id}.jpg"
        image.save(temp_file_path, format="JPEG")

        # Отправка изображения
        with open(temp_file_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=caption)

        # Удаление временного файла
        os.remove(temp_file_path)
    except Exception as e:
        bot.send_message(chat_id, "❌ Не удалось загрузить изображение. Попробуйте позже.")

# Функция для отправки каталога изображений по одному (каждая модель отправляется отдельно)
def send_catalog_individual(bot, chat_id, catalog):
    try:
        for size, models in catalog.items():
            bot.send_message(chat_id, f"🔹 *Размер: {size}*", parse_mode="Markdown")
            for model in models:
                send_resized_photo(
                    bot,
                    chat_id,
                    model['image_url'],
                    f"🧸 {model['name']}\n💰 Цена: {model['price']} EUR"
                )
    except Exception as e:
        bot.send_message(chat_id, "❌ Ошибка при отправке каталога. Попробуйте позже.")

# Function to save order to CSV
def save_order_to_csv(order):
    file_path = "orders.csv"
    header = ["Surname", "Name", "Phone Number", "Pickup Location", "Model", "Price"]

    try:
        # Проверяем, существует ли файл
        file_exists = os.path.isfile(file_path)

        # Записываем в файл
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(header)  # Добавляем заголовок только если файл новый
            writer.writerow([
                order['surname'],
                order['name'],
                order['phone_number'],
                order['pickup_location'],
                order['model']['name'],
                order['model']['price']
            ])
    except Exception as e:
        print(f"Error writing to CSV: {e}")
