import requests
import matplotlib
import matplotlib.pyplot as plt
from   matplotlib.dates  import MonthLocator, DateFormatter
import datetime as dt

############################
##### Helper functions #####
############################

YEAR=2024

def url(topic, granularity='daily', time_start=f'{YEAR}0101', time_end=f'{YEAR}1231'):
    """Construct URL to fetch Wikipedia page views for a given topic"""
    url_parts = [
        'https://wikimedia.org/api/rest_v1/metrics',
        # If you want to change any of these: make it into an
        # argument for this function and replace the string with it
        'pageviews',
        'per-article',
        'en.wikipedia.org', # can add other languages
        'all-access',
        'all-agents',       # e.g. only mobile, only computer
        topic,
        granularity,
        time_start,
        time_end
        ]
    return '/'.join(url_parts)

def parse_date(str):
    """Parse a timestamp string into Python datetime object.
       Expected format: YYYYMMDDHH
    """
    return dt.datetime.strptime(str, '%Y%m%d%H')

def dates_views(topic):
    """Fetch the Wikipedia page views for topic.
       Returns the dates and pageviews in aligned lists.
    """
    dummy_headers = {
        'Authentication': '-',
        'User-Agent': '-'
    }
    wp_topic = topic.replace(' ', '_') # Turn name into Wikipedia title
    response = requests.get(url(wp_topic), headers=dummy_headers)
    topic_data = response.json()
    dates = []
    views = []
    for page_view in topic_data['items']:
        date = parse_date(page_view['timestamp'])
        dates.append(date)
        views.append(page_view['views'])
    return dates, views


#################################
##### Settings for the plot #####
#################################

## Custom style settings for the plot

bgcolor = 'lavenderblush'
textcolor = 'xkcd:dark magenta'
gridcolor = 'thistle'
pinkstyle = {
    'font.family': 'sans-serif',
    'font.sans-serif': ['Comic Sans MS'] \
      + plt.rcParams['font.sans-serif'], # fallback if Comic Sans MS doesn't exist
    'text.color': textcolor,
    'figure.facecolor': bgcolor,
    'xtick.color': textcolor,
    'ytick.color': textcolor,
    'axes.edgecolor': bgcolor,
    'axes.facecolor': bgcolor,
    'axes.grid': True,
    'grid.color': gridcolor,
    'legend.fancybox': True,
    'legend.shadow': True,
}

## Define formatter for page views: show numbers with comma, e.g. 800,000
LargeNumberFormatter = \
    matplotlib.ticker.FuncFormatter(lambda x, _pos: format(int(x), ','))

## Fabulous colors to plot our divas (https://matplotlib.org/stable/gallery/color/named_colors.html)
pinks = ['crimson', 'fuchsia', 'xkcd:bubblegum pink', 'orchid', 'hotpink']

## The pop divas to compare
divas = ['Beyoncé', 'Lady Gaga', 'Taylor Swift']

###################################
##### Finally, plot the divas #####
###################################

title = f'Who was the most popular pop diva in {YEAR}?' # YEAR is defined at the top of the file

## Use the predefined 'fivethirtyeight' style but make it more pink!
plt.style.use(['fivethirtyeight', pinkstyle])

## Create the figure
fig, ax = plt.subplots(num=title) # Use title as window title…
plt.title(title)                  # …and as the plot title.

# Plot each diva with a different color
for dname, dcolor in zip(divas, pinks):
    dates, views = dates_views(dname)
    ax.plot(dates, views,
            label=dname,   # Label with artist name
            color=dcolor,  # Use the assigned color
            alpha=0.8      # Slightly transparent (because of possible overlap)
            )

ax.xaxis.set_major_locator(MonthLocator())          # Set month as labels for x-axis
ax.xaxis.set_major_formatter(DateFormatter('%b'))   # 3-letter name like Jan, Feb
ax.yaxis.set_major_formatter(LargeNumberFormatter)  # Format large numbers with comma
plt.legend() # Display the name and color of the diva in a legend
plt.show()   # Show the plot!