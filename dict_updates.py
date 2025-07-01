# Dummy data for demonstration purposes
def dummy_data(timestamp, views):
  return {"timestamp": timestamp, "views": views, "article": f"Article {views}"}

articles1 = [dummy_data("20241231", 1), dummy_data("20250101", 1)]
articles2 = [dummy_data("20241231", 2), dummy_data("20250101", 2)]
articles3 = [dummy_data("20241231", 3), dummy_data("20250101", 3)]


# Demonstration of dict manipulation
big_unified_dict = {} # Start the new dictionary

def update_dict(articles):
    for article in articles:
        timestamp = article["timestamp"]
        new_dict = {article["article"]: article["views"]}

        # If there is nothing in big_unified_dict with current timestamp, insert {}
        # If there is a value in big_unified_dict with current timestamp, leave it untouched
        big_unified_dict.setdefault(timestamp, {})

        # Now we know there is something in big_unified_dict[timestamp]:
        # either an empty list, or whatever was there already
        # So we can safely update the value there!
        big_unified_dict[timestamp].update(new_dict)


# Apply the function to these lists of article views
update_dict(articles1)
update_dict(articles2)
update_dict(articles3)

print(big_unified_dict)

## Output looks like this:
{ '20241231' :
    { 'Article 1' : 1
    , 'Article 2' : 2
    , 'Article 3' : 3
    }
, '20250101' :
    { 'Article 1' : 1
    , 'Article 2' : 2
    , 'Article 3' : 3
    }
}
