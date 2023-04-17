from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import ENV
import pandas as pd
import csv
from sample_data.sample import sample_scraped_reviews


def main(original_url, number_pages):
    if ENV == "dev":
        driver = webdriver.Chrome()
    else:
        options = Options()

        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        # options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(
            executable_path=str(os.environ.get("CHROMEDRIVER_PATH")),
            chrome_options=options,
        )

    if original_url == "auto":
        # original_url = "https://www.amazon.com/Apple-AirPods-Charging-Latest-Model/dp/B07PXGQC1Q/ref=sr_1_1_sspa?dchild=1&keywords=airpods&qid=1610226273&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFVNkIyMEFDM0NEWkEmZW5jcnlwdGVkSWQ9QTA0NDI5MDgyVkZDOVNMVUtIUUdaJmVuY3J5cHRlZEFkSWQ9QTAzMDg3NzMyQzIzWFNBVjJGMUxXJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
        original_url = "https://www.amazon.com/Tide-Febreze-Defense-Detergent-Packaging/dp/B01BZQJLFW/ref=asc_df_B01BZQJLFW/?tag=hyprod-20&linkCode=df0&hvadid=309832782859&hvpos=&hvnetw=g&hvrand=14385160540479028809&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9073502&hvtargid=pla-425063129473&psc=1&tag=&ref=&adgrpid=70155173188&hvpone=&hvptwo=&hvadid=309832782859&hvpos=&hvnetw=g&hvrand=14385160540479028809&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9073502&hvtargid=pla-425063129473"
    number_pages = 2  # 100 pages = 950 almost 1000 reviews

    driver.get(original_url)
    # img_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "imgTagWrapper")))
    # product_image_url = img_div.find_element_by_tag_name("img").get_attribute("src")
    # product_sub_category = driver.find_element_by_class_name("nav-a-content").text
    product_code = original_url.split("/dp/")[1].split("/ref")[0]

    amazon_reviews = list()
    page = 1
    while page <= number_pages:
        url = f"https://www.amazon.com/product-reviews/{product_code}/ref=cm_cr_getr_d_paging_btm_next_8?ie=UTF8&showViewpoints=1&pageNumber={page}&sortBy=recent"
        driver.get(url)

        # wait for num_review_count to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[4]/div",
                )
            )
        )

        source = driver.page_source
        review_list = list()
        soup = BeautifulSoup(source, "lxml")

        # check if no more reviews
        num_reviews_div = soup.find(
            "div", attrs={"data-hook": "cr-filter-info-review-rating-count"}
        )
        print(num_reviews_div)
        num_reviews = num_reviews_div.text.split("total ratings, ")[1].split(
            " with reviews"
        )[0]
        if num_reviews == "0":
            break

        reviews = soup.find_all("div", attrs={"data-hook": "review"})
        for r in reviews:
            date_span = r.find("span", attrs={"data-hook": "review-date"})
            date = date_span.text.split("on ")[1]
            review_span = r.find("span", attrs={"data-hook": "review-body"})
            review = review_span.find("span").text.replace("\n", "")
            stars_a = r.find("i", attrs={"data-hook": "review-star-rating"}).text
            stars = stars_a.split(" out")[0]
            title_a = r.find("a", attrs={"data-hook": "review-title"}).text
            title = title_a.replace("\n", "")
            review_list.append((date, stars, title, review))
        soup.decompose()

        amazon_reviews += review_list
        page += 1
    driver.quit()

    print(amazon_reviews)
    save(amazon_reviews)
    # category = Category.objects.get(name=product_sub_category)
    # result = Result.objects.create(order=order, image_url=product_image_url, code=product_code, category=category, reviews=amazon_reviews, review_count=len(amazon_reviews))


def save(data):
    columns = ["Date", "Stars", "Title", "Review"]
    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv("./reviews.csv", sep=",", quoting=csv.QUOTE_ALL, index_label="Index")


main("auto", 2)
# save(sample_scraped_reviews)
