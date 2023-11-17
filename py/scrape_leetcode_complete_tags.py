import datetime
import json
import time
from argparse import ArgumentParser
from dataclasses import asdict, replace

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver

from problem import Problem

ESTIMATED_STARTUP_SECONDS = 4
SLEEP_SECONDS = 3


def load_problems_json(file: str) -> list[Problem]:
    with open(file) as fp:
        return [Problem(**problem_dict) for problem_dict in json.load(fp)]


def get_webdriver_page_as_soup(driver: WebDriver) -> BeautifulSoup:
    page_source = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")
    return BeautifulSoup(page_source, features="lxml")


def complete_problem_tags(driver: WebDriver, problem: Problem) -> Problem:
    """
    Visits a problem's URL, scrapes its tags, and returns a copy of the problem
    with its tags filled in.
    """
    driver.get(problem.url)
    time.sleep(SLEEP_SECONDS)
    soup = get_webdriver_page_as_soup(driver)
    anchors = soup.find_all("a", href=True)
    tag_anchors = [a for a in anchors if a["href"].find("/tag/") != -1]
    tags = [tag_anchor.text for tag_anchor in tag_anchors]
    return replace(problem, tags=tags)


def has_partial_tags(problem: Problem) -> bool:
    # Only fill in tags for problems whose lists contain a "1+", "2+", etc.,
    # which signify more tags to be filled in.
    return any(tag.endswith("+") for tag in problem.tags)


def main() -> int:
    argument_parser = ArgumentParser("LeetCode problem tag scraper")
    argument_parser.add_argument(
        "-p",
        "--problems_json",
        type=str,
        required=True,
        help="JSON file containing LeetCode problems with partially filled tag lists",
    )
    argument_parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="File to dump problems with complete tags to",
    )

    args = argument_parser.parse_args()
    problems_json = args.problems_json
    output = args.output

    problems_with_maybe_partial_tags = load_problems_json(problems_json)
    problems_with_complete_tags: list[Problem] = [
        problem
        for problem in problems_with_maybe_partial_tags
        if not has_partial_tags(problem)
    ]
    problems_with_partial_tags = [
        problem
        for problem in problems_with_maybe_partial_tags
        if has_partial_tags(problem)
    ]
    timedelta = datetime.timedelta(
        seconds=len(problems_with_partial_tags) * SLEEP_SECONDS
        + ESTIMATED_STARTUP_SECONDS
    )
    end_time = datetime.datetime.now() + timedelta
    print(f"Total problems: {len(problems_with_maybe_partial_tags)}")
    print(f"Problems with partial tags: {len(problems_with_partial_tags)}")
    print(f"Estimated time to complete: {timedelta} ({end_time})")

    options = Options()
    options.add_argument("-headless")
    service = Service(executable_path=r"/snap/bin/firefox.geckodriver")
    with webdriver.Firefox(options=options, service=service) as driver:
        for i, problem in enumerate(problems_with_partial_tags):
            problems_with_complete_tags.append(complete_problem_tags(driver, problem))
            print(f"Completed tags for problem {i} / {len(problems_with_partial_tags)}")

    with open(output, "w") as fp:
        json.dump(
            [asdict(problem) for problem in problems_with_complete_tags], fp, indent=4
        )

    return 0


if __name__ == "__main__":
    exit(main())
