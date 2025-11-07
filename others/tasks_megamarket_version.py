# tasks
import hashlib
import json
import os
import re
from datetime import (
    date,
)

from celery import (
    current_app as app,
)
# logging
from celery.utils.log import (
    get_task_logger,
)
# scraping
from grab import (
    Grab,
)
#putters
from putter.tasks import (
    put_city,
    put_group,
    put_price,
    put_product,
    put_region,
    put_shop,
)
#decorators
from services.decorators import (
    get_connect,
    get_page,
    get_page14,
    rate_limit,
)
#tools
from services.tools import (
    extract_json_objects,
    search_mera,
)


logger = get_task_logger(__name__)


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
def get_groups14(self, *args, **kwargs):
    # cookies = {'region_id': 50, 'adult_disclaimer_confirmed':1 }
    post = {"parentId":"0","depthLevel":3}
    url = 'https://megamarket.ru/api/mobile/v1/catalogService/catalog/menu'
    get_groups.s(url=url, post=post).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page14()
def get_groups(self, *args, **kwargs):
    '''
    Парсинг групп товаров
    '''
    url = kwargs['url']
    body = kwargs['body']
    print(body)
    driver = kwargs['driver']
    driver.quit()

    base_url = 'https://megamarket.ru'

    js = None
    groups = {}
    groups_out = {}
    try:
        js = json.loads(body)
    except Exception as e:
        logger.error("js not parse from url: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    if js:
        for group in js['nodes']:
            group_id = group['collection']['collectionId']
            group_name = group['collection']['title']
            parent_id = group['collection']['parentId']
            group_url = base_url + group['collection']['url']
            slug = group['collection']['slug']
            groups[group_id] = {'name': group_name, 'parent': parent_id, 'url': group_url}

        groups_out = {}
        for id, category in groups.items():
            if id not in ['15588', '14037', '695654']:
                continue
            parent_id = category['parent']
            if parent_id == '0':
                if id not in groups_out:
                    groups_out[id] = {}

        for id, category in groups.items():
            parent_id = category['parent']
            if parent_id in groups_out:
                if parent_id == '14037' and id not in ['14045', '14040']:
                    continue
                if parent_id == '695654' and id not in ['13218']:
                    continue
                groups_out[parent_id][id] = {}

        for id, category in groups.items():
            parent_id = category['parent']
            for group_id in groups_out:
                if parent_id in groups_out[group_id]:
                    if parent_id == '14045' and id not in ['14097']:
                        continue
                    if parent_id == '14040' and id not in ['14042']:
                        continue
                    if parent_id == '13218' and id not in ['13287']:
                        continue
                    groups_out[group_id][parent_id][id] = {}

        for group_id, group in groups_out.items():
            group1 = groups[group_id]
            put_group.s(14, group1, group_id).apply_async(queue='put')
            for subgroup_id, subgroup in group.items():
                subgroup1 = groups[subgroup_id]
                put_group.s(14, subgroup1, subgroup_id).apply_async(queue='put')
                for subgroup2_id, subgroup2 in subgroup.items():
                    subgroup2 = groups[subgroup2_id]
                    put_group.s(14, subgroup2, subgroup2_id).apply_async(queue='put')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page()
def get_oblast14(self, *args, **kwargs):
    url = kwargs['url']
    grab = kwargs['grab']

    logger.info("Get KB groups from: %s" % url)
    groups = None
    groups_init = None
    try:
        groups = json.loads(grab.doc.body)
    except Exception as e:
        logger.error("groups KB is not a json from %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)
    if groups:
        groups_init = [group['id'] for group in groups if group['selected']]
    get_oblast.s(groups_init).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
def get_oblast(self, groups_init, *args, **kwargs):
    post = {"parentId":"0","depthLevel":3}
    url = 'https://megamarket.ru/api/mobile/v1/catalogService/catalog/menu'
    get_oblast_common.s(groups_init, url=url, post=post).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page14()
def get_oblast_common(self, groups_init, *args, **kwargs):
    '''
    Парсинг товаров
    '''
    url = kwargs['url']
    body = kwargs['body']
    print(body)
    driver = kwargs['driver']
    base_url = 'https://megamarket.ru'

    cookies = {'region_id': 50, 'adult_disclaimer_confirmed':1}
    logger.info("Get groups from: %s" % url)
    try:
        js = json.loads(body)
    except Exception as e:
        logger.error("js not parse from url: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    categories = js['nodes']
    groups = {}

    for category in categories:
        parent_id = category['collection']['parentId']
        id = category['collection']['collectionId']
        if id not in ['15588', '14037', '695654']:
            continue
        if parent_id == '0':
            if id not in groups:
                groups[id] = {}

    for category in categories:
        parent_id = category['collection']['parentId']
        id = category['collection']['collectionId']
        if parent_id in groups:
            if parent_id == '14037' and id not in ['14045', '14040']:
                continue
            if parent_id == '695654' and id not in ['13218']:
                continue
            groups[parent_id][id] = {}

    for category in categories:
        parent_id = category['collection']['parentId']
        id = category['collection']['collectionId']
        for group_id in groups:
            if parent_id in groups[group_id]:
                if parent_id == '14045' and id not in ['14097']:
                    continue
                if parent_id == '14040' and id not in ['14042']:
                    continue
                if parent_id == '13218' and id not in ['13287']:
                    continue
                groups[group_id][parent_id][id] = {}

    url = 'https://megamarket.ru/api/mobile/v1/catalogService/catalog/search'

    for group_id in groups:
        for subgroup_id in groups[group_id]:
            for subgroup2_id in groups[group_id][subgroup_id]:
                #если группа в отмеченных для парсинга
                if subgroup2_id not in groups_init:
                    continue
                if groups[group_id][subgroup_id]:
                    post = {"auth":{"locationId": str(50),"appPlatform":"WEB"}, "requestVersion":10, "limit":44, "offset":0, "ageMore18": 2, "collectionId": subgroup2_id, "showNotAvailable": True }
                    get_products.s(group_id, subgroup_id, subgroup2_id, url=url, post=post).apply_async(queue='work14')
                else:
                    #если группа в отмеченных для парсинга
                    if subgroup_id not in groups_init:
                        continue
                    post = {"auth":{"locationId": str(50),"appPlatform":"WEB"},"requestVersion":10, "limit":44, "offset":0, "ageMore18": 2, "collectionId": subgroup_id, "showNotAvailable": True }
                    get_products.s(group_id, subgroup_id, url=url, post=post).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page14()
def get_products(self, group_id, subgroup_id, subgroup2_id=None, *args, **kwargs):
    url = kwargs['url']
    post = kwargs["post"]
    body = kwargs['body']
    print(body)
    driver = kwargs['driver']

    base_url = 'https://megamarket.ru'
    # cookies = {'region_id': 50, 'adult_disclaimer_confirmed':1 }

    logger.info("Get products for group: %s, subgroup: %s, subgroup2: %s" % (group_id, subgroup_id, subgroup2_id))
    products = {}
    try:
        products = json.loads(body)
    except Exception as e:
        logger.error("products not parse from url: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    if products:
        limit = int(products['limit'])
        offset = int(products['offset'])
        total = int(products['total'])

        items = products['items']
        if items:
            for item in items:
                product_image = None
                if 'isAvailable' in item and item['isAvailable']:
                    product_id = item['goods']['goodsId']
                    product_name = item['goods']['title']
                    product_brand = item['goods']['brand']
                    product_image = item['goods']['titleImage']
                    if not product_image:
                        product_image = 'http://91.233.82.83/comparison/foto/no-product.jpg'
                    product_slug = item['goods']['slug']
                    product_url = item['goods']['webUrl']
                    product_price = item['price']
                    product_price_discount = item['finalPrice']
                    product_last_price = item['lastPrice']
                    if not product_price_discount:
                        product_price_discount = product_last_price
                        product_price = product_last_price

                    meras = search_mera(product_name)
                    product = {}
                    product['image_url'] = product_image
                    product['product_url'] = product_url
                    product['name'] = product_name
                    product['slug'] = product_slug
                    product['price'] = product_price
                    product['price_discount'] = product_price_discount
                    product['group'] = group_id
                    product['subgroup'] = subgroup_id
                    product['subgroup2'] = subgroup2_id
                    if meras['count'] != '':
                        product['quantity'] = meras['count'][0]
                    if meras['weight'] != '':
                        product['mera'] = meras['weight'][0]
                        product['unit'] = meras['weight'][1]
                    if meras['volume'] != '':
                        product['volume'] = ' '.join(meras['volume'])
                        product['mera'] = meras['volume'][0]
                        product['unit'] = meras['volume'][1]
                    if meras['procent'] != '':
                        product['percent'] = ' '.join(meras['procent'])

                    if 'mera' in product and (product['mera'] == ',' or product['mera'] == '.'):
                        product['mera'] = ''
                        product['unit'] = ''
                        product['volume'] = ''
                    put_product.s(14, product, product_id).apply_async(queue='put')

        if not total:
            return
        if offset > 0:
            return

        pages = total / limit
        pages = int(-1 * pages // 1 * -1)
        for page in range(1, pages + 2):
            offset_next = limit * page
            if subgroup2_id is not None:
                post = {"auth":{"locationId": str(50),"appPlatform":"WEB"}, "requestVersion":10, "limit":44, "offset": offset_next, "ageMore18": 2, "collectionId": subgroup2_id, "showNotAvailable": True}
                get_products.s(group_id, subgroup_id, subgroup2_id, url=url, post=post).apply_async(queue='work14')
            else:
                post = {"auth":{"locationId": str(50),"appPlatform":"WEB"}, "requestVersion":10, "limit":44, "offset": offset_next, "ageMore18": 2, "collectionId": subgroup_id, "showNotAvailable": True}
                get_products.s(group_id, subgroup_id, url=url, post=post).apply_async(queue='work14')

        driver.quit()


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
def get_shops14(self, *args, **kwargs):
    post = {"kladrId": None}
    url = 'https://megamarket.ru/api/mobile/v1/regionService/region/search'
    get_shops.s(url=url, post=post).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page14()
def get_shops(self, *args, **kwargs):
    url = kwargs['url']
    body = kwargs['body']
    driver = kwargs['driver']
    driver.quit()

    base_url = 'https://megamarket.ru'
    logger.info("Get shop from: %s" % url)
    try:
        data = json.loads(body)
    except Exception as e:
        logger.error("data not parse from: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    for region in data['regions']:
        region_id = region['id']
        region_slug = region['kladrId']
        region_name = region['dislplayName']
        region1 = {'name': region_name, 'id': region_id, 'slug': region_slug}
        put_region.s(14, region1, region_id).apply_async(queue='put')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_connect()
@get_page()
def get_prices_old(self, region_id, product_id, *args, **kwargs):
    url = kwargs['url']
    grab = kwargs['grab']

    base_url = 'https://sbermegamarket.ru'

    product = {}
    try:
        product = json.loads(grab.doc.body)
    except Exception as e:
        logger.error("product not parse from url: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    date_today = date.today()

    city_id = 0 # Для всех городов
    shop_id = 0 # Для всех магазинов

    price_discount = 0
    price_discounts = []

    for offer in product['offers']:
        price_discounts.append( offer['finalPrice'] )

    if price_discounts:
        price_discount = min(price_discounts)

#    product_id = product['item']['goods']['goodsId']
    price_name = str(region_id) + str(city_id) + str(shop_id) + str(product_id) + str(date_today)
    price_id = hashlib.sha1(price_name.encode("utf-8")).hexdigest()
    price_out = {}
    price_out['id'] = price_id
    price_out['region_id'] = region_id
    price_out['city_id'] = city_id
    price_out['shop_id'] = shop_id
    price_out['product_id'] = product_id
    price_out['price'] = price_discount
    price_out['price_discount'] = price_discount
    if price_discount:
        put_price.s(14, price_out, price_id).apply_async(queue='put')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
def get_prices(self, group_ids, subgroup_ids, subgroup2_ids, products_init, *args, **kwargs):
    url = 'http://kb-base.local/api/competitor14/groups/all/?format=json'
    get_groups_init_s.s(group_ids, subgroup_ids, subgroup2_ids, products_init, url=url).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page()
def get_groups_init_s(self, group_ids, subgroup_ids, subgroup2_ids, products_init, *args, **kwargs):
    url = kwargs['url']
    grab = kwargs['grab']

    logger.info("Get KB groups from: %s" % url)
    groups = None
    groups_init = None
    try:
        groups = json.loads(grab.doc.body)
    except Exception as e:
        logger.error("groups KB is not a json from %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)
    if groups:
        groups_init = [group['id'] for group in groups if group['selected'] and (group['id'] in group_ids or group['id'] in subgroup_ids or group['id'] in subgroup2_ids)]
#        groups_init = [group['id'] for group in groups if group['selected']]
#    groups_init = [group for group in groups_init if group in group_ids or group in subgroup_ids]
    print(groups_init)
    get_regions_init_s.s(products_init, groups_init, url='http://kb-base.local/api/competitor14/comparisons/regions/?format=json').apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page()
def get_regions_init_s(self, products_init, groups_init, *args, **kwargs):
    url = kwargs['url']
    grab = kwargs['grab']

    logger.info("Get comparison regions from: %s" % url)
    comparisons = None
    regions_init = None
    try:
        comparisons = json.loads(grab.doc.body)
    except Exception as e:
        logger.error("cities is not a json from %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)
    if comparisons:
        regions_init = [comparison['comp_id'] for comparison in comparisons]
    post = {"kladrId": None}
    # cookies = {'region_id': 50, 'adult_disclaimer_confirmed':1 }
    url = 'https://megamarket.ru/api/mobile/v1/regionService/region/search'
    get_shops_s.s(products_init, regions_init, groups_init, url=url, post=post).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page14()
def get_shops_s(self, products_init, regions_init, groups_init, *args, **kwargs):
    url = kwargs['url']
    post = kwargs["post"]
    body = kwargs['body']
    driver = kwargs['driver']

    base_url = 'https://megamarket.ru'
    logger.info("Get shop from: %s" % url)
    try:
        data = json.loads(body)
    except Exception as e:
        logger.error("data not parse from: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    for region in data['regions']:
        region_id = region['id']
        if region_id in regions_init:
            # cookies = {'region_id': region_id, 'adult_disclaimer_confirmed':1}
            post = {"parentId":"0","depthLevel":3}
            url = 'https://megamarket.ru/api/mobile/v1/catalogService/catalog/menu'
            get_oblast_common_s.s(region_id, products_init, groups_init, url=url, post=post).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page14()
def get_oblast_common_s(self, region_id, products_init, groups_init, *args, **kwargs):
    '''
    Парсинг товаров
    '''
    url = kwargs['url']
    post = kwargs["post"]
    body = kwargs['body']
    driver = kwargs['driver']

    base_url = 'https://megamarket.ru'
    # cookies = {'region_id': region_id, 'adult_disclaimer_confirmed': 1}
    logger.info("Get groups from: %s" % url)
    try:
        js = json.loads(body)
    except Exception as e:
        logger.error("js not parse from url: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    categories = js['nodes']
    groups = {}

    for category in categories:
        parent_id = category['collection']['parentId']
        id = category['collection']['collectionId']
        if id not in ['15588', '14037', '695654']:
            continue
        if parent_id == '0':
            if id not in groups:
                groups[id] = {}

    for category in categories:
        parent_id = category['collection']['parentId']
        id = category['collection']['collectionId']
        if parent_id in groups:
            if parent_id == '14037' and id not in ['14045', '14040']:
                continue
            if parent_id == '695654' and id not in ['13218']:
                continue
            groups[parent_id][id] = {}

    for category in categories:
        parent_id = category['collection']['parentId']
        id = category['collection']['collectionId']
        for group_id in groups:
            if parent_id in groups[group_id]:
                if parent_id == '14045' and id not in ['14097']:
                    continue
                if parent_id == '14040' and id not in ['14042']:
                    continue
                if parent_id == '13218' and id not in ['13287']:
                    continue
                groups[group_id][parent_id][id] = {}

    url = 'https://megamarket.ru/api/mobile/v1/catalogService/catalog/search'

    for group_id in groups:
        for subgroup_id in groups[group_id]:
            for subgroup2_id in groups[group_id][subgroup_id]:
                #если группа в отмеченных для парсинга
                if subgroup2_id not in groups_init:
                    continue
                if groups[group_id][subgroup_id]:
                    post = {"auth":{"locationId": str(region_id),"appPlatform":"WEB"}, "requestVersion":10, "limit":44, "offset":0, "ageMore18": 2, "collectionId": subgroup2_id, "showNotAvailable": True }
                    get_prices_s.s(region_id, products_init, group_id, subgroup_id, subgroup2_id, url=url, post=post).apply_async(queue='work14')
                else:
                    #если группа в отмеченных для парсинга
                    if subgroup_id not in groups_init:
                        continue
                    post = { "auth":{"locationId": str(region_id),"appPlatform":"WEB"},"requestVersion":10, "limit":44, "offset":0, "ageMore18": 2, "collectionId": subgroup_id, "showNotAvailable": True }
                    get_prices_s.s(region_id, products_init, group_id, subgroup_id, url=url, post=post).apply_async(queue='work14')


@app.task(bind=True, autoretry_for=(Exception,), max_retries=None, ignore_result=True)
@rate_limit('competitor14')
@get_page14()
def get_prices_s(self, region_id, products_init, group_id, subgroup_id, subgroup2_id=None, *args, **kwargs):
    url = kwargs['url']
    post = kwargs["post"]
    body = kwargs['body']
    driver = kwargs['driver']

    base_url = 'https://megamarket.ru'
    # cookies = {'region_id': 50, 'adult_disclaimer_confirmed':1 }

    logger.info("Get products for group: %s, subgroup: %s, subgroup2: %s" % (group_id, subgroup_id, subgroup2_id))
    products = {}
    try:
        products = json.loads(body)
    except Exception as e:
        logger.error("products not parse from url: %s" % url)
        logger.error("%s" % str(e))
        raise self.retry(exc=e, countdown=5)

    if products:
        limit = int(products['limit'])
        offset = int(products['offset'])
        total = int(products['total'])

        items = products['items']
        if items:
            for item in items:
                if 'isAvailable' in item and item['isAvailable']:
                    product_id = str(item['goods']['goodsId'])
                    product_price_discount = None
                    if product_id in products_init:
                        product_price = item['price']
                        product_price_discount = item['priceFrom']
                        product_price_bonus = item['bonusAmount']
                        product_last_price = item['lastPrice']
                        if not product_price_discount:
                            product_price_discount = product_last_price
                            product_price = product_last_price

                        date_today = date.today()
                        city_id = 0 # Для всех городов
                        shop_id = 0 # Для всех магазинов
                        price_name = str(region_id) + str(city_id) + str(shop_id) + str(product_id) + str(date_today)
                        price_id = hashlib.sha1(price_name.encode("utf-8")).hexdigest()
                        price_out = {}
                        price_out['id'] = price_id
                        price_out['region_id'] = region_id
                        price_out['city_id'] = city_id
                        price_out['shop_id'] = shop_id
                        price_out['product_id'] = product_id
                        price_out['price'] = product_price
                        price_out['price_discount'] = product_price_discount - product_price_bonus
                        if product_price_discount:
                            put_price.s(14, price_out, price_id).apply_async(queue='put')


        if offset + limit <= total:
            offset_next = offset + limit
            if subgroup2_id is not None:
                post = {"auth":{"locationId": str(region_id),"appPlatform":"WEB"}, "requestVersion":10, "limit":44, "offset": offset_next, "ageMore18": 2, "collectionId": subgroup2_id, "showNotAvailable": True }
                get_prices_s.s(region_id, products_init, group_id, subgroup_id, subgroup2_id, url=url, post=post).apply_async(queue='work14')
            else:
                post = {"auth":{"locationId": str(region_id),"appPlatform":"WEB"}, "requestVersion":10, "limit":44, "offset": offset_next, "ageMore18": 2, "collectionId": subgroup_id, "showNotAvailable": True }
                get_prices_s.s(region_id, products_init, group_id, subgroup_id, url=url, post=post).apply_async(queue='work14')

        driver.quit()

