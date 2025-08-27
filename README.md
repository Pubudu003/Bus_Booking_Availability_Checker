# 🚌 1315.lk Bus Seat Booking Availability Automation

This project automates the process of checking bus seat booking availability on [1315.lk / eseat.lk](https://sltb.eseat.lk) for a given route and date.  
If the selected bus schedule is available, it sends an **email notification**. If not available, it also notifies you.

This project is a small system I built myself to make things easier. Building it paved the way for me to learn automation, GitHub Actions, Selenium, and more.

## 🔑 Features
- Automates seat availability checking for a specific route/date.
- Uses **Selenium** with Chrome (headless mode) to load the booking page.
- Sends email alerts hourly via **Gmail SMTP** when:
  - ✅ Seats are available.
  - ❌ Seats are not yet available.
- Customizable route, date, and bus schedule ID.

## 🛠 Tech Stack
- **Python 3**
- **Selenium** + `webdriver-manager` (for Chrome automation)
- **smtplib** + **SSL** (for email notifications)
- **Gmail SMTP server**

## ⚙️ Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/1315lk-bus-seat-automation.git
cd 1315lk-bus-seat-automation```
