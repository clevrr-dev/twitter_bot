import time

from selenium import webdriver
from selenium.common import exceptions
# from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_options=chrome_options)

# driver.maximize_window()
driver.implicitly_wait(10)


class TwitterUser:
    """
    Twitter user class
    """

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.driver = driver
        self.is_logged_in = False

    def login(self):
        """
        Login to Twitter account with provided username and password
        :return:
        """
        self.driver.get("https://twitter.com/i/flow/login")

        time.sleep(5)

        # click text box then enter username
        username_field = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        username_field.click()
        time.sleep(1)
        username_field.send_keys(self.username)
        time.sleep(1)
        username_field.send_keys(Keys.RETURN)

        time.sleep(3)

        # click text box then enter password
        password_field = driver.find_element(By.XPATH, "//input[@name='password']")
        password_field.click()
        time.sleep(1)
        password_field.send_keys(self.password)
        time.sleep(1)
        password_field.send_keys(Keys.RETURN)

        time.sleep(3)

        try:
            email_field = driver.find_element(By.XPATH, "//input[@autocomplete='email']")
            email_field.click()
            time.sleep(1)
            email_field.send_keys(self.email)
            time.sleep(1)
            email_field.send_keys(Keys.RETURN)

        except Exception as e:
            print(e)

        time.sleep(5)

        self.is_logged_in = True

    def logout(self):
        """
        logout of account
        :return:
        """
        if not self.is_logged_in:
            return

        self.driver.get("https://twitter.com/home")

        time.sleep(5)

        self.driver.find_element(By.XPATH, "//div[@data-testid='SideNav_AccountSwitcher_Button']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//a[@data-testid='AccountSwitcher_Logout_Button']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@data-testid='confirmationSheetConfirm']").click()
        time.sleep(2)

        self.is_logged_in = False

    def get_followers(self):
        """
        get the list of followers
        :return:
        """
        # TODO: This method isn't working.... Yet
        #       You'll figure it out. I believe in you ;)
        users = []
        i = 0
        # put the link of profile here
        self.driver.get(f"https://twitter.com/{self.username}/followers")

        while True:
            time.sleep(3)
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                html = self.driver.page_source
                soup = BeautifulSoup(html)
                element_class = "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"
                followers = soup.find_all('span', class_=element_class)
                time.sleep(3)

                for follower in followers:
                    print(follower.text)
                    # users.append(follower.text)

                i += 1
            except:
                continue

    def send_message(self, user, message):
        """
        Send a DM with the message :param message: to :param user:

        :param user:
        :param message:
        :return:
        """
        # open twitter messages page
        self.driver.get("https://twitter.com/messages")
        time.sleep(1)

        # TODO: Something is wrong here. Figure it out and fix it
        #       Has something to do with the check for users with locked DMs
        #       Code assumes user's DM is locked when it really is open
        #       WHY???!!!
        try:
            # click new message icon
            new_message_icon = self.driver.find_element(By.XPATH, "//a[@data-testid='NewDM_Button']")
            new_message_icon.click()
            time.sleep(2)

            # enter username in search field
            search = self.driver.find_element(By.XPATH, "//input[@data-testid='searchPeople']")
            search.click()
            search.send_keys(f"{user}")
            time.sleep(1)

            # click the first account in the list of search results
            first_account = self.driver.find_element(By.XPATH, "//div[@data-testid='typeaheadResult']")
            first_account.click()
            time.sleep(1)

            try:
                # TODO: Error occurs here... I think
                # check if account is selectable
                self.driver.find_element(By.XPATH, "//div[@aria-disabled='true']")

                # # User's DM is locked, do nothing
                print(f"{user}'s DM is locked.")
                print("Moving to the next user")

                return 0, user

            except exceptions.NoSuchElementException:
                # click next button
                next_button = self.driver.find_element(By.XPATH, "//div[@data-testid='nextButton']")
                next_button.click()
                time.sleep(2)

            # Try again if there's a pop-up
            except exceptions.ElementClickInterceptedException:
                print("Pop-up detected")
                # Send RETURN key to remove pop_up
                pop_up = self.driver.find_element(By.CLASS_NAME, "css-18t94o4 css-1dbjc4n r-1niwhzg r-1ets6dv r-sdzlij "
                                                                 "r-1phboty r-rs99b7 r-1wzrnnt r-peo1c r-1ps3wis "
                                                                 "r-1ny4l3l r-1guathk r-o7ynqc r-6416eg r-lrvibr")
                pop_up.send_keys(Keys.RETURN)
                # Try again
                self.send_message(user, message)

            # send message to user
            message_input_field = self.driver.find_element(By.XPATH, "//div[@data-testid='dmComposerTextInput']")
            message_input_field.click()
            time.sleep(1)
            message_input_field.send_keys(message)
            time.sleep(1)
            message_input_field.send_keys(Keys.RETURN)

        except Exception as e:
            print(f"The following error was encountered: {e}")
            return 0
