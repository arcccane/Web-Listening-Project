import csv
import os
import pandas as pd
from time import sleep
from selenium.common import exceptions
from hwz.hwz1 import create_webdriver_instance

""" Fetches the actual data using the urls collected"""

def forum_search(link, driver):
    try:
        url = str(link)
        driver.get(url)
        """Below line changes the browser size to be not visible. Do not minimize the browser"""
        driver.set_window_position(-2000,0)
        sleep(1)
        return True
    except exceptions.WebDriverException as e:
        print(e.stacktrace)

def generate_id(data):
    return ''.join(data)

def pagination(driver):
    try:
        next_page_button = driver.find_element_by_xpath(f'.//a[@class="pageNav-jump pageNav-jump--next"]')
        next_page_button.click()
        return False
    except exceptions.NoSuchElementException:
        return True

def save_data_to_csv(records, filepath, mode='a+'):
    header = ["platform","forum_url","forum_title","date","username","body","blockquote","media"]
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
    cards = driver.find_elements_by_xpath('//article[@class="message message--post js-post js-inlineModContainer  "]')
    return cards

def extract_forum_data(card):
    try:
        title = card.find_element_by_xpath('//*[@id="top"]/div[2]/div[2]/div[1]/div[2]/div[1]/h1').text
    except exceptions.NoSuchElementException:
        title = ""
    try:
        unclean_date = card.find_element_by_xpath('.//time[@itemprop="datePublished"]').get_attribute('datetime')
        date = unclean_date.replace('+0800','+00:00').replace('T',' ')
    except exceptions.NoSuchElementException:
        date = ""
    try:
        user = card.find_element_by_xpath('.//a[@class="username "]').text
    except exceptions.NoSuchElementException:
        user = ""
    try:
        comment = card.find_element_by_xpath('.//div[@class="bbWrapper"]').text
    except exceptions.NoSuchElementException:
        comment = ""
    try:
        blockquote = card.find_element_by_xpath('.//div[@class="bbCodeBlock-expandContent js-expandContent "]').text
    except exceptions.NoSuchElementException:
        blockquote = ""
    try:
        media = card.find_element_by_xpath('.//img[@class="bbImage"]').get_attribute('src')
    except exceptions.NoSuchElementException:
        media = ""
    data = ["HardwareZone",title,date,user,comment,blockquote,media]
    return data

def fetch_data(filepath=f'hwz/dataset/{"".join(os.listdir("hwz/urls"))}'):

    for f in os.listdir('hwz/dataset'):
        os.remove(os.path.join('hwz/dataset', f))

    save_data_to_csv(None, filepath, 'w')
    unique_ids = set()

    driver = create_webdriver_instance()

    df = pd.read_csv(f"hwz/urls/{os.listdir('hwz/urls')[0]}")
    for row in df.iterrows():
        link = row[1]['url']
        hwz_search_page_term = forum_search(link, driver)
        if not hwz_search_page_term:
            return

        end_of_page = False

        while not end_of_page:
            cards = collect_all_cards_from_current_view(driver)
            for card in cards:
                try:
                    data = extract_forum_data(card)
                    data.insert(1,link)
                    # print(data)
                except exceptions.StaleElementReferenceException:
                    continue
                if not data:
                    continue
                data_id = generate_id(data)
                if data_id not in unique_ids:
                    unique_ids.add(data_id)
                    save_data_to_csv(data, filepath)
            end_of_page = True  # pagination(driver)
            sleep(0.5)
    driver.quit()
