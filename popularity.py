import requests
import matplotlib.pyplot as plt
from   matplotlib.dates  import MonthLocator, DateFormatter
import datetime as dt


############################
##### Helper functions #####
############################

def url(topic, granularity="daily", time_start="20240101", time_end="20241231"):
    url_parts = [
        "https://wikimedia.org/api/rest_v1/metrics",
        # If you want to change any of these: make it into an
        # argument for this function and replace the string with it
        "pageviews",
        "per-article",
        "en.wikipedia.org", # can add other languages
        "all-access",
        "all-agents",       # e.g. only mobile, only computer
        topic,
        granularity,
        time_start,
        time_end
        ]
    return "/".join(url_parts)

def parse_date(str):
    return dt.datetime.strptime(str, '%Y%m%d%H')

def dates_views(topic):
    dummy_headers = {
        "Authentication": "-",
        "User-Agent": "-"
    }
    response = requests.get(url(topic), headers=dummy_headers)
    topic_data = response.json()
    dates = []
    views = []
    for page_view in topic_data["items"]:
        date = parse_date(page_view["timestamp"])
        dates.append(date)
        views.append(page_view["views"])
    return dates, views


###########################
##### Create the plot #####
###########################

fig, ax = plt.subplots()

## Visually distinct colors, source: https://sashamaps.net/docs/resources/20-colors/
distinct_colors = [
    '#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
    '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff',
    '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
    '#000075', '#a9a9a9', '#ffffff', '#000000' ]

## Some pink-ish colors (https://matplotlib.org/stable/gallery/color/named_colors.html)
pinks = ["crimson", "fuchsia", "lightpink", "orchid", "hotpink", "lavenderblush"]

divas = ["Beyoncé", "Lady Gaga", "Taylor Swift"]

for dname, dcolor in zip(divas, pinks):
    wp_diva = dname.replace(" ", "_")
    dates, views = dates_views(wp_diva)
    ax.plot(dates,views, label=dname, color=dcolor)


ax.xaxis.set_major_locator(MonthLocator())        # Set month as labels for x-axis
ax.xaxis.set_major_formatter(DateFormatter('%b')) # 3-letter name like Jan, Feb
plt.legend()                                      # Display the name and color of the diva
plt.show()



