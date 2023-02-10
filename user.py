from time import sleep

import utils

from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup


class TwitterUser:
    """
    Twitter user class
    """

    def __init__(self, driver, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.driver = driver

        self.is_logged_in = False

        self.current_url = ""

    def login(self):
        """
        Login to Twitter account with provided username and password
        :return:
        """
        self.driver.get("https://twitter.com/i/flow/login")

        sleep(5)

        # click text box then enter username
        username_field = self.driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        username_field.click()
        sleep(1)
        username_field.send_keys(self.username)
        sleep(1)
        username_field.send_keys(Keys.RETURN)

        sleep(5)

        # click text box then enter password
        password_field = self.driver.find_element(By.XPATH, "//input[@name='password']")
        password_field.click()
        sleep(1)
        password_field.send_keys(self.password)
        sleep(1)
        password_field.send_keys(Keys.RETURN)

        sleep(1)

        try:
            email_field = self.driver.find_element(By.XPATH, "//input[@autocomplete='email']")
            email_field.click()
            sleep(1)
            email_field.send_keys(self.email)
            sleep(1)
            email_field.send_keys(Keys.RETURN)

        except exceptions.NoSuchElementException:
            pass

        sleep(3)

        self.is_logged_in = True

    def logout(self):
        """
        logout of account
        :return:
        """
        if not self.is_logged_in:
            return

        self.driver.get("https://twitter.com/home")

        sleep(5)

        self.driver.find_element(By.XPATH, "//div[@data-testid='SideNav_AccountSwitcher_Button']").click()
        sleep(2)
        self.driver.find_element(By.XPATH, "//a[@data-testid='AccountSwitcher_Logout_Button']").click()
        sleep(2)
        self.driver.find_element(By.XPATH, "//div[@data-testid='confirmationSheetConfirm']").click()
        sleep(2)

        self.is_logged_in = False

    def get_list_of_followers(self, account):
        """
        get the list of followers from starting account
        :return:
        """
        # TODO: Yay! It works
        #       Just need to save the usernames to a file

        user_list = set()

        # open followers page of starting_account
        self.driver.get(f"https://twitter.com/{account}/followers")

        sleep(5)

        # TODO: find a better way to specify the number used in range()
        # while len(user_list) < 100:
        for i in range(2):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                html = self.driver.page_source
                parsed_html = BeautifulSoup(html, features="lxml")

                element_class = "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"
                user_links = parsed_html.find_all('a', class_=element_class, href=True)

                sleep(2)

                for link in user_links:
                    username = link.get("href")
                    # print(username.strip("/"))
                    user_list.add(username.strip("/"))

                i += 1
            except Exception as e:
                print(e)
                return 0

        # utils.save_to_file(user_list, "usernames")
        return user_list

    def send_message(self, user, message):
        """
        Send a DM with the message :param message: to :param user:

        :param user:
        :param message:
        :return:
        """
        url = "https://twitter.com/messages"

        # open twitter messages page
        if self.current_url == "":
            # helps when sending new messages
            self.driver.get(url)
            self.current_url = url

        sleep(2)

        # TODO: Something is wrong here. Figure it out and fix it
        #       Has something to do with the check for users with locked DMs
        #       Code assumes user's DM is locked when it really is open
        #       WHY???!!! I think it's fixed
        try:
            # click new message icon
            new_message_icon = self.driver.find_element(By.XPATH, "//a[@data-testid='NewDM_Button']")
            new_message_icon.click()
            sleep(2)

            try:
                # check for pop up
                pop_up = self.driver.find_element(By.CLASS_NAME, "css-1dbjc4n r-1ffj0ar r-1p0dtai r-1d2f490 r-1xcajam "
                                                                 "r-zchlnj r-ipm5af")
                sleep(1)
                pop_up.send_keys(Keys.RETURN)

            except exceptions.NoSuchElementException:
                print("No pop_ups")

            # enter username in search field
            search_field = self.driver.find_element(By.XPATH, "//input[@data-testid='searchPeople']")
            search_field.click()
            sleep(1)
            search_field.send_keys(f"{user}")
            sleep(1)

            # click the first account in the list of search results
            first_account = self.driver.find_element(By.XPATH, "//div[@data-testid='typeaheadResult']")
            sleep(1)

            try:
                # TODO: Error occurs here... I think
                # check if account is selectable
                first_account.find_element(By.XPATH, "//div[@aria-diabled='true']")
                #  User's DM is locked, do nothing

                # close search dialog
                close_button = self.driver.find_element(By.XPATH, "//div[@data=testid='app-bar-close']")
                close_button.click()

                return 0

            except exceptions.NoSuchElementException:
                # click first account
                first_account.click()
                sleep(1)

                # click next button
                next_button = self.driver.find_element(By.XPATH, "//div[@data-testid='nextButton']")
                next_button.click()
                sleep(2)

                # send message to user
                message_input_field = self.driver.find_element(By.XPATH, "//div[@data-testid='dmComposerTextInput']")
                message_input_field.click()
                sleep(1)
                message_input_field.send_keys(message)
                sleep(1)
                message_input_field.send_keys(Keys.RETURN)

                # look for pop-up
                try:
                    sleep(2)
                    pop_up = self.driver.find_element(By.CLASS_NAME, "css-18t94o4 css-1dbjc4n r-42olwf r-sdzlij "
                                                                     "r-1phboty r-rs99b7 r-1mnahxq r-19yznuf r-64el8z"
                                                                     " r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr")
                    pop_up.send_keys(Keys.RETURN)
                    # resend message
                    message_input_field = self.driver.find_element(By.XPATH,
                                                                   "//div[@data-testid='dmComposerTextInput']")
                    message_input_field.click()
                    sleep(1)
                    message_input_field.send_keys(message)
                    sleep(1)
                    message_input_field.send_keys(Keys.RETURN)

                except exceptions.NoSuchElementException:
                    return 1

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

            return 1

        except Exception as e:
            print(f"The following error was encountered: {e}")
            return 0
