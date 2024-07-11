# import pickle
from selenium import webdriver
import time

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


def main():
    urls = ["https://www.aftonbladet.se/", "https://www.expressen.se/", "https://www.svt.se/", "https://www.svd.se/",
            "https://www.dn.se/"]
    # TODO fix setup file

    # TODO change path
    # profile_dir = "/Users/william/Library/Application Support/Firefox/Profiles/zkr8w5jt.default-release"
    profile_dir = ""
    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    options.add_argument(f"{profile_dir}")
    driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    # TODO change value to find wanted monitor. 1000 should be offset per monitor from center monitor

    # driver.set_window_position(-1000, 0)
    driver.implicitly_wait(2)

    # driver.get(urls[0])
    # foo = input()
    # save_cookie(driver, '/Users/william/PycharmProjects/random_smaller_stuff/cookies')

    while True:
        curr_url = urls.pop(0)
        driver.get(curr_url)
        urls.append(curr_url)
        time.sleep(15)


if __name__ == "__main__":
    main()
