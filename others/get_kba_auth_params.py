import base64
import json
import random
import string
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


if __name__ == "__main__":
    k = get_dict_auth_store(7630)
    print(k)
