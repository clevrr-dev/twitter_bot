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

        sleep(3)

        # click text box then enter username
        username_field = self.driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        username_field.click()
        sleep(1)
        username_field.send_keys(self.username)
        sleep(1)
        username_field.send_keys(Keys.RETURN)

        sleep(3)

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
        self.driver.get("https://twitter.com/home")

        if not self.is_logged_in:
            return 0

        sleep(3)

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
        user_list = set()

        # open followers page of starting_account
        self.driver.get(f"https://twitter.com/{account}/followers")

        sleep(5)

        # scroll 20x
        for i in range(25):
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

        return user_list

    def send_message(self, user, message):
        """
        Send a DM with the message :param message: to :param user:

        :param user:
        :param message:
        :return:
        """
        url = "https://twitter.com/messages/compose"

        self.driver.get(url)

        def close_dialog():
            # locate and close pop up
            button = self.driver.find_element(By.XPATH, "//div[@data-testid='app-bar-close']")
            button.click()
            sleep(3)

        def enter_message():
            # type and send message
            message_input_field = self.driver.find_element(By.XPATH, "//div[@data-testid='dmComposerTextInput']")
            message_input_field.click()
            sleep(1)
            message_input_field.send_keys(message)
            message_input_field.send_keys(Keys.RETURN)
            sleep(1)

        sleep(2)

        # enter username in search field
        search_field = self.driver.find_element(By.XPATH, "//input[@data-testid='searchPeople']")
        search_field.click()
        sleep(1)
        search_field.send_keys(f"{user}")
        sleep(1)

        try:
            # select the first account in the list of search results if available
            first_account = self.driver.find_element(By.XPATH, "//div[@data-testid='typeaheadResult']")
            sleep(1)
            first_account.click()

            try:
                # check if account is selectable
                print("checking account...")
                self.driver.find_element(By.XPATH, "//div[@data-testid='typeaheadResult']")
                #  User's DM is locked, do nothing
                return 0

            except exceptions.NoSuchElementException:
                # click first account
                print("account found...")
                sleep(1)

                # click next button
                next_button = self.driver.find_element(By.XPATH, "//div[@data-testid='nextButton']")
                next_button.click()
                sleep(2)

                try:
                    enter_message()

                    try:
                        # locate and close pop up
                        close_dialog()
                        enter_message()

                    except exceptions.NoSuchElementException:
                        enter_message()

                except exceptions.ElementClickInterceptedException:

                    try:
                        # locate and close pop up
                        close_dialog()
                        enter_message()

                    except exceptions.NoSuchElementException:
                        enter_message()

        except exceptions.NoSuchElementException:
            return 2

        return 1


if __name__ == "__main__":
    # testing section
    import utils
    import random
    from time import sleep
    from selenium import webdriver

    # initialise webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    # get user credentials
    credentials = utils.read_csv_file('accounts')
    random.shuffle(credentials)
    name, password, email = credentials[1]

    # initialise user and login
    user = TwitterUser(driver, name, password, email)
    user.login()

    sleep(3)

    # get followers
    start_account = utils.read_file("starting_account.txt")[0]
    targets = user.get_list_of_followers(f"{start_account}")

    for target in targets:
        print(target)

    utils.save_to_file(targets, "message_sent_users")

    print(" ")
    print(f"{len(targets)}")

    user.logout()
