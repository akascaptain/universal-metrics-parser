import pandas as pd
from bs4 import BeautifulSoup

def clean_keep_unit(text):
    return " ".join(text.replace(",", "").split())

def parse_metric_cards_from_html(soup, metric_name):
    cards = soup.find_all("div", class_="topRow")
    data = []

    for card in cards:
        country_tag = card.find("div", class_="longFormName")
        value_tag = card.find("div", class_="valueContainer")

        if not country_tag or not value_tag:
            continue

        country = country_tag.get_text(strip=True)
        raw_text = value_tag.get_text(" ", strip=True)
        clean_value = clean_keep_unit(raw_text)

        data.append([country, clean_value])

    df = pd.DataFrame(data, columns=["country", metric_name])
    return df