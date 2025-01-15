"""
⚙️ TGBot-for-Orders - Created by Marc ⚙️

📄 License: Custom License Agreement
Copyright © 2025 Marc. All rights reserved.

🚫 Unauthorized use, copying, modification, or distribution of this software is strictly prohibited.
❗ Violators will be prosecuted under international copyright law.

⚠️ WARNING: Misuse of this code will lead to legal action. Unauthorized users may face endless debugging hell.

🔒 By using this software, you agree to these terms.
"""


# === HANDLERS ===
# Регистрация хендлеров
from telebot import types
from catalog import bearbrick_catalog
from utils import send_resized_photo
import os
import csv

# User data dictionary to store user input during the order process
user_data = {}

# Функция для сохранения заказа в CSV
file_path = "orders.csv"
header = ["Name", "Surname", "Phone Number", "Pickup Location", "Model", "Price"]

def save_order_to_csv(order):
    try:
        # Проверяем, существует ли файл
        file_exists = os.path.isfile(file_path)

        # Записываем в файл
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(header)  # Добавляем заголовок только если файл новый
            writer.writerow([
                order['name'],
                order['surname'],
                order['phone_number'],
                order['pickup_location'],
                order['model']['name'],
                order['model']['price']
            ])
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Регистрация всех хендлеров

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        item_price = types.KeyboardButton("📋 View Catalog")
        item_order = types.KeyboardButton("🛒 Place an Order")
        markup.add(item_price, item_order)
        bot.send_message(
            message.chat.id,
            "👋 Welcome to the Bearbrick Store! Here you can view our catalog and place an order without waiting for a response from an operator.",
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: message.text == "📋 View Catalog")
    def handle_show_catalog(message):
        for size, models in bearbrick_catalog.items():
            bot.send_message(message.chat.id, f"🔹 *Размер: {size}*", parse_mode="Markdown")
            for model in models:
                send_resized_photo(
                    bot,
                    message.chat.id,
                    model['image_url'],
                    f"🧸 {model['name']}\n💰 Цена: {model['price']} EUR"
                )

    @bot.message_handler(func=lambda message: message.text == "🛒 Place an Order")
    def handle_order(message):
        chat_id = message.chat.id
        user_data[chat_id] = {}

        # Show Bearbrick sizes
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for size in bearbrick_catalog.keys():
            markup.add(types.KeyboardButton(size))

        bot.send_message(chat_id, "Please select a Bearbrick size:", reply_markup=markup)
        bot.register_next_step_handler(message, process_size)

    def process_size(message):
        chat_id = message.chat.id
        selected_size = message.text

        if selected_size not in bearbrick_catalog:
            bot.send_message(chat_id, "Invalid selection. Please try again.")
            return

        user_data[chat_id]['size'] = selected_size

        # Show models for the selected size
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for model in bearbrick_catalog[selected_size]:
            markup.add(types.KeyboardButton(model['name']))

        bot.send_message(chat_id, "Please select a Bearbrick model:", reply_markup=markup)
        bot.register_next_step_handler(message, process_model)

    def process_model(message):
        chat_id = message.chat.id
        selected_model = message.text

        # Find the model in the catalog
        size = user_data[chat_id]['size']
        model = next((m for m in bearbrick_catalog[size] if m['name'] == selected_model), None)

        if not model:
            bot.send_message(chat_id, "Invalid selection. Please try again.")
            return

        user_data[chat_id]['model'] = model
        bot.send_photo(
            chat_id,
            model['image_url'],
            caption=f"🧸 {model['name']}\n💰 Цена: {model['price']} EUR",
            reply_markup=create_confirmation_markup()
        )

    def create_confirmation_markup():
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Confirm", callback_data="confirm_order"),
            types.InlineKeyboardButton("✏️ Change Model", callback_data="change_model")
        )
        return markup

    @bot.callback_query_handler(func=lambda call: call.data in ["confirm_order", "change_model"])
    def handle_confirmation(call):
        chat_id = call.message.chat.id

        if call.data == "confirm_order":
            bot.send_message(chat_id, "Order confirmed! Proceeding to checkout.")
            process_checkout(call.message)
        elif call.data == "change_model":
            bot.send_message(chat_id, "Let's start over. Please select a size:")
            handle_order(call.message)

    def process_checkout(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "Great! Now, please enter your first name (letters only):")
        bot.register_next_step_handler(message, process_name)

    def process_name(message):
        chat_id = message.chat.id
        if not message.text.isalpha():
            bot.send_message(chat_id, "Please enter a valid first name (letters only).")
            bot.register_next_step_handler(message, process_name)
            return

        user_data[chat_id]['name'] = message.text
        bot.send_message(chat_id, "Great! Now, please enter your surname (letters only):")
        bot.register_next_step_handler(message, process_surname)

    def process_surname(message):
        chat_id = message.chat.id
        if not message.text.isalpha():
            bot.send_message(chat_id, "Please enter a valid surname (letters only).")
            bot.register_next_step_handler(message, process_surname)
            return

        user_data[chat_id]['surname'] = message.text
        bot.send_message(
            chat_id,
            "Great! Now, please enter your phone number (digits only):"
        )
        bot.register_next_step_handler(message, process_phone_number)

    def process_phone_number(message):
        chat_id = message.chat.id
        if not message.text.isdigit():
            bot.send_message(chat_id, "Please enter a valid phone number (digits only).")
            bot.register_next_step_handler(message, process_phone_number)
            return

        user_data[chat_id]['phone_number'] = message.text
        bot.send_message(chat_id, "Now, please enter your pickup location:")
        bot.register_next_step_handler(message, process_pickup_location)

    def process_pickup_location(message):
        chat_id = message.chat.id
        user_data[chat_id]['pickup_location'] = message.text
        finalize_order(chat_id)

    def finalize_order(chat_id):
        model = user_data[chat_id]['model']
        order_info = (
            f"🧾 **Order Summary**\n"
            f"👤 Name: {user_data[chat_id]['name']} {user_data[chat_id]['surname']}\n"
            f"📞 Phone: {user_data[chat_id]['phone_number']}\n"
            f"📍 Pickup Location: {user_data[chat_id]['pickup_location']}\n"
            f"🧸 Model: {model['name']}\n"
            f"💰 Price: {model['price']} EUR"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Confirm Order", callback_data="final_confirm"),
            types.InlineKeyboardButton("✏️ Edit Order", callback_data="edit_order")
        )

        # Отправляем фото с кнопками
        bot.send_photo(chat_id, model['image_url'], caption=order_info, parse_mode="Markdown", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data in ["final_confirm", "edit_order"])
    def handle_final_confirmation(call):
        chat_id = call.message.chat.id

        if call.data == "final_confirm":
            save_order_to_csv(user_data[chat_id])
            bot.send_message(chat_id, "Thank you! Your order has been saved.")
        elif call.data == "edit_order":
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            markup.add("Change Name", "Change Surname")
            markup.add("Change Phone", "Change Model")
            markup.add("Change Pickup Location", "Start Over")

            bot.send_message(chat_id, "What would you like to edit?", reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text.startswith("Change "))
    # Функция изменения данных заказа

    @bot.message_handler(func=lambda message: message.text.startswith("Change "))
    @bot.message_handler(func=lambda message: message.text.startswith("Change "))
    def handle_edit_request(message):
        chat_id = message.chat.id
        field_to_edit = message.text.replace("Change ", "").lower()

        if field_to_edit == "name":
            bot.send_message(chat_id, "Please enter your new first name:")
            bot.register_next_step_handler(message, lambda msg: process_edit(chat_id, "name", msg.text))

        elif field_to_edit == "surname":
            bot.send_message(chat_id, "Please enter your new surname:")
            bot.register_next_step_handler(message, lambda msg: process_edit(chat_id, "surname", msg.text))

        elif field_to_edit == "phone":
            bot.send_message(chat_id, "Please enter your new phone number:")
            bot.register_next_step_handler(message, lambda msg: process_edit(chat_id, "phone_number", msg.text))

        elif field_to_edit == "pickup location":
            bot.send_message(chat_id, "Please enter your new pickup location:")
            bot.register_next_step_handler(message, lambda msg: process_edit(chat_id, "pickup_location", msg.text))

        elif field_to_edit == "model":
            bot.send_message(chat_id, "Let's select your Bearbrick model again. Please choose a size:")
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            for size in bearbrick_catalog.keys():
                markup.add(types.KeyboardButton(size))
            bot.send_message(chat_id, "Select size:", reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: process_size_for_edit(chat_id, msg))

    def process_size_for_edit(chat_id, message):
        selected_size = message.text
        if selected_size not in bearbrick_catalog:
            bot.send_message(chat_id, "Invalid size selection. Please try again.")
            return

        user_data[chat_id]['size'] = selected_size
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for model in bearbrick_catalog[selected_size]:
            markup.add(types.KeyboardButton(model['name']))

        bot.send_message(chat_id, "Please select a Bearbrick model:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: process_model_for_edit(chat_id, msg))

    def process_model_for_edit(chat_id, message):
        selected_model = message.text
        size = user_data[chat_id]['size']
        model = next((m for m in bearbrick_catalog[size] if m['name'] == selected_model), None)

        if not model:
            bot.send_message(chat_id, "Invalid model selection. Please try again.")
            return

        user_data[chat_id]['model'] = model
        bot.send_photo(
            chat_id,
            model['image_url'],
            caption=f"🧸 {model['name']}\n💰 Цена: {model['price']} EUR",
            parse_mode="Markdown"
        )

        show_order_summary(chat_id)

    def process_edit(chat_id, field, new_value):
        if chat_id in user_data:
            user_data[chat_id][field] = new_value
            bot.send_message(chat_id, f"Your {field} has been updated.")

        show_order_summary(chat_id)


    def show_order_summary(chat_id):
        model = user_data[chat_id]['model']
        order_info = (
            f"🧾 **Order Summary**\n"
            f"👤 Name: {user_data[chat_id]['name']} {user_data[chat_id]['surname']}\n"
            f"📞 Phone: {user_data[chat_id]['phone_number']}\n"
            f"📍 Pickup Location: {user_data[chat_id]['pickup_location']}\n"
            f"🧸 Model: {model['name']}\n"
            f"💰 Price: {model['price']} EUR"
        )

        bot.send_photo(chat_id, model['image_url'], caption=order_info, parse_mode="Markdown")

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Confirm Order", callback_data="final_confirm"),
            types.InlineKeyboardButton("✏️ Edit Order", callback_data="edit_order")
        )
        bot.send_message(chat_id, "Would you like to confirm your order or edit it?", reply_markup=markup)