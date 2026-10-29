# 🎓 NULP ScheduleBot

<p align="center">
  <a href="README.md">🇺🇦 Українська</a> •
  <a href="README.en.md">🇬🇧 English</a>
</p>

[![Python Version](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![BeautifulSoup](https://img.shields.io/badge/Parser-BeautifulSoup4-3F51B5?style=flat)](https://www.crummy.com/software/BeautifulSoup/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

**NULP ScheduleBot** is a feature-rich Telegram bot tailored for students of **Lviv Polytechnic National University (NULP)**. The bot provides real-time access to the academic schedule parsed directly from the university's official scheduling portal, interactive inline filtering (by day, subgroup, and numerator/denominator weeks), campus building navigation via Google Maps, and daily weather forecasts for Lviv.

---

## ✨ Features

- 📅 **Live Academic Schedule**:
  - Real-time scraping from the university's official portal [`student.lpnu.ua`](https://student.lpnu.ua/students_schedule).
  - Search by any student academic group (e.g., `ІК-41`, `ПЗ-21`, etc.).
  - Intuitive inline keyboard controls:
    - 🔘 Day selector (Mon–Fri).
    - 👥 Subgroup filter (**Subgroup 1** / **Subgroup 2**).
    - 🔢 Week type filter (**Numerator** / **Denominator**).
    - 🕐 Accurate lesson periods (1st through 8th class) with emoji numbering.

- 📍 **Campus Buildings Navigation**:
  - **Automatic Geo-tags**: The bot identifies campus building numbers in the class description (including Roman numeral notations like `XXVII н.к.`) and attaches clickable 📍 Google Maps links with precise GPS coordinates.
  - **Building Search**: Send `/map` or tap `Карта📍` to enter any building number (e.g., `0` for Main Building, `1`, `4`, `28`, etc.) to receive its street address and a pinned Telegram Location.

- ⛅️ **Weather Forecast in Lviv**:
  - Command `/weather` or button `Погода⛅️`.
  - Powered by **OpenWeatherMap API**: minimum/maximum temperature, precipitation, humidity, and forecast description for today and tomorrow.
  - Automatic translation of weather condition descriptions to Ukrainian.

---

## 📸 Screenshots & Demo

| Main Keyboard Menu | Fetching Schedule | Schedule Filters & Settings |
| :---: | :---: | :---: |
| <img src="demo-screenshots/keyboard-menu.jpg" width="280" alt="Main Keyboard Menu" /> | <img src="demo-screenshots/start-dialog.jpg" width="280" alt="Fetching Schedule" /> | <img src="demo-screenshots/schedule-filters.jpg" width="280" alt="Schedule Filters" /> |

| Direct Google Maps Link | Building Location by Number | Lviv Weather Forecast |
| :---: | :---: | :---: |
| <img src="demo-screenshots/readdress-link-on-googlemaps.jpg" width="280" alt="Google Maps Link" /> | <img src="demo-screenshots/find-academic-building-location.jpg" width="280" alt="Building Location" /> | <img src="demo-screenshots/weather-forecast-dialog.jpg" width="280" alt="Weather Forecast" /> |

---

## 📁 Repository Structure

```text
ScheduleBot/
├── demo-screenshots/              # Bot UI demo screenshots
├── project/
│   ├── convert_roman_numerals.py  # Detects and converts Roman numerals for campus building numbers
│   ├── corps_dataset.py           # Dataset of GPS coordinates and street addresses for NULP buildings
│   ├── forecast.py                # OpenWeatherMap API integration and forecast formatting
│   ├── schedule_handler.py        # Web scraper for student.lpnu.ua and schedule builder
│   └── telegram_bot.py            # Main Telegram bot handlers, conversational state, and inline UI
├── .env.example                   # Template for environment variables
├── .gitignore                     # Git ignore rules for virtual environments, secrets, and temp files
├── Dockerfile                     # Docker container definition
├── docker-compose.yml             # Docker Compose orchestration configuration
├── main.py                        # Application entry point
├── README.md                      # Documentation in Ukrainian
├── README.en.md                   # Documentation in English
└── requirements.txt               # Python package dependencies
```

---

## 🛠 Tech Stack

- **Language**: Python 3.12+
- **Telegram Framework**: [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) (`v13.15`)
- **Web Scraping**: [`BeautifulSoup4`](https://www.crummy.com/software/BeautifulSoup/) + [`requests`](https://requests.readthedocs.io/)
- **Weather Service**: [OpenWeatherMap API](https://openweathermap.org/api)
- **Translation**: [`googletrans`](https://py-googletrans.readthedocs.io/)
- **Configuration**: [`python-dotenv`](https://github.com/theskumar/python-dotenv)
- **Containerization**: Docker & Docker Compose

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sasha-1337/NULP-ScheduleBot.git
cd NULP-ScheduleBot
```

### 2. Configure Environment Variables

Create your local `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Open `.env` in an editor and supply your credentials:

```env
# Bot token from @BotFather in Telegram
TELEGRAM_TOKEN=your_telegram_bot_token_here

# OpenWeatherMap API key (free at https://openweathermap.org/api)
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here

# Weather forecast city (default: Lviv)
CITY=Lviv
```

---

### Option A: Local Python Environment

1. **Create and activate a virtual environment**:
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the bot**:
   ```bash
   python main.py
   ```

---

### Option B: Docker Deployment

1. **Build and start the container**:
   ```bash
   docker build -t nulp-schedulebot .
   docker run -d --name schedulebot --env-file .env nulp-schedulebot
   ```

2. **Or run with Docker Compose**:
   ```bash
   docker-compose up -d --build
   ```

---

## 🤖 Commands & Usage

| Command / Button | Description |
| :--- | :--- |
| `/start` or `Розклад занять🗓` | Start conversation, input group name, and fetch class schedule |
| `/map` or `Карта📍` | Search building address and receive a GPS map pin (e.g. `0` for main building, `1`, `4`) |
| `/weather` or `Погода⛅️` | Display weather forecast for today and tomorrow |
| `/cancel` | Cancel current conversation state |

### Interactive Schedule Menu
- **Weekday Buttons (`Пн`, `Вт`, `Ср`, `Чт`, `Пт`)**: Instant tab switching between Monday through Friday.
- **⚙️ Settings (`⚙️Налаштування`)**:
  - `1 група` / `2 група` — Toggle student subgroup.
  - `чисельник` / `знаменник` — Toggle numerator/denominator week.
  - `❗️Видалити розклад❗️` — Reset stored schedule parameters.
  - `Повернутись назад↩️` — Return to timetable view.

---

## 🔒 Security Notice

> [!WARNING]
> Never commit your `.env` file containing actual tokens (`TELEGRAM_TOKEN`, `OPENWEATHERMAP_API_KEY`) to version control. Always verify that `.env` is listed in `.gitignore`.

---

## 👨‍💻 Author

Created for students of Lviv Polytechnic National University: [@sasha-1337](https://github.com/sasha-1337).
