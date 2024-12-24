from playwright.sync_api import sync_playwright
import time
import os

DEBUG = 0

class VehicleDataService:
    def get_vehicle_data(self, registration_number: str, url: str):
        """
        This monster is written mostly by chatgpt, do not ask me what is going on:)
        """
        with sync_playwright() as p:
            if DEBUG == 1:
                browser = p.chromium.launch(headless=False)  # Debug mode with visible browser
            else:
                browser = p.chromium.launch(
                    headless=True, 
                    args=["--disable-web-security", "--disable-features=IsolateOrigins,site-per-process"]
                )

            # Always use a context to set User-Agent and other parameters
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                viewport={"width": 1366, "height": 768},  # Simulate a smaller screen size
                java_script_enabled=True  # Ensure JavaScript is enabled
            )

            page = context.new_page()
            #page.set_default_timeout(30000)  # Set timeout to 30 seconds

            try:
                # Open the website
                page.goto(url)

                # Wait for and handle cookie consent popup
                try:
                    accept_button = page.locator("button:has-text('Jag accepterar alla cookies')")
                    accept_button.click()
                except Exception as e:
                    print(f"No cookie consent button found: {e}")

                # Locate the search bar and fill in the registration number
                search_bar = page.locator("input[type='search']").nth(0)
                search_bar.wait_for(state="visible")
                search_bar.scroll_into_view_if_needed()

                search_bar.fill(registration_number)
                #page.wait_for_timeout(1000) 

                search_bar.focus()


                #page.wait_for_timeout(500)

                search_bar.press('Enter')

                mer_om_bilen_button = page.locator("button[aria-label='Mer om bilen']")
                mer_om_bilen_button.click()

                page.wait_for_selector("div:has-text('Fordonsinformation') + ul")  # Wait for the <ul> list inside Fordonsinformation


                fordonsinformation = page.locator("div:has-text('Fordonsinformation') + ul")
                fordonsinformation_data = fordonsinformation.all_text_contents() 

                vehicle_info = {}
                for index in range(fordonsinformation.locator("li").count()):  
                    item = fordonsinformation.locator("li").nth(index)
                    label = item.locator("label").nth(0).text_content()  
                    value = item.locator("label").nth(1).text_content()
                    vehicle_info[label] = value

                                
                return vehicle_info

            except Exception as e:
                print(f"Error occurred: {e}")
                return str(e)

            finally:
                browser.close()

    def validate_reg_number(self, reg_number):
        reg_number = reg_number.replace(" ", "").upper()
        if len(reg_number) == 6:
            first_part = reg_number[:3]
            second_part = reg_number[3:]
            if first_part.isalnum() and second_part.isalnum():
                return True
        return False


    def get_oil_capacity(self, registration_number: str, url: str, engine_type: str):
        with sync_playwright() as p:
            if DEBUG == 1:
                browser = p.chromium.launch(headless=False)
            else:
                browser = p.chromium.launch(headless=True)

            page = browser.new_page()
            motor = engine_type 

            try:
                # Open the website
                page.goto(url)

                # Handle cookie popup
                try:
                    accept_button = page.locator("button:has-text('Ok, vi kör!')")
                    accept_button.click()
                except:
                    print("Cookie popup not found.")

                # Wait for the search bar
                search_bar = page.locator("input[id*='carsearch-module-regnr-input']")
                search_bar.click()
                search_bar.fill(registration_number)

                # Wait for the car selection dropdown to appear (if there are multiple options)
                try:
                    # Attempt to find the car options
                    page.wait_for_selector("div.plate-car-selection-box div.select-car", timeout=5000)
                    # Get the list of car options
                    select_car_divs = page.locator("div.plate-car-selection-box div.select-car")
                    car_count = select_car_divs.count()

                    if car_count == 1:
                        # If there's only one option, click it and continue
                        select_car_divs.nth(0).click()
                    elif car_count > 1:
                        # Handle multiple car options
                        my_car = ""
                        for i in range(car_count):
                            car_text = select_car_divs.nth(i).inner_text()
                            # Look for the motor keyword (e.g., "D2") in the car text
                            if motor in car_text:
                                my_car = car_text
                                select_car_divs.nth(i).click()  # Click the car option that matches the keyword
                                print(f"Clicked on the car: {my_car}")
                                break
                except:
                    # If the dropdown is not found, assume that there is only one car and continue
                    print("No car options found. Proceeding without selection.")

                # Get oil capacity information
                oil_capacity_element = page.locator("#oil-capacity")
                oil_info = oil_capacity_element.inner_text().split("\n")[1]
                return oil_info

            finally:
                browser.close()


