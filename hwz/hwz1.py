import csv
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

""" Fetches urls from forum"""

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

def create_webdriver_instance():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=chrome_options)
        set_viewport_size(driver,800,600)
        return driver
    except exceptions.SessionNotCreatedException as e:
        print(e)

def hwz_search(driver, search_term):
    url = 'https://www.hardwarezone.com.sg/search/forum/'
    driver.get(url)
    """Below line changes the browser size to be not visible. Do not minimize the browser"""
    driver.set_window_position(-2000,0)
    sleep(3)

    try:
        skip_ad = driver.find_element_by_xpath('.//span[contains(text(), "Skip Ad") or contains(text(), "Close Ad")]')
        skip_ad.click()
    except exceptions.NoSuchElementException:
        pass

    search_input = driver.find_element_by_xpath('//input[@title="Search HWZ Singapore"]')
    search_input.send_keys(search_term)
    search_input.send_keys(Keys.RETURN)
    sleep(3)

    try:
        skip_ad = driver.find_element_by_xpath('.//span[contains(text(), "Skip Ad") or contains(text(), "Close Ad")]')
        skip_ad.click()
    except exceptions.NoSuchElementException:
        pass
    return True

def change_page_content(tab_name, driver):
    tab = driver.find_element_by_link_text(tab_name)
    tab.click()
    sleep(1)
    xpath_tab_state = f'//li/a[contains(text(),\"{tab_name}\") and @class=\"tab on\"]'
    return xpath_tab_state

def generate_id(url):
    return ''.join(url)

def pagination(driver):
    try:
        current_page_no = int(driver.find_element_by_xpath('.//div[@class="gsc-cursor-page gsc-cursor-current-page"]').text)
        next_page = driver.find_element_by_xpath(f'.//div[@class="gsc-cursor"]/div[contains(text(), "{current_page_no + 1}")]')
        # print(next_page.text)
        next_page.click()
        sleep(1)
        return False
    except exceptions.NoSuchElementException:
        return True

def save_url_to_csv(records, filepath, mode='a+'):
    header = ["url"]
    try:
        with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if mode == 'w':
                writer.writerow(header)
            if records:
                writer.writerow(records)
    except IOError:
        print('File issue')

def collect_all_cards_from_current_view(driver):
    cards = driver.find_elements_by_xpath('//div[@class="gsc-webResult gsc-result"]')
    return cards

def extract_forum_urls(card):
    sleep(0.5)
    try:
        url = card.find_element_by_xpath('.//a[@class="gs-title"]').get_attribute('href')
    except exceptions.NoSuchElementException:
        url = ""
    row = (url,)
    return row

def fetch_urls(keywords_list, filepath, page_content='Forum'):
    filename = ' '.join(keywords_list)
    path = f'{filepath}/{filename}.csv'

    for f in os.listdir(filepath):
        os.remove(os.path.join(filepath, f))

    save_url_to_csv(None, path, 'w')
    end_of_forum = False
    unique_ids = set()

    print(f"\nFetching data from hwz forum: {filename} ...")
    driver = create_webdriver_instance()
    hwz_search_page_term = hwz_search(driver, filename)
    if not hwz_search_page_term:
        return

    change_page_content(page_content, driver)

    while not end_of_forum:
        cards = collect_all_cards_from_current_view(driver)
        for card in cards:
            try:
                url = extract_forum_urls(card)
            except exceptions.StaleElementReferenceException:
                continue
            if not url:
                continue
            url_id = generate_id(url)
            if url_id not in unique_ids:
                unique_ids.add(url_id)
                save_url_to_csv(url, path)
        end_of_forum = pagination(driver)
    driver.quit()
