# import pickle
import selenium.common.exceptions
from selenium.common import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

from selenium.webdriver.support.wait import WebDriverWait


#
# def save_cookie(driver, path):
#     with open(path, 'wb') as filehandler:
#         pickle.dump(driver.get_cookies(), filehandler)
#
#
# def load_cookie(driver, path):
#     with open(path, 'rb') as cookiesfile:
#         cookies = pickle.load(cookiesfile)

#         for cookie in cookies:
#             driver.add_cookie(cookie)

def accept_cookies(driver):
    # In case cookies for some reason reset
    try:
        wait = WebDriverWait(driver, 1)
        button_def = (By.XPATH, "//button[text()='Tillåt alla cookies']")
        button = wait.until(EC.element_to_be_clickable(button_def))
        button.click()
        print("Clicked cookie")
        time.sleep(1)
    except (NoSuchElementException, TimeoutException):
        try:
            wait = WebDriverWait(driver, 1)
            button_def = (By.XPATH, "//button[text()='Allow all cookies']")
            button = wait.until(EC.element_to_be_clickable(button_def))
            button.click()
            print("Clicked cookie")
            time.sleep(1)
        except (NoSuchElementException, TimeoutException):
            print("No cookie option")
            pass

def main():
    try:
        with open("vars.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        with open("vars.txt", "w") as file:
            pass
        with open("vars.txt", "r") as file:
            lines = file.readlines()
    # Requires setup if vars file is empty
    require_setup = lines == []
    arg_count = len(sys.argv)
    if arg_count == 3:
        if sys.argv[1] == "--offset":
            offset = sys.argv[2]
            if is_offset_valid(offset):
                set_offset(offset)
        raise TypeError("Too many arguments, expected 1 for setup, 0 for running already initiated program.")
    elif arg_count < 2 and require_setup:
        raise TypeError(
            "Firefox/chrome profile path is needed for first time setup\n\nRerun file with 'newsbrowser.exe path\\to\\browser profile'")
    elif arg_count == 1 and not require_setup:
        run_program()
    elif arg_count == 2 and require_setup:
        path = sys.argv[1]
        setup(path)
        run_program()
    else:
        print(f"argcount: {arg_count} require_setup: {require_setup}. for running expected is 1 false.")
        raise SyntaxError("Unknown syntaxerror, try again")


def set_offset(offset):
    with open("vars.txt", "r") as file:
        lines = file.read().split(",")
        lines[1] = offset
    with open("vars.txt", "w") as file:
        file.write(",".join(lines))


def is_offset_valid(offset):
    try:
        if not int(offset) // 1000 == int(offset) / 1000:
            print("Not a multiple of 1000. Re-enter a correct multiple of 1000.")
            print("Enter program offset (multiple of 1000 per screen from main screen + for right - for left). Can be reconfigured by running program with newsbrowser.exe --offset [amount] ")
            return False
        else:
            return True
    except TypeError:
        # print(offset)
        print("Not a valid int, try again")
        return False
    except ValueError:
        # print(offset)
        print("Not a valid int, try again")
        return False


def setup(path):
    # while True:
    #     offset = input(
    #         "Enter program offset (multiple of 1000 per screen from main screen + for right - for left). Can be reconfigured by running program with newsbrowser.exe --offset [amount] ")
    #     if is_offset_valid(offset):
    #         break

    with open("vars.txt", "w") as file:
        if os.path.exists(path):
            file.write(f"{path}")
        else:
            raise FileNotFoundError(
                f"Couldnt find file at path {path}. Make sure it is a correct path to the profile file.")


def run_program():
    urls = ["https://www.aftonbladet.se/", "https://www.expressen.se/", "https://www.svt.se/", "https://www.svd.se/",
            "https://www.dn.se/"]
    try:
        with open("vars.txt", "r") as file:
            lines = file.read().split(",")
    except FileNotFoundError:
        with open("vars.txt", "w") as file:
            pass
        with open("vars.txt", "r") as file:
            lines = file.read().split(",")
    profile_dir = lines[0]
    if len(lines) > 1 and lines[1] != "":
        offset = int(lines[1])
    else:
        offset = 0
    # TODO add alternative for chrome?
    #profile_dir = "/Users/william/Library/Application Support/Firefox/Profiles/megaserver-local"
    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    # options.add_argument("-headless")
    options.add_argument(profile_dir)
    driver = webdriver.Firefox(options=options)

    # find wanted monitor. 1000 should be offset per monitor from center monitor
    driver.maximize_window()
    driver.set_window_position(offset, 0)
    driver.implicitly_wait(2)

    counter = 0
    waiting_time = 10

    while True:
        try:
            curr_url = urls.pop(0)
            driver.get(curr_url)
            urls.append(curr_url)
            print(counter)
            if counter < len(urls): # check that every site is visited once (should fix cookies always)
                accept_cookies(driver)
                counter += 1

                time.sleep(waiting_time - 3)
            else:
                time.sleep(waiting_time)

        except:
            print("Window closed")
            driver.quit()
            break
    # driver.get(urls[0])
    # foo = input()
    # save_cookie(driver, '/Users/william/PycharmProjects/random_smaller_stuff/cookies')


if __name__ == "__main__":
    main()
