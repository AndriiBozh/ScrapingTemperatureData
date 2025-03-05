import os.path
from datetime import datetime

import requests as re
from selectorlib import Extractor
import dotenv

import matplotlib.pyplot as plt

request_url = dotenv.get_key('.env', 'REQUEST_URL')


def get_html_page_str(website_url):
    resp = re.get(website_url)
    resp_txt = resp.text
    return resp_txt


def get_temperature(html_page_str):
    e = Extractor.from_yaml_file('selectors.yaml')
    # 'data' is a dictionary, its key ('temperature') is specified in 'selectors.yaml' file
    data = e.extract(html_page_str)
    temp = data['temperature']
    return temp


def get_current_time():
    current_time = datetime.now().isoformat(' ', timespec='seconds')
    return current_time


def format_data_for_txt_file(time, tem):
    return f'{time}, {tem}'


def check_file_exists(filename):
    path = f'./{filename}'
    return os.path.exists(path)


def create_empty_file(filename):
    try:
        open(filename, 'a').close()
    except Exception as e:
        print('Error occurred! ', e)


def write_data_to_file(data, filename):
    try:
        with open(filename, 'a') as file:
            file.write(data + '\n')
            print('Data was added.')
    except Exception as e:
        print('Error occurred! ', e)


html_page_txt = get_html_page_str(request_url)
temperature = get_temperature(html_page_txt)
date_time = get_current_time()
formatted_str = format_data_for_txt_file(date_time, temperature)

file_name = 'temperature.txt'

file_exists = check_file_exists(file_name)

# if file does not exist, create it
if not file_exists:
    create_empty_file(file_name)

write_data_to_file(formatted_str, file_name)


def get_data_from_file(filename):
    try:
        with open(filename) as file:
            txt = file.read()
            return txt
    except Exception as e:
        print('Error occurred! ', e)


data_str = get_data_from_file(file_name)
data_lst = data_str.split('\n')
# since we have a '\n' new string character after each line, the '\n' after
# a last line gives us an empty string, so
# remove the last element (empty string)
data_lst.pop()


# extract the dates and temperatures into separate lists

def make_separate_lists(lst):
    dts = []
    temps = []
    for el in data_lst:
        res = el.split(',')
        # get date without time (first 10 elements)
        dts.append(res[0][:10])
        # convert string to number
        temps.append(float(res[1]))
    return [dts, temps]


dates = make_separate_lists(data_lst)[0]
temperatures = make_separate_lists(data_lst)[1]

fig, ax = plt.subplots()
# marker adds markers for each data point
ax.plot(dates, temperatures, marker='o')

ax.set_xlabel('Date')
ax.set_ylabel('Temperature')
plt.xticks(rotation=45) # rotate x tick labels for readability
plt.tight_layout()  # adjust layout to prevent overlap
plt.show()
