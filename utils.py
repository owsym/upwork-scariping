import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def scrape_freelancer_data(url, start_page, end_page):
    driver = webdriver.Chrome(executable_path="chromedriver")
    driver.get(url)
    time.sleep(15)
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    freelancers_data = []

    for page_number in range(1, start_page):
        try:
            next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-icon")))
            if not next_button.is_displayed():
                break
            next_button.click()
            time.sleep(2)
        except (NoSuchElementException, TimeoutException):
            break

    for page_number in range(start_page, end_page + 1):
        last_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(0.5)
        new_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_scroll_height == last_scroll_height:
            try:
                next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-icon")))
                if not next_button.is_displayed():
                    break
                next_button.click()
                time.sleep(2)
            except (NoSuchElementException, TimeoutException):
                break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data = soup.find_all('div', {'class': 'up-card-section up-card-hover'})

        for extract_data in data:
            name = extract_data.find('div', {"class": "identity-name"}).text.strip()
            role = extract_data.find('p', {'class': 'my-0 freelancer-title'}).text.strip()
            country = extract_data.find('span', {'class': 'd-inline-block vertical-align-middle'}).text.strip()
            hourly_rate = extract_data.find('div', {'data-qa': 'rate'}).text.strip()
            earned_amount = extract_data.find('span', {'data-test': 'earned-amount-formatted'})
            total_earned = earned_amount.text.strip() if earned_amount else ""
            job_success_rate = extract_data.find('span', {'class': 'up-job-success-text'}).text.strip().replace('\n', '').replace('            ', '')
            badge = extract_data.find('span', {'class': 'status-text d-flex top-rated-badge-status'}).text.strip()
            description = extract_data.find('div', {'class': 'up-line-clamp-v2 clamped'}).text.strip()
            company_name_element = extract_data.find('div', {'class': 'd-flex align-items-center up-btn-link'})
            company_name = company_name_element.text.strip() if company_name_element else ""
            company_earned_element = extract_data.find('div', {'class': 'ml-10 agency-box-stats'})
            company_earned = company_earned_element.text.strip() if company_earned_element else ""
            raw_html = extract_data.prettify()
            profile_links = soup.find_all('div', {'class': 'd-flex justify-space-between align-items-start'})
            split_data = str(profile_links).split()
            sliced_data = split_data[9:10]
            split_sliced_data = sliced_data[0].split("=")
            final = split_sliced_data[1]
            final = final.replace('"', '')
            profile_link = 'https://www.upwork.com/freelancers/' + final
            company_links = soup.find_all('div', {'class': 'cfe-ui-freelancer-tile-agency-box-legacy mt-5 mt-10 agency-box-legacy--link'})
            split_data = str(company_links).split(" ")
            sliced_data = split_data[5:6]
            split_sliced_data = sliced_data[0].split('=')
            sliced_split_sliced_data = split_sliced_data[1:]
            cleaned_data = sliced_split_sliced_data[0].strip('[]').strip('"')
            company_link = 'https://www.upwork.com/agencies/' + cleaned_data
            freelancer_data = {
                "Name": name,
                "Country": country,
                "Badge": badge,
                "Job Success Rate": job_success_rate,
                "Hourly Rate": hourly_rate,
                "Total Earned": total_earned,
                "Role": role,
                "Description": description,
                "Profile Link": profile_link,
                "Company Name": company_name,
                "Company Earned": company_earned,
                "Company Link": company_link,
                "Raw HTML": raw_html
            }
            freelancers_data.append(freelancer_data)

    driver.quit()
    return freelancers_data


def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Name', 'Country', 'Badge', 'Job Success Rate', 'Hourly Rate', 'Total Earned', 'Role', 'Description',
            'Profile Link', 'Company Name', 'Company Earned', 'Company Link', 'Raw HTML'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {filename}")
