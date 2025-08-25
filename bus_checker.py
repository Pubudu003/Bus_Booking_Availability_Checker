import smtplib
import ssl
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
FROM_LOCATION = "Makumbura"
TO_LOCATION = "Wellawaya"
SEARCH_DATE = "2025-09-04"
BUS_SCHEDULE_ID = "SLTTSEX01-2100-CA"

SENDER_EMAIL = "pubuduakshan04@gmail.com"
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = "pubuduakshan04@gmail.com"

# --- Check bus availability ---
def check_bus_availability():
    search_url = f"https://sltb.eseat.lk/search?type=1&from={FROM_LOCATION}&to={TO_LOCATION}&from_date={SEARCH_DATE}&to_date="

    # Use the webdriver-manager to automatically handle the driver installation
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("Opening browser to check bus availability...")
        driver.get(search_url)
        
        time.sleep(10)
        
        if BUS_SCHEDULE_ID in driver.page_source:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error accessing the website: {e}")
        return False
    finally:
        if driver:
            driver.quit()
    
# --- Send an email notification ---
def send_email_notification():
    subject = "Bus Booking Open!"
    body = f"Bus booking for the route from {FROM_LOCATION} to {TO_LOCATION} on {SEARCH_DATE} are now available on eseat.lk.\n\n" \
           f"You can book now at https://sltb.eseat.lk/search?type=1&from={FROM_LOCATION}&to={TO_LOCATION}&from_date={SEARCH_DATE}&to_date=" 
           
    message = f"Subject: {subject}\n\n{body}"
    
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- Send an unavailability email
def send_booking_unavailable_email():
    subject = "Bus Booking not available yet!"
    body = f"Bus booking is yet not avalable for, from {FROM_LOCATION} to {TO_LOCATION} on {SEARCH_DATE}.\n\n"
            f"You can check at https://sltb.eseat.lk/search?type=1&from={FROM_LOCATION}&to={TO_LOCATION}&from_date={SEARCH_DATE}&to_date="

    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- Main program ---
if __name__ == "__main__":
    print("Checking for bus availability...")
    if check_bus_availability():
        print("Bus booking is now available!")
        send_email_notification()
    else:
        print("Bus booking is not yet available.")
        send_booking_unavailable_email()
