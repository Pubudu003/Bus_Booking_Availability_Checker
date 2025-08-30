import smtplib
import ssl
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
FROM_LOCATION = "Wellawaya"
TO_LOCATION = "Makumbura"
SEARCH_DATE = "2025-09-08"
BUS_SCHEDULE_ID = "SLTTSEX198-1600-MC"
SEAT_CHECKING_ID = "870555"

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

# --- Find the available bus sheat count ---
def find_available_bus_seats():
    search_url = f"https://sltb.eseat.lk/seats/{SEAT_CHECKING_ID}"
    
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
        
        print("Waiting for seat information to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list-group li.list-group-item'))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        elements = soup.select('ul.list-group li.list-group-item')
        
        if elements:
            print(f"found {len(elements)} elements.")
            available_seat_index = -1
            for index, element in enumerate(elements):
                if element.get_text().strip() == "Available Seats":
                    available_seat_index = index + 1
                    break
            available_seats = elements[available_seat_index].get_text().strip()
            return available_seats
        else:
            print("No seat element found!")
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
    body = f"Bus booking is yet not avalable for, from {FROM_LOCATION} to {TO_LOCATION} on {SEARCH_DATE}.\n\n" \
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

# --- Send an email notification with available seat count ---
def send_available_seat_count_email(available_seat_count):
    subject = "Bus Booking Open and Seats Available!"
    body = f"Bus booking for the route from {FROM_LOCATION} to {TO_LOCATION} on {SEARCH_DATE} are now available on eseat.lk.\n\n" \
           f"https://sltb.eseat.lk/seats/{SEAT_CHECKING_ID}" \
           f"\n\nAvailable Seats: {available_seat_count}"
           
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
        print("Checking for bus seat availability...")
        seat_count = find_available_bus_seats()
        
        if seat_count:
            print(f"Available Seats: {seat_count}")
            send_available_seat_count_email(seat_count)
        else:
            print("No seat information found.")
            send_email_notification()
        
    else:
        print("Bus booking is not yet available.")
        send_booking_unavailable_email()
