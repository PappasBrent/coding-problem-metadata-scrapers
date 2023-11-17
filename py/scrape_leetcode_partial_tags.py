import datetime
import json
import time
from argparse import ArgumentParser
from dataclasses import asdict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver

from problem import Problem

GET_SLEEP_SECONDS = 5
CLICK_SLEEP_SECONDS = 1


def scrape_number_of_problem_pages(driver: WebDriver) -> int:
    first_page_url = r"https://leetcode.com/problemset/all/?page=1"
    driver.get(first_page_url)
    time.sleep(GET_SLEEP_SECONDS)
    page_source = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")
    soup = BeautifulSoup(page_source, features="lxml")
    pagination_nav = soup.select_one("nav.flex.flex-nowrap.items-center")
    pagination_nav_buttons = pagination_nav.find_all("button")
    last_page_button = pagination_nav_buttons[-2]
    return int(last_page_button.text)


def scrape_problems_on_page(driver: WebDriver, page_number: int) -> list[Problem]:
    leetcode_base_url = "https://leetcode.com"
    problem_page_base_url = r"https://leetcode.com/problemset/all/"
    driver.get(problem_page_base_url + f"?page={page_number}")
    time.sleep(GET_SLEEP_SECONDS)

    settings_button = driver.find_element(
        By.CSS_SELECTOR, r"button[aria-label='settings']"
    )
    settings_button.click()
    time.sleep(CLICK_SLEEP_SECONDS)

    show_tags_checkmark = driver.find_element(By.CSS_SELECTOR, r"div[role='switch']")
    show_tags_checkmark.click()
    time.sleep(CLICK_SLEEP_SECONDS)

    page_source = driver.find_element(By.XPATH, r"//body").get_attribute("outerHTML")
    soup = BeautifulSoup(page_source, features="lxml")
    problem_as = [
        a
        for a in soup.find_all("a", href=True)
        if all(
            [
                # Only problem links
                a["href"].startswith("/problems/"),
                # No solution links
                not a["href"].endswith("/solution"),
                # No daily problems
                "?envType=daily-question" not in a["href"],
                # Not premimum
                a.parent.find_next_sibling("svg") is None,
            ]
        )
    ]
    problem_difficulties = [
        a.parent.parent.parent.parent.parent.parent.find_all("div", recursive=False)[
            4
        ].text
        for a in problem_as
    ]
    problem_tags = []
    for a in problem_as:
        if (
            (parent := a.parent)
            and (grandparent := parent.parent)
            and (next_ := grandparent.find_next_sibling("div"))
        ):
            problem_tags.append([span.text for span in next_.find_all("span") if span])

    problems = [
        Problem(
            url=leetcode_base_url + a["href"],
            name=a.text,
            difficulty=difficulty,
            tags=tags,
        )
        for a, difficulty, tags in zip(problem_as, problem_difficulties, problem_tags)
    ]
    return problems


def main() -> int:
    argument_parser = ArgumentParser("LeetCode problem scraper")
    argument_parser.add_argument("-o", "--output", type=str, required=True)
    arguments = argument_parser.parse_args()
    output = arguments.output

    all_problems = []
    options = Options()
    options.add_argument("-headless")
    service = Service(executable_path=r"/snap/bin/firefox.geckodriver")
    with webdriver.Firefox(options=options, service=service) as driver:
        num_pages = scrape_number_of_problem_pages(driver)
        timedelta = datetime.timedelta(
            seconds=num_pages * (GET_SLEEP_SECONDS + CLICK_SLEEP_SECONDS * 2)
        )
        end_time = datetime.datetime.now() + timedelta
        print(f"Estimated time to complete: {timedelta} ({end_time})")

        for page_number in range(1, num_pages + 1):
            problems_on_page = scrape_problems_on_page(driver, page_number)
            all_problems.extend(problems_on_page)
            print(f"Scraped page {page_number} / {num_pages}")

    with open(output, "w") as fp:
        json.dump([asdict(problem) for problem in all_problems], fp, indent=4)

    return 0


if __name__ == "__main__":
    exit(main())
