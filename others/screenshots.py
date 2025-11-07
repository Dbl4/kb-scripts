import base64
import json
import random
import string
from pathlib import WindowsPath

import requests
from datetime import datetime


def get_dict_auth_store(store):

    dict_auth = {}

    try:
        # Numbers
        list_numbers = list(str(int(datetime.timestamp(datetime.now()))
                                * int(str(store))
                                * (int(str(store)[-1]) + 1)))

        # Length
        length_total = 30
        length_numbers = len(list_numbers)

        # Letters
        letters = (string.ascii_letters + string.punctuation)

        # Number positions
        list_pos_numbers = list(random.sample(range(length_total), length_numbers))
        list_pos_numbers.sort()

        # Result
        list_res = []
        i_number = 0
        for i in range(length_total):
            if i in list_pos_numbers:
                list_res.append(list_numbers[i_number])
                i_number += 1
            else:
                list_res.append(random.choice(letters))
        res = ''.join(list_res)

        dict_auth = {
            'user_id': store,
            'user_group': 'store_server',
            'token': base64.b64encode(res.encode('utf-8-sig')).decode('latin-1'),
        }
    except Exception as e:
        print("Error while executing 'get_dict_auth_store()'. {e}".format(e=e))


    return json.dumps(dict_auth)

def run():
    # url = 'http://tkba.rw.org:1072/api/events/screenshots/'
    url = 'http://localhost:8000/api/events/screenshots/'
    headers = {
        'authorization': get_dict_auth_store(store="768"),
        'content-type': 'application/json'
    }

    post_data = {
        'description': "ntcn test",
        'screenshot_id': 8660151,
        'event_id': 651472095,
    }

    try:
        response = requests.post(url, json=post_data, headers=headers)
        data = json.loads(response.text)
    except Exception as e:
        print(e)


def post_events():

    url = 'http://localhost:8000/api/events/events_nested/'
    headers = {
        'authorization': get_dict_auth_store(store="768"),
        'content-type': 'application/json'
    }

    post_data = {
        'duration': '0.14598571666666665',
        'end_at': '2025-07-09 15:20:52',
        'is_manual': True,
        'name': 'Доступ к товарам затруднен на 23%. ',
        'scenario_id': {
            'name': 'store_mess',
            'project_id': {'name': 'merchandising'}
        },
        'start_at': '2025-07-09 15:20:43',
        'store_id': {'name': '768'}
    }

    try:
        response = requests.post(url, json=post_data, headers=headers)
        data = json.loads(response.text)
    except Exception as e:
        print(e)


def post_image_info_to_cctv_screenshots():

    '''Отправка информации о фотографии хлама в бэкенд КБА'''

    url = 'http://localhost:8000/api/data_storage/cctv_screenshots/'
    headers = {
        'authorization': get_dict_auth_store(store="768"),
    }

    # filename = mess_data['image_filename']
    file_path = '/home/user/Рабочий стол/общая/768_12_10_1752135979.jpg'

    post_data = {'datetime': '2025-07-10 11:46:28',
                 'dvr_channel': '10',
                 'store_id': 764
                 }

    dict_file = {
        'file': open(file_path, 'rb'),
    }

    response = requests.post(url, data=post_data, files=dict_file, headers=headers)
    data = json.loads(response.text)
    print(f'POST TO CCTV_SCREENSHOTS file_path: {file_path}')
    screenshot_id = data.get('id')
    print(screenshot_id)
    return data.get('id')


if __name__ == '__main__':
    # run()
    # post_events()
    post_image_info_to_cctv_screenshots()
    print(get_dict_auth_store('768'))
