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

SLEEP_TIME_SECONDS = 1

problems_page_link_tags_difficulty = [
    (r"https://www.codechef.com/practice/basic-math-c", ["Math"], "Beginner"),
    (r"https://www.codechef.com/practice/arrays-c", ["Array"], "Beginner"),
    (r"https://www.codechef.com/practice/strings-c", ["String"], "Beginner"),
    (r"https://www.codechef.com/practice/sorting-c", ["Sorting"], "Beginner"),
    (r"https://www.codechef.com/practice/linked-lists", ["Linked list"], "Beginner"),
    (r"https://www.codechef.com/practice/two-pointers", ["Two pointers"], "Beginner"),
    (
        r"https://www.codechef.com/practice/stacks-and-queues",
        ["Stack", "Queue"],
        "Beginner",
    ),
    (r"https://www.codechef.com/practice/heaps", ["Heap"], "Beginner"),
    (
        r"https://www.codechef.com/practice/arrays-strings-sorting",
        ["Array", "String", "Sorting"],
        "Intermediate",
    ),
    (
        r"https://www.codechef.com/practice/greedy-algorithms",
        ["Greedy"],
        "Intermediate",
    ),
    (
        r"https://www.codechef.com/practice/binary-search",
        ["Binary search"],
        "Intermediate",
    ),
    (
        r"https://www.codechef.com/practice/dynamic-programming",
        ["Dynamic programming"],
        "Intermediate",
    ),
    (r"https://www.codechef.com/practice/number-theory", ["Math"], "Intermediate"),
]


def scrape_problems_on_page(
    driver: WebDriver, problems_page_link: str, tags: list[str], difficulty: str
) -> list[Problem]:
    """Scrapes the names and URLs of all problems on the given CodeChef page,
    and gives them the given tags and difficulty.

    Arguments:
        driver:             The Selenium WebDriver instance to use to scrape
                            CodeChef with.
        problems_page_link: The link to the CodeChef page containing a list of
                            problems to scrape.
        tags:               The list of tags to give each problem.
        difficulty:         The difficulty to give each problem.

    Returns:    The list of scraped problems.
    """
    driver.get(problems_page_link)
    time.sleep(SLEEP_TIME_SECONDS)
    page_source = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")
    soup = BeautifulSoup(page_source, features="lxml")
    anchors = soup.find_all("a", href=True)
    return [
        Problem(a["href"], a.text.strip(), difficulty, tags)
        for a in anchors
        if (
            # Has a class.
            a.has_attr("class")
            # Links to a problem.
            and a["class"][0].startswith("_problemName")
            # Not a multiple choice question.
            and a.text != "Multiple Choice Question"
        )
    ]


def main() -> int:
    argument_parser = ArgumentParser("CodeChef problem scraper")
    argument_parser.add_argument(
        "-o", "--output", type=str, required=True, help="Output file"
    )
    arguments = argument_parser.parse_args()
    output = arguments.output

    problem_name_to_problem: dict[str, Problem] = {}
    options = Options()
    options.add_argument("-headless")
    service = Service(executable_path=r"/snap/bin/firefox.geckodriver")
    with webdriver.Firefox(options=options, service=service) as driver:
        for i, (problems_page_link, tags, difficulty) in enumerate(
            problems_page_link_tags_difficulty, 1
        ):
            for problem in scrape_problems_on_page(
                driver, problems_page_link, tags, difficulty
            ):
                found_problem = problem_name_to_problem.get(problem.name)
                if found_problem:
                    assert found_problem.difficulty == problem.difficulty
                    problem_name_to_problem[problem.name].tags = list(
                        set(problem.tags) | set(found_problem.tags)
                    )
                else:
                    problem_name_to_problem[problem.name] = problem
            print(f"Scraped page {i} / {len(problems_page_link_tags_difficulty)}")

    with open(output, "w") as fp:
        json.dump(
            [asdict(problem) for problem in problem_name_to_problem.values()],
            fp,
            indent=4,
        )

    return 0


if __name__ == "__main__":
    exit(main())
