# Coding website problem metadata scrapers
Scripts for scraping metadata of coding problems from popular coding websites,
and for generating a random sample of scraped problems.

## Getting started

#### Requirements
- Bash shell
- Make
- Python 3 with the following packages
  - BeautifulSoup 4
  - Selenium
- The firefox webdriver

### Running the code
To run the scrapers and generate a random sample of the data, simply run `make`
at the top-level project directory:
```
make
```

## TODO
- Change the scraper scripts to accept the path to the web driver as an
  argument.
- Allow the scraper scripts to use other web driver than firefox.
- Make the scrapers more robust.
- Improve documentation.

## Notes
- By default, we sample problems with the following tags: Array, Bit
  Manipulation, Linked List, Math, Stack, String, Queue, Recursion, Sorting. We
  choose these tags because they are present in the syllabi for UCF courses for
  [Intro to
  C](http://www.cs.ucf.edu/courses/cop3223/fall2023/section2/3223schedFa2023.pdf)
  and
[CS1](http://www.cs.ucf.edu/courses/cop3502/fall2021/COP3502-Sec12-Syllabus-Fall21.pdf).
  
- LeetCode problem metadata was last scraped on Nov 14 16:35 EST.
- CodeChef problem metadata was last scraped on Nov 14 15:43 EST.

<!--
- Need to use selenium because LeetCode problems page has dynamic content.
- Chose to use Firefox webdriver because it comes pre-packaged with Linux
  distributions.
-->