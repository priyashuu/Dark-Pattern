from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
detect_success = False

def detect_false_urgency(url):
    # Set up the web driver (make sure to download the appropriate driver for your browser)
    driver = webdriver.Chrome()

    try:
        # Open the website
        driver.get(url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Track the count of pop-ups, alerts, and loud sounds
        pop_up_count = 0
        alert_count = 0
        loud_sound_count = 0

        # Monitor for a certain period of time (adjust as needed)
        monitoring_duration = 30  # seconds
        start_time = time.time()

        while time.time() - start_time < monitoring_duration:
            # Check for pop-ups
            pop_up_count += len(driver.window_handles) - 1

            # Check for alerts
            try:
                alert = driver.switch_to.alert
                alert_count += 1
                alert.accept()
            except:
                pass

            # Check for loud sounds (you may need to adjust this based on specific scenarios)
            # loud_sound_count += check_for_loud_sounds(driver)

            # Wait for a short interval before checking again
            time.sleep(1)

        # Analyze the results and determine false urgency
        if pop_up_count > 5 or alert_count > 5 or loud_sound_count > 5:
            result = "False Urgency Detected!"
            detect_success = True
        else:
            result = "No False Urgency Detected."

    finally:
        # Close the browser window
        driver.quit()

    return result, detect_success


def analyze_text(text):
    shaming_keywords = ['shame', 'guilt', 'blame', 'condemn', 'criticize']  # Add more keywords as needed

    # Tokenize the text into words
    words = word_tokenize(text)

    # Check if any shaming keywords are present in the text
    shaming_occurrences = [word for word in words if word.lower() in shaming_keywords]

    return shaming_occurrences


def scan_website_for_shaming(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content from the HTML
            text_content = soup.get_text()

            # Analyze the text for shaming keywords
            shaming_occurrences = analyze_text(text_content)

            if shaming_occurrences:
                detect_success = True
                print("Potential shaming content detected on the website.")
                print("Shaming keywords found:", shaming_occurrences)
            else:
                print("No shaming content detected on the website.")
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return detect_success


class CartMonitor:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def start_monitoring(self, monitoring_duration=30):
        try:
            # Open the website
            self.driver.get(self.url)

            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Get initial cart content
            initial_cart_content = self.get_cart_content()

            # Monitor for changes in the cart
            start_time = time.time()

            while time.time() - start_time < monitoring_duration:
                # Check if cart content has changed
                current_cart_content = self.get_cart_content()

                if current_cart_content != initial_cart_content:
                    print("Items added to the cart without user interaction!")

                # Wait for a short interval before checking again
                time.sleep(1)

        finally:
            # Close the browser window
            self.driver.quit()

    def get_cart_content(self):
        # This function retrieves the current content of the shopping cart
        # Implement this function based on the structure of the website's cart
        # For demonstration purposes, it returns a placeholder value
        # You need to modify it based on the actual structure of the website's cart

        # Example: Assume the cart items are stored in a div with class "cart-item"
        try:
            cart_items = self.driver.find_elements(By.CLASS_NAME, 'cart-item')
            cart_content = [item.text for item in cart_items]
            return cart_content
        except:
            return []


class ForcedActionDetector:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def detect_forced_action(self):
        try:
            # Open the website
            self.driver.get(self.url)

            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Check if going back is discouraged
            self.detect_discouraged_back()

            # Check if proceeding further is blocked
            self.detect_blocked_proceed()

        finally:
            # Close the browser window
            self.driver.quit()

    def detect_discouraged_back(self):
        # Attempt to go back
        self.driver.back()

        # Check if there is a prompt or the same page is loaded again
        current_url = self.driver.current_url

        # Check if the current URL is still the same
        if current_url == self.url:
            print("Forced action detected: Discouraging users from going back. (Prompt or same page)")

        # Check if there is a prompt indicating that going back is not allowed
        try:
            prompt_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'cannot go back')]")
            if prompt_element.is_displayed():
                print("Forced action detected: A prompt discouraging users from going back is displayed.")
        except:
            pass  # No prompt element found

    def detect_blocked_proceed(self):
        # Perform an action to proceed further (e.g., clicking a button)
        # You need to customize this based on the actual website behavior
        # Here, we click an element with ID 'proceed-btn' as an example
        proceed_button = self.driver.find_element(By.ID, 'proceed-btn')
        proceed_button.click()

        # Check if the current URL indicates a subscription or sign-in requirement
        current_url = self.driver.current_url
        blocked_keywords = ['subscribe', 'sign-in', 'login', 'buy']

        if any(keyword in current_url.lower() for keyword in blocked_keywords):
            print("Forced action detected: Blocked from proceeding further, subscription or sign-in required.")
            detect_success = True
            
        else:
            print("No forced action detected: Proceeding further is allowed.")
        
        return detect_success


class SubscriptionTrapDetector:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def detect_subscription_trap(self):
        try:
            # Open the website
            self.driver.get(self.url)

            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Check if proceeding further is blocked
            if self.is_subscription_trap_present():
                print("Subscription trap detected: Proceeding further requires a subscription.")
                detect_success = True
                
            else:
                print("No subscription trap detected: Proceeding further is allowed.")

        finally:
            # Close the browser window
            self.driver.quit()

        return detect_success

    def is_subscription_trap_present(self):
        # Perform actions to proceed further (e.g., clicking a button)
        # Customize this based on the actual website behavior
        # Here, we look for an element with ID 'proceed-btn' as an example
        proceed_button = self.driver.find_element(By.ID, 'proceed-btn')
        proceed_button.click()

        # Check if the current URL or page content indicates a subscription requirement
        current_url = self.driver.current_url
        blocked_keywords = ['subscribe', 'sign-in', 'login', 'buy']

        return any(keyword in current_url.lower() for keyword in blocked_keywords)


def detect_bait_and_switch_with_delivery(url):
    try:
        # Set up the Selenium WebDriver (ensure you have the appropriate driver installed)
        driver = webdriver.Chrome()  # Change to the appropriate driver for your browser

        # Open the website
        driver.get(url)

        # Extract initial price information
        initial_price_element = driver.find_element(By.CLASS_NAME, 'product-price')
        initial_price = float(initial_price_element.text.strip().replace('Rs', '').replace(',', ''))

        # Extract initial delivery charge information
        initial_delivery_charge_element = driver.find_element(By.CLASS_NAME, 'delivery-charge')
        initial_delivery_charge = float(initial_delivery_charge_element.text.strip().replace('Rs', '').replace(',', ''))

        # Calculate the total initial cost
        total_initial_cost = initial_price + initial_delivery_charge

        # Proceed to checkout or the next step
        checkout_button = driver.find_element(By.ID, 'checkout-button')
        checkout_button.click()

        # Wait for the next page to load (adjust the timeout as needed)
        WebDriverWait(driver, 10).until(EC.url_changes(url))

        # Extract updated price information
        updated_price_element = driver.find_element(By.CLASS_NAME, 'updated-price')
        updated_price = float(updated_price_element.text.strip().replace('Rs', '').replace(',', ''))

        # Extract updated delivery charge information
        updated_delivery_charge_element = driver.find_element(By.CLASS_NAME, 'updated-delivery-charge')
        updated_delivery_charge = float(updated_delivery_charge_element.text.strip().replace('Rs', '').replace(',', ''))

        # Calculate the total updated cost
        total_updated_cost = updated_price + updated_delivery_charge

        # Set the delivery charge threshold as a percentage of the product price
        delivery_charge_threshold_percentage = 12  # Adjust as needed

        # Check for insane delivery charges
        if (
            (updated_delivery_charge > delivery_charge_threshold_percentage / 100 * updated_price)
        ):
            print("Potential bait-and-switch with insane delivery charges detected!")
            detect_success = True
            print(f"Initial Total Cost: Rs {total_initial_cost}")
            print(f"Updated Total Cost: Rs {total_updated_cost}")
        else:
            print("No bait-and-switch detected with insane delivery charges.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser window
        driver.quit()

    return detect_success


def detect_price_changes(url):
    try:
        # Set up the Selenium WebDriver (ensure you have the appropriate driver installed)
        driver = webdriver.Chrome()  # Change to the appropriate driver for your browser

        # Open the website
        driver.get(url)

        # Extract initial product cost
        initial_price_element = driver.find_element(By.CLASS_NAME, 'initial-price')
        initial_price = float(initial_price_element.text.strip().replace('Rs', '').replace(',', ''))

        # Extract initial charges
        initial_charges_element = driver.find_element(By.CLASS_NAME, 'initial-charges')
        initial_charges = float(initial_charges_element.text.strip().replace('Rs', '').replace(',', ''))

        # Calculate the total initial cost
        total_initial_cost = initial_price + initial_charges

        # Proceed to the buying stage
        buy_button = driver.find_element(By.ID, 'buy-button')
        buy_button.click()

        # Wait for the next page to load (adjust the timeout as needed)
        WebDriverWait(driver, 10).until(EC.url_changes(url))

        # Extract final product cost
        final_price_element = driver.find_element(By.CLASS_NAME, 'final-price')
        final_price = float(final_price_element.text.strip().replace('Rs', '').replace(',', ''))

        # Extract final charges
        final_charges_element = driver.find_element(By.CLASS_NAME, 'final-charges')
        final_charges = float(final_charges_element.text.strip().replace('Rs', '').replace(',', ''))

        # Calculate the total final cost
        total_final_cost = final_price + final_charges

        # Set the percentage thresholds
        percentage_threshold_normal = 0.15  # 15%
        percentage_threshold_high = 0.10  # 10% for products over 10,000 Rs

        # Check for price changes
        if (
            (total_final_cost > (1 + percentage_threshold_normal) * total_initial_cost) or
            (initial_price > 10000 and total_final_cost > (1 + percentage_threshold_high) * total_initial_cost)
        ):
            print("Potential price change detected!")
            detect_success = True
            print(f"Initial Total Cost: Rs {total_initial_cost}")
            print(f"Final Total Cost: Rs {total_final_cost}")
        else:
            print("No significant price change detected.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser window
        driver.quit()

    return detect_success


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        url_to_check = request.form['domain']
        result = detect_false_urgency(url_to_check)

        cart_monitor = CartMonitor(url_to_check)
        cart_monitor.start_monitoring()

        scan_website_for_shaming(url_to_check)

        forced_action_detector = ForcedActionDetector(url_to_check)
        forced_action_detector.detect_forced_action()

        subscription_trap_detector = SubscriptionTrapDetector(url_to_check)
        subscription_trap_detector.detect_subscription_trap()

        detect_bait_and_switch_with_delivery(url_to_check)

        detect_price_changes(url_to_check)

    return render_template('../popup/popup.html', result=result)

def detect_dark_pattern():
    try:
        data = request.get_json()
        content = data.get('content', '')

        is_dark_pattern = detect_success

        return jsonify({'isDarkPattern': is_dark_pattern})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
