import fetcher as f

data = f.load_config()
f.search_craigslist(data)
f.search_ebay(data)
