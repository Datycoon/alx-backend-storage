# web.py

import requests
import time
from functools import wraps
from typing import Dict

cache: Dict[str, tuple] = {}

def get_page(url: str) -> str:
    if url in cache:
        print(f"Retrieving from cache: {url}")
        return cache[url][0]
    else:
        print(f"Retrieving from web: {url}")
        response = requests.get(url)
        result = response.text
        cache[url] = (result, time.time())
        return result

def cache_with_expiration(expiration: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            key = f"count:{url}"
            if key in cache:
                count, timestamp = cache[key]
                if time.time() - timestamp > expiration:
                    result = func(*args, **kwargs)
                    cache[key] = (count+1, time.time())
                    return result
                else:
                    cache[key] = (count+1, timestamp)
                    return cache[url][0]  # Return cached result
            else:
                result = func(*args, **kwargs)
                cache[key] = (1, time.time())
                return result
        return wrapper
    return decorator

@cache_with_expiration(expiration=10)
def get_page_cached(url: str) -> str:
    return get_page(url)

# Example usage
if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    
    for _ in range(5):
        html_content = get_page_cached(slow_url)
        print(f"HTML content: {html_content}")
        
        time.sleep(2)

    access_count, timestamp = cache.get(f"count:{slow_url}", (0, 0))
    print(f"Access count for {slow_url}: {access_count}")

