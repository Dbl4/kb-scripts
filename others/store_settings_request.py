# import requests
#
# default_settings_data = {
#     "queues_dvr_channel": "12_4",
#     "queues_points": "[[0, 0], [960,0], [960, 540], [0,540], [0, 0]]",
#     "store_id": 90304
# }
#
# response = requests.post(**post_args)



# if __name__ == "__main__":
#     k = get_dict_auth_store(7630)
#     print(k)


test_lst = [5, -1, 2, 0, 4]


for i in range(len(test_lst)):
    min_idx = i
    for j in range(i + 1, len(test_lst)):
        if test_lst[j] < test_lst[min_idx]:
            min_idx = j

    tmp = test_lst[min_idx]
    test_lst[min_idx] = test_lst[i]
    test_lst[i] = tmp

print(test_lst)

YANDEX_API_KEY = 123456

def get_city_coordinates():
    city_name = "Алейск"
    region_name = None
    # if not region_name:
    #     logger.warning(f"Can't find region name for region_id = {data.region_id}")
    coordinates = fetch_city_coordinates(city_name, region_name)


def fetch_city_coordinates(city_name, region_name=None):
    """Получает координаты населенного пункта из геокодера, сохраняет в static_cities_coordinates"""

    if region_name:
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_API_KEY}&geocode={city_name}, {region_name}&format=json&results=1"
    else:
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_API_KEY}&geocode={city_name}&format=json&results=1"

    print(url)


get_city_coordinates()


def insertion_sort(nums):
    for i in range(1, len(nums)):
        insert_item = nums[i]
        j = i - 1

        while j >= 0 and nums[j] > insert_item:
            nums[j + 1] = nums[j]
            j = j - 1

        nums[j + 1] = insert_item


# Проверяем, что оно работает
random_list_of_nums = [9, 1, 15, 28, 6]
insertion_sort(random_list_of_nums)
print(random_list_of_nums)