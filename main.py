from utils import scrape_freelancer_data, save_data_to_csv

URL = "https://www.upwork.com/ab/profiles/search/?category_uid=531770282580668418&page=1&top_rated_plus=yes"
start_page = int(input("Enter the start page number: "))  
end_page = int(input("Enter the end page number: "))

freelancers_data = scrape_freelancer_data(URL, start_page, end_page)

filename = 'extracted_freelancers_data.csv'
save_data_to_csv(freelancers_data, filename)
