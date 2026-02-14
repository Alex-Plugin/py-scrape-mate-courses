import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

MAIN_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def fetch_html(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_main_page(html: str) -> list[tuple[str, str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a.ProfessionCard_cardWrapper__BCg0O")

    courses_data = []
    seen = set()

    for card in cards:
        href = card.get("href")
        if not href or href in seen:
            continue

        seen.add(href)

        name_el = card.select_one("h3 span")
        duration_el = card.select_one("p.ProfessionCard_duration__13PwX")

        name = name_el.text.strip() if name_el else ""
        duration = duration_el.text.strip() if duration_el else ""

        full_url = MAIN_URL + href

        if name:
            courses_data.append((name, duration, full_url))

    return courses_data


def parse_course_page(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    desc_el = soup.select_one("p.SalarySection_aboutProfession__C6ftM")
    return desc_el.text.strip() if desc_el else ""


def get_all_courses() -> list[Course]:
    main_html = fetch_html(MAIN_URL)
    courses_raw = parse_main_page(main_html)

    courses = []

    for name, duration, url in courses_raw:
        page_html = fetch_html(url)
        short_desc = parse_course_page(page_html)

        courses.append(
            Course(
                name=name,
                short_description=short_desc,
                duration=duration,
            )
        )
    print(courses)
    return courses
