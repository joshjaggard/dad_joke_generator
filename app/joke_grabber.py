import httpx
import logging

logging.basicConfig(level=logging.WARNING)

def joke_grabber(url):
    
    set_headers = {
        "User-Agent": "Dad Joke Generator (https://github.com/joshjaggard/dad_joke_generator)",
        "Accept": "application/json",
    }
    
    try:
        get_joke = httpx.get(url, headers=set_headers)
        joke_raw = get_joke
        # Get joke in JSON format
        joke_json = joke_raw.json()
        logging.info(f'joke_json var = {joke_json}')
        joke_id = joke_json['id']
        logging.info(f'joke_id var = {joke_id}')
        joke = joke_json['joke']
        logging.info(f'joke var = {joke}')
        joke_link = url + f'/j/{joke_id}'
        logging.warning(f'Dad joke delivered... {joke_link}')

        return joke, joke_link

    except Exception as e:
        print(f'An error occurred: {e}')
