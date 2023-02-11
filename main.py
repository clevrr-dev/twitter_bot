# import time
import utils
import random

from time import sleep

from selenium import webdriver

from user import TwitterUser

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)

driver.implicitly_wait(3)


def main(message):
    """
    code starts here
    :return:
    """
    credentials = utils.read_csv_file('accounts')

    message_sent = set(utils.read_file('message_sent_users'))
    locked_dm = set(utils.read_file('locked_dm_users'))

    # shuffle credentials
    random.shuffle(credentials)

    start_account = utils.read_file("starting_account.txt")[0]

    for credential in credentials:
        print(credential)
        username, password, email = credential

        user = TwitterUser(driver, username, password, email)

        user.login()
        sleep(3)

        targets = user.get_list_of_followers(f"{start_account}")

        for target in targets:
            # check if message has already been sent to target
            # and if target's dm is locked
            print(target)
            if target not in message_sent and target not in locked_dm:
                # send message
                sleep(random.randint(3, 5))
                sent_status = user.send_message(target, message)

                # check if message was sent
                if sent_status == 0:
                    locked_dm.add(target)
                    print(f"{target}'s DM is locked")
                    print("")

                if sent_status == 1:
                    message_sent.add(target)
                    print(f"Message sent to {target}")
                    print("")

                if sent_status == 2:
                    locked_dm.add(target)
                    print("Account not found")

        sleep(random.randint(3, 6))
        user.logout()

        # pick a random target as start_account for next loop
        start_account = list(targets)[0]

        # save to file
        utils.save_to_file(message_sent, "message_sent_users")
        utils.save_to_file(locked_dm, "locked_dm_users")


if __name__ == "__main__":
    # start here
    message = utils.read_file("message.txt")
    comp_message = " ".join(message)
    main(comp_message)
