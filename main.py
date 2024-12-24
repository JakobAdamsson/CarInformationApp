from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

DEBUG = 0
class VehicleDataService:
    def __init__(self):
        self.chrome_options = Options()
        if DEBUG == 1:
            self.driver_path = r"C:\Skola\CarInfoApp\backend\chromedriver\chromedriver.exe"
            self.chrome_binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            self.wait_const = 5
        else:
            self.driver_path = "/usr/bin/chromedriver"
            self.chrome_binary_path = "/usr/bin/chromium"
            self.wait_const = 5
            self.chrome_options.binary_location = self.chrome_binary_path  # Specify path to Chrome binary
            self.chrome_options.add_argument("--no-sandbox")  # Disables the sandboxing feature
            self.chrome_options.add_argument("--disable-dev-shm-usage")  # Resolves /dev/shm issues in Docker
            self.chrome_options.add_argument("--remote-debugging-port=9222")  # Opens a port for Chrome to communicate
            self.chrome_options.add_argument("--verbose")
            self.chrome_options.add_argument("--log-path=/tmp/chromedriver.log")  # Logs will be saved here





    def get_vehicle_data(self, registration_number, url):
        # Initialize the WebDriver using the Service class and Chrome options
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=self.chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(self.wait_const)
        wait = WebDriverWait(driver, self.wait_const)
        try:
            # Open Biltema's website
            driver.get(url)
            # Wait for the cookie consent popup and click on "Jag accepterar alla cookies"
            try:
                
                accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Jag accepterar alla cookies')]")))
                accept_button.click()
            except:
                pass  # No cookie consent found

            # Wait for the search bar input to be visible (replacing the previous search bar selector)
            search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'quicksearch__target')]//input[@type='search']")))
            # Click on the search bar first to activate it
            search_bar.click()

            # Now enter the registration number into the search bar
            search_bar.send_keys(registration_number)
            search_bar.send_keys(Keys.RETURN)

            # Wait for and click the "Mer om bilen" button (target the button more robustly)
            more_about_car_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mer om bilen']")))
            more_about_car_button.click()

            # Extract the "Fordonsinformation" section and the details
            vehicle_info_section = driver.find_element(By.XPATH, "//div[contains(@class, 'jk5tktBY45StAzlElGgVVw==')]")
            vehicle_info = vehicle_info_section.text
            return vehicle_info

        finally:
            # Close the browser
            driver.quit()

    def split_vehicle_data(self, vehicle_data):
        data_dict = {}
        for data in vehicle_data.split("\n"):
            tmp = data.split(":")
            # ooga booga but works :D
            try:
                if tmp[1]:
                    #print(tmp[1], "adadadadada")
                    data_dict[tmp[0]] = tmp[1]
            except:
                pass
        return data_dict


    def validate_reg_number(self, reg_number):
        reg_number = reg_number.replace(" ", "").upper()
        if len(reg_number) == 6:
            first_part = reg_number[:3]
            second_part = reg_number[3:]
            if first_part.isalnum() and second_part.isalnum():
                print("Valid registration number")
                return True
        print("Invalid registration number")
        return False



    def get_oil_capacity(self, registration_number, url):


        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=self.chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(self.wait_const)
        wait = WebDriverWait(driver, self.wait_const)
        motor = "D2"
        try:
            # Open the website
            driver.get(url)

            # Handle cookie popup
            try:
                accept_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ok, vi kör!')]"))
                )
                accept_button.click()
            except TimeoutException:
                print("Cookie popup not found.")

            # Wait for the search bar
            try:
                search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'carsearch-module-regnr-input')]")))
                search_bar.click()
                search_bar.send_keys(registration_number)

                # Check the number of car options
                try:
                    select_car_divs = driver.find_elements(By.XPATH, "//div[@class='plate-car-selection-box']//div[@class='select-car']")
                    
                    if len(select_car_divs) == 1:
                        # If there's only one option, click it and skip further selection
                        select_car_divs[0].click()
                        print("Only one car option found. Proceeding with the selection.")
                    elif len(select_car_divs) >= 2:
                        # Handle multiple car options
                        my_car = ""
                        for car_option in select_car_divs:
                            car_text = car_option.find_element(By.XPATH, ".//div").text
                            car_name = car_text.split(" <small")[0]
                            
                            if motor in car_name:
                                my_car = car_name
                                break

                        # Click the matched car option
                        if my_car:
                            for car_option in select_car_divs:
                                car_text = car_option.find_element(By.XPATH, ".//div").text
                                car_name = car_text.split(" <small")[0]
                                if car_name == my_car:
                                    car_option.click()
                                    print(f"Clicked on the car: {my_car}")
                                    break
                        else:
                            print("No matching car found.")
                    else:
                        print("No car options found. Proceeding without selection.")
                except TimeoutException:
                    print("Error while checking for car options.")
            except TimeoutException:
                print("Search bar or button not found.")
                return "Search failed."

            # Get oil capacity information
            try:
                oil_capacity_element = wait.until(
                    EC.presence_of_element_located((By.ID, "oil-capacity"))
                )
                oil_info = oil_capacity_element.text.split("\n")[1]
                return oil_info
            except TimeoutException:
                print("Vehicle information section not found.")
                return "Vehicle information not found."

        finally:
            driver.quit()

    
