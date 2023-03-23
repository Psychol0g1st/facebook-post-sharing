import facebook
import sys
import os
from enum import Enum
import requests
from bs4 import BeautifulSoup
from datetime import datetime

PAGE_ID = 466768547214708

class Parameter_type(Enum):
    UNDEFINED = 0
    URL = 1
    FILE = 2

def get_acess_token():
    with open(".access-token", "r") as file:
        access_token = file.read().strip()
    return access_token

def get_parameter_type(arg):
    if os.path.isfile(arg):
        return Parameter_type.FILE
    elif "http" in arg:
        return Parameter_type.URL
    return Parameter_type.UNDEFINED

def post_to_facebook(page_id, message, link):
    access_token = get_acess_token()
    graph = facebook.GraphAPI(access_token)
    graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)

def get_message_template():
    with open("message-template.txt", "r") as file:
        return file.read().strip()

def create_post_message(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    meta = {}
    for tag in soup.find_all("meta"):
        if tag.get("name") or tag.get("property"):
            name = tag.get("name") or tag.get("property")
            value = tag.get("content")
            meta[name] = value

    if len(meta['description']) > 200:
        meta['description'] = meta['description'][:200] + "..."
    template = get_message_template()
    message = template.format(title=meta['og:title'], description=meta['description'], url=url)
    return message

def read_url_from_file(filename):
    with open(filename, "r") as file:
        links = file.readlines()
    links = [link.strip() for link in links if link.strip()]
    return links

if __name__ == "__main__":
    unsuccessful = []

    if len(sys.argv) == 2:
        arg = sys.argv[1]
        type = get_parameter_type(arg)
        if  type == Parameter_type.FILE:
            urls = read_url_from_file(arg)
        elif type == Parameter_type.URL:
            urls = [arg]
        else:
            print("Wrong parameter!")
            exit(1)
        # post urls
        for url in urls:
            try:
                message = create_post_message(url)
                post_to_facebook(PAGE_ID, message, url)
            except Exception as e:
                print(f"Publication error on {url}")
                print(e)
                unsuccessful.append(url)
        if len(unsuccessful) > 0:
            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
            isExist = os.path.exists("./logs")
            if not isExist:
                os.makedirs("./logs")
            with open(f"logs/{dt_string}-unsuccessful-urls.txt", 'w') as f:
                for item in unsuccessful:
                    f.write("%s\n" % item)
        print("Successful publication!")

    else:
        print("No parameters passed!")
        exit(2)



