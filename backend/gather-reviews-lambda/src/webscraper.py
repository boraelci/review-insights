from io import StringIO
import boto3
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from sample_data.sample import sample_scraped_reviews


class WebScraper:
    def __init__(self, original_url, env):
        self.original_url = original_url
        self.number_pages = 1
        self.env = env
        self.s3 = boto3.client("s3")

        if env == "dev":
            self.driver = webdriver.Chrome()
        else:
            from headless_chrome import create_driver

            new_params = [
                "--no-sandbox",
            ]
            self.driver = create_driver(new_params)
            print("driver created")

    def run(self):
        driver = self.driver
        original_url = self.original_url
        number_pages = self.number_pages

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
            # Example: https://www.amazon.com/product-reviews/B01BZQJLFW/ref=cm_cr_getr_d_paging_btm_next_8?ie=UTF8&showViewpoints=1&pageNumber=1&sortBy=recent
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

            review_list = list()

            num_reviews_div = driver.find_element(
                By.CSS_SELECTOR, "div[data-hook='cr-filter-info-review-rating-count']"
            )
            num_reviews = num_reviews_div.text.split("total ratings, ")[1].split(
                " with reviews"
            )[0]
            if num_reviews == "0":
                break

            reviews = driver.find_elements(By.CSS_SELECTOR, "div[data-hook='review']")
            for i, r in enumerate(reviews):
                date_span = r.find_element(
                    By.CSS_SELECTOR, "span[data-hook='review-date']"
                )
                date = date_span.text.split("on ")[1]
                review_span = r.find_element(
                    By.CSS_SELECTOR, "span[data-hook='review-body']"
                )
                review = review_span.find_element(By.CSS_SELECTOR, "span").text.replace(
                    "\n", ""
                )
                stars_i = r.find_element(
                    By.CSS_SELECTOR, "i[data-hook='review-star-rating']"
                ).get_attribute("textContent")
                stars = stars_i.split(" out")[0]
                title_a = r.find_element(
                    By.CSS_SELECTOR, "a[data-hook='review-title']"
                ).text
                title = title_a.replace("\n", "")
                review_list.append((i, date, stars, title, review))

            amazon_reviews += review_list
            page += 1
        driver.quit()

        self.amazon_reviews = amazon_reviews
        print(self.amazon_reviews)

    def save(self, bucket_name, product_id, reviews):
        file_path = f"{product_id}.csv"
        if self.env == "dev":
            with open(file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["Index", "Date", "Stars", "Title", "Review"])
                writer.writerows(reviews)
        else:
            s3 = self.s3
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["Index", "Date", "Stars", "Title", "Review"])
            writer.writerows(reviews)
            csv_buffer.seek(0)
            s3.put_object(Bucket=bucket_name, Key=file_path, Body=csv_buffer.getvalue())
