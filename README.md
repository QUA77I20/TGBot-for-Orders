# 🧸 TGBot-for-Orders (Bearbrick Store Bot)

## 📋 Project Description
Bearbrick Store Bot is a Telegram bot designed to manage orders for collectible Bearbrick figures. It offers users an interactive interface to browse the catalog, select models, place orders, and edit order details.

### 💡 Main Features:
- View the Bearbrick catalog
- Select models and sizes
- Place an order with customer details
- Save orders in a CSV file
- Edit orders at any stage
- Interactive buttons for order confirmation or changes

---

## 🛠️ Technologies Used
- **Python 3.13**
- **PyTelegramBotAPI (telebot)** — for interacting with the Telegram API
- **dotenv** — for environment variable management
- **Pillow (PIL)** — for image processing
- **requests** — for handling external requests
- **CSV** — for storing order data
- **os** — for file system operations

---

## 🔮 Future Enhancements
The following features are planned for future releases:
- Migration to asynchronous handling (async polling and requests)
- Integration of a perceptron to predict popular models and process orders automatically
- Analytics and order data visualization
- Automated notifications to users about order status

---

## 🚀 How to Use
1. Install all dependencies from the `requirements.txt` file.
2. Run the bot using the command:
   ```bash
   python3 main.py
   ```
3. Set up the `.env` file with your Telegram API token:
   ```
   TELEGRAM_API_TOKEN=your_token_here
   ```

---
