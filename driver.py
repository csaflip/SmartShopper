import fetcher as f
data = f.load_config()
cl_results = f.search_craigslist(data)
ebay_results = f.search_ebay(data)
