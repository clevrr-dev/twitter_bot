# import time
import random
import sys
from time import sleep

from selenium import webdriver
from selenium.common import exceptions

import utils
from user import TwitterUser

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# driver.maximize_window()
driver.implicitly_wait(5)


def main(message):
    """
    code starts here
    :return:
    """
    credentials = utils.read_csv_file('accounts')
    # targets = utils.read_file('usernames')

    message_sent = set(utils.read_file('message_sent_users'))
    locked_dm = set(utils.read_file('locked_dm_users'))

    # shuffle credentials
    random.shuffle(credentials)

    for credential in credentials:
        print(credential)
        username, password, email = credential

        # user = TwitterUser(driver, "YapanDilruba", "24v47v86", "shbprlukhof@outlook.com")
        user = TwitterUser(driver, username, password, email)

        try:
            user.login()
            sleep(5)

            targets = user.get_list_of_followers("ChristopheNice1")

            sleep(5)

            for target in targets:
                # check if message has already been sent to target
                # and if target's dm is locked
                print(target)
                if target not in message_sent and target not in locked_dm:
                    # send message
                    sleep(random.randint(3, 7))
                    sent_status = user.send_message(target, message)

                    # check if message was sent
                    if sent_status == 0:
                        locked_dm.add(target)
                        print(f"{target}'s DM is locked...")

                    if sent_status == 1:
                        message_sent.add(target)
                        print(f"Message sent to {target}")

            sleep(random.randint(3, 6))
            user.logout()

            sys.exit()

            # sleep(random.randint(3, 6))

        except exceptions.NoSuchElementException as e:
            print(e)

        # save to file
        utils.save_to_file(message_sent, "message_sent_users")
        utils.save_to_file(locked_dm, "locked_dm_users")


if __name__ == "__main__":
    # import threading
    print("Enter message to send")
    m = input(">>>")
    # m = "Wow, Follow @christysaint699 Twitter. Her OF is only $3.50"
    main(m)
