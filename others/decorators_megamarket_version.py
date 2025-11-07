# coding: utf8

import hashlib
import json
import random
import string
import time
import uuid
from functools import (
    wraps,
)
from queue import (
    Empty,
)
from urllib.parse import (
    urlparse,
)

import requests
from billiard import (
    current_process,
)
from celery import (
    current_app as app,
)
from celery.exceptions import (
    Ignore,
    Reject,
)
from celery.task.control import (
    revoke,
)
# logging
from celery.utils.log import (
    get_task_logger,
)
from grab import (
    Grab,
)
from grab.cookie import (
    CookieManager,
)
from grab.error import (
    GrabNetworkError,
    GrabTimeoutError,
)
from kombu import (
    Queue,
)
from services.redirect import (
    fast_connect,
    gen_cookies_16,
    get_driver_14,
    get_hostname,
    get_post_response_14,
    set_global_driver_to_none,
)
# tools
from services.tools import (
    make_dir,
    rand_string,
)
from urllib3.util import (
    connection,
)


logger = get_task_logger(__name__)


_orig_create_connection = connection.create_connection


def patch_http_connection_pool(**constructor_kwargs):
    from urllib3 import (
        connectionpool,
        poolmanager,
    )

    class MyHTTPConnectionPool(connectionpool.HTTPConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['http'] = MyHTTPConnectionPool


def patch_https_connection_pool(**constructor_kwargs):
    from urllib3 import (
        connectionpool,
        poolmanager,
    )

    class MyHTTPSConnectionPool(connectionpool.HTTPSConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPSConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['https'] = MyHTTPSConnectionPool


#def gen_cookies_16():
#    aa = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
#    a = random.choice(string.ascii_letters)
#    return {'aa': aa, 'a': a}

def get_sessionId():
    randomInts = [random.randrange(10,99) for _ in range(10)]
    randomStrings = [str(x) for x in randomInts]
    strings = ''.join(randomStrings)
    return strings[:-1]


def get_uuid():
    return uuid.uuid4()


def get_city_info():
    city_info = {"slug":"","name":"","lat":0,"lon":0}
    return json.dumps(city_info)


@app.task(ignore_result=True)
def token(connect=None):
    '''
    Задача, хранящая коннект
    '''
    return connect


@app.task(ignore_result=True)
def token_cookies(cookies=None, connect=None):
    '''
    Задача, хранящая кукис
    '''
    return cookies


@app.task(ignore_result=True)
def token_cookies_16(cookies=None):
    '''
    Задача, хранящая кукис
    '''
    return cookies


def rate_limit(task_group):
    '''
    Декоратор для ограничения доступа к сайту (rate limit)
    task_group - имя
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            with self.app.connection_for_read() as conn:
                with conn.SimpleQueue(task_group+'_tokens', no_ack=True, queue_opts={'max_length':2}) as queue:
                    try:
                        queue.get(block=True, timeout=3)
#                        queue.get(block=True)
                        return func(self, *args, **kwargs)
                    except Empty:
                        self.retry(countdown=1)
        return function
    return decorator_func

#def rate_limit(task_group):
#    '''
#    Декоратор для ограничения доступа к сайту (rate limit)
#    task_group - имя
#    '''
#    def decorator_func(func):
#        @wraps(func)
#        def function(self, *args, **kwargs):
#            with self.app.connection_for_read() as conn:
#                msg = conn.default_channel.basic_get(task_group+'_tokens', no_ack=True, queue_opts={'max_length':2})
#                if msg is None:
#                    self.retry(countdown=1)
#                return func(self, *args, **kwargs)
#        return function
#    return decorator_func


def get_cookies10():
    '''
    Декоратор для получения кукиса для competitior10 из очереди
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            worker_hostname = self.app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            worker_shops = self.app.conf.get_by_parts("KB", "WORKER_SHOPS")
            url = kwargs['url']
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            with self.app.connection_for_read() as conn:
                with conn.SimpleQueue(worker_hostname + '_' + hostname_id + '_tokens_cookies10', no_ack=True) as queue:
                    try:
                        msg = queue.get(block=False)
                        task_payload = msg.payload
                        task_kwargs = task_payload[1]
                        try:
                            cookies = task_kwargs['cookies']
                            connect = task_kwargs['connect']
                            logger.error('cookies from queue: %s' % cookies)
                            logger.error('connect from queue: %s' % connect)
                        except:
                            raise Empty
                        kwargs['cookies'] = cookies
                        kwargs['connect'] = connect
                        return func(self, *args, **kwargs)

                    except Empty:
                        connect = kwargs['connect']

                        cookies = None
                        url_init = 'https://lenta.com/catalog/myaso-ptica-kolbasa/'
                        grab = Grab()
                        if connect:
                            grab.setup(connect=connect)
                        grab.go(url_init)
                        cookies_init = grab.cookies.get_dict()
                        try:
                            cookies = kwargs['cookies']
                            for cookie in cookies_init:
                                cookies[cookie['name']] = cookie['value']
                            for cookie in kwargs['cookies']:
                                cookies[cookie['name']] = cookie['value']
                        except:
                            cookies = {}
                            for cookie in cookies_init:
                                cookies[cookie['name']] = cookie['value']

                        if cookies:
                            logger.error('cookies from @get_cookies: %s' % cookies)
                            logger.error('connect from @get_cookies: %s' % connect)
                            kwargs['connect'] = connect
                            kwargs['cookies'] = cookies

                            return func(self, *args, **kwargs)
                        else:
                            if 'connect' in kwargs:
                                del kwargs['connect']
                            if 'cookies' in kwargs:
                                del kwargs['cookies']

                            self.retry(countdown=1, kwargs=kwargs)
        return function
    return decorator_func


def get_cookies03():
    '''
    Декоратор для получения cookies и headers для competitor03
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            cookies = {'mg_foradult': 'true'}
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
                'x-platform-version': 'window.navigator.userAgent',
                'x-device-id': 'nu3kd9367h',
                'x-device-tag': 'disabled',
                'x-app-version': '0.1.0',
                'x-device-platform': 'Web',
                'x-client-name': 'magnit',
            }
            kwargs['cookies'] = cookies
            kwargs['headers'] = headers

            return func(self, *args, **kwargs)

        return function
    return decorator_func


def get_page():
    '''
    Декоратор для скачивания странички
    kwargs['url'] - урл для скачивания
    kwargs['connect'] - коннект
    kwargs['post'] - параметры для POST запроса
    kwargs['cookies'] - параметры для cookies
    kwargs['connect_timeout'] - параметр connect_timeout
    kwargs['timeout'] - параметр timeout
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            grab_debug = app.conf.get_by_parts("KB", "WORKER_GRAB_DEBUG")
            worker_hostname = app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            if grab_debug:
                procces_index = current_process().index
                path = 'log/' + worker_hostname + '/' + str(procces_index)
                make_dir(path)
            try:
                url = kwargs['url']
            except KeyError:
                url = None
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            try:
                ignore = kwargs['ignore']
            except KeyError:
                ignore = False
            try:
                timeout = kwargs['timeout']
            except KeyError:
                timeout = 90
            try:
                connect_timeout = kwargs['connect_timeout']
            except KeyError:
                connect_timeout = 120
            try:
                connect = kwargs['connect']
                print(connect)
            except:
                connect = None
            try:
                post = kwargs['post']
            except KeyError:
                post = None
            try:
                referer = kwargs['referer']
            except KeyError:
                referer = None
            try:
                charset = kwargs['charset']
            except KeyError:
                charset = None
            try:
                headers = kwargs['headers']
            except KeyError:
                headers = None
            try:
                cookies = kwargs['cookies']
            except KeyError:
                cookies = None
            try:
                user_agent = kwargs['user_agent']
            except KeyError:
                user_agent = None
            try:
                reuse_cookies = kwargs['reuse_cookies']
            except KeyError:
                reuse_cookies = None

            grab = Grab()

            if grab_debug:
                grab.setup(log_dir=path) #
                grab.setup(debug=True) #
            if reuse_cookies:
                grab.setup(reuse_cookies=reuse_cookies)
            if connect_timeout:
                grab.setup(connect_timeout=connect_timeout)
            if timeout:
                grab.setup(timeout=timeout)
            if connect:
                grab.setup(connect=connect)
            if headers:
                grab.setup(headers=headers)
            if post:
                grab.setup(post=post)
            if referer:
                grab.setup(referer=referer)
            if charset:
                grab.setup(charset=charset)
            if user_agent:
                grab.setup(user_agent=user_agent)
            if cookies:
                if isinstance(cookies, list):
                    manager = CookieManager()
                    for item in cookies:
                        extra = dict((x, y) for x, y in item.items()
                                     if x not in ['name', 'value', 'domain'])
                        manager.set(item['name'], item['value'], item['domain'], **extra)
                    grab.cookies = manager
                else:
                    grab.setup(cookies=cookies)


            try:
                grab.go(url)
            except GrabNetworkError as e:
                logger.error("GrabNetworkError in task id %s, retries: %s" % (self.request.id, self.request.retries))
                logger.error("%s" % str(e))
                if 'GrabNetworkError' in kwargs:
                    if kwargs['GrabNetworkError'] >= 3:
                        revoke(self.request.id)
                        logger.error("Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabNetworkError'] += 1
                else:
                    kwargs['GrabNetworkError'] = 1
                if 'connect' in kwargs:
                    del kwargs['connect']
#                self.retry(countdown=1, kwargs=kwargs)
            except GrabTimeoutError as e:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabTimeoutError in task id %s, set countdown: %s" % (self.request.id, 1))
                logger.error("%s" % str(e))
#                self.retry(countdown=1)
            except Exception as e:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("Decorator don't grab from: %s" % url)
                logger.error("%s" % str(e))
#                self.retry(countdown=1)
#            print(grab.doc.body)

            if 'megamarket' in url:
                if grab.doc.body and (b'8 800 600-08-88' in grab.doc.body or b'403 Forbidden' in grab.doc.body):
                    grab.doc.code = 405

            if grab.doc.code and grab.doc.code < 400:

                kwargs['grab'] = grab
                if grab.doc.headers and grab.doc.headers['Connection'] != 'close':
                    if 'connect' in kwargs and kwargs['connect']:
                        token.s(connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens',
                                                             kwargs={'connect': connect})

                if 'connect' in kwargs:
                    print(connect, 'connect*')
                    del kwargs['connect']

                return func(self, *args, **kwargs)
            elif grab.doc.code and grab.doc.code == 404:
                if grab.doc.headers and grab.doc.headers['Connection'] and grab.doc.headers['Connection'] != 'close':
                    if 'connect' in kwargs and kwargs['connect']:
                        token.s(connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens', kwargs={'connect': connect})
                if 'connect' in kwargs:
                    del kwargs['connect']

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 3:
                        if not ignore:
                            revoke(self.request.id)
                        logger.error("GrabDocCode 404, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1

#                logger.error("GrabDocCode 404, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
#                revoke(self.request.id)
            elif grab.doc.code and grab.doc.code == 403:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabDocCode 403, Task %s is retried, %s retries" % (self.request.id, self.request.retries))

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 3:
                        if not ignore:
                            revoke(self.request.id)
                        logger.error("GrabDocCode 403, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1
                self.retry(countdown=1, kwargs=kwargs)
            elif grab.doc.code and grab.doc.code >= 400 and grab.doc.code not in [403,404]:
                if 'connect' in kwargs:
                    del kwargs['connect']

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 3:
                        if not ignore:
                            revoke(self.request.id)
                        logger.error("GrabDocCode, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1

                self.retry(countdown=1, kwargs=kwargs)
            else:
                self.retry(countdown=1, kwargs=kwargs)
        return function
    return decorator_func


def get_page01():
    '''
    Декоратор для скачивания странички
    kwargs['url'] - урл для скачивания
    kwargs['connect'] - коннект
    kwargs['post'] - параметры для POST запроса
    kwargs['cookies'] - параметры для cookies
    kwargs['connect_timeout'] - параметр connect_timeout
    kwargs['timeout'] - параметр timeout
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            grab_debug = app.conf.get_by_parts("KB", "WORKER_GRAB_DEBUG")
            worker_hostname = app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            if grab_debug:
                procces_index = current_process().index
                path = 'log/' + worker_hostname + '/' + str(procces_index)
                make_dir(path)
            try:
                url = kwargs['url']
            except KeyError:
                url = None
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            try:
                ignore = kwargs['ignore']
            except KeyError:
                ignore = False
            try:
                timeout = kwargs['timeout']
            except KeyError:
                timeout = 90
            try:
                connect_timeout = kwargs['connect_timeout']
            except KeyError:
                connect_timeout = 120
            try:
                connect = kwargs['connect']
                print(connect)
            except:
                connect = None
            try:
                post = kwargs['post']
            except KeyError:
                post = None
            try:
                referer = kwargs['referer']
            except KeyError:
                referer = None
            try:
                charset = kwargs['charset']
            except KeyError:
                charset = None
            try:
                headers = kwargs['headers']
            except KeyError:
                headers = None
            try:
                cookies = kwargs['cookies']
            except KeyError:
                cookies = None
            try:
                user_agent = kwargs['user_agent']
            except KeyError:
                user_agent = None
            try:
                reuse_cookies = kwargs['reuse_cookies']
            except KeyError:
                reuse_cookies = None

            grab = Grab()

            if grab_debug:
                grab.setup(log_dir=path) #
                grab.setup(debug=True) #
            if reuse_cookies:
                grab.setup(reuse_cookies=reuse_cookies)
            if connect_timeout:
                grab.setup(connect_timeout=connect_timeout)
            if timeout:
                grab.setup(timeout=timeout)
            if connect:
                grab.setup(connect=connect)
            if headers:
                grab.setup(headers=headers)
            if post:
                grab.setup(post=post)
            if referer:
                grab.setup(referer=referer)
            if charset:
                grab.setup(charset=charset)
            if user_agent:
                grab.setup(user_agent=user_agent)
            if cookies:
                if isinstance(cookies, list):
                    manager = CookieManager()
                    for item in cookies:
                        extra = dict((x, y) for x, y in item.items()
                                     if x not in ['name', 'value', 'domain'])
                        manager.set(item['name'], item['value'], item['domain'], **extra)
                    grab.cookies = manager
                else:
                    grab.setup(cookies=cookies)


            try:
                grab.go(url)
            except GrabNetworkError as e:
                logger.error("GrabNetworkError in task id %s, retries: %s" % (self.request.id, self.request.retries))
                logger.error("%s" % str(e))
                if 'GrabNetworkError' in kwargs:
                    if kwargs['GrabNetworkError'] >= 8:
                        revoke(self.request.id)
                        logger.error("Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabNetworkError'] += 1
                else:
                    kwargs['GrabNetworkError'] = 1
#                self.retry(countdown=1, kwargs=kwargs)
            except GrabTimeoutError as e:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabTimeoutError in task id %s, set countdown: %s" % (self.request.id, 1))
                logger.error("%s" % str(e))
#                self.retry(countdown=1)
            except Exception as e:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("Decorator don't grab from: %s" % url)
                logger.error("%s" % str(e))
#                self.retry(countdown=1)
#            print(grab.doc.body)

            if 'sbermegamarket' in url:
                if grab.doc.body and (b'8 800 600-08-88' in grab.doc.body or b'403 Forbidden' in grab.doc.body):
                    grab.doc.code = 405

            if grab.doc.code and grab.doc.code < 400:

                kwargs['grab'] = grab
                if grab.doc.headers and grab.doc.headers['Connection'] != 'close':
                    if 'connect' in kwargs and kwargs['connect']:
                        token.s(connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens',
                                                             kwargs={'connect': connect})

                return func(self, *args, **kwargs)
            elif grab.doc.code and grab.doc.code == 404:
                if grab.doc.headers and grab.doc.headers['Connection'] and grab.doc.headers['Connection'] != 'close':
                    if 'connect' in kwargs and kwargs['connect']:
                        token.s(connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens', kwargs={'connect': connect})

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 6:
                        if not ignore:
                            revoke(self.request.id)
                        logger.error("GrabDocCode 404, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1

#                logger.error("GrabDocCode 404, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
#                revoke(self.request.id)
            elif grab.doc.code and grab.doc.code == 403:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabDocCode 403, Task %s is retried, %s retries" % (self.request.id, self.request.retries))

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 6:
                        if not ignore:
                            revoke(self.request.id)
                        logger.error("GrabDocCode 403, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1
                self.retry(countdown=1, kwargs=kwargs)
            elif grab.doc.code and grab.doc.code >= 400 and grab.doc.code not in [403,404]:

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 6:
                        if not ignore:
                            revoke(self.request.id)
                        logger.error("GrabDocCode, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1

                self.retry(countdown=1, kwargs=kwargs)
            else:
                self.retry(countdown=1, kwargs=kwargs)
        return function
    return decorator_func


def get_page03():
    '''
    Декоратор для скачивания странички
    kwargs['url'] - урл для скачивания
    kwargs['connect'] - коннект
    kwargs['post'] - параметры для POST запроса
    kwargs['cookies'] - параметры для cookies
    kwargs['connect_timeout'] - параметр connect_timeout
    kwargs['timeout'] - параметр timeout
    '''

    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):

            try:
                print(kwargs['connect'])
                connect = kwargs['connect']
            except KeyError:
                connect = None

            def patched_create_connection(address, *args, **kwargs):
                if 'connect' in locals():
                    _, _, host, port = connect[0].split(':')
                else:
                    host, port = address
                return _orig_create_connection((host, port), *args, **kwargs)

            if connect:
                connection.create_connection = patched_create_connection
            else:
                connection.create_connection = _orig_create_connection

            patch_http_connection_pool(maxsize=32, retries=9)
            patch_https_connection_pool(maxsize=32, retries=9)

            try:
                url = kwargs['url']
                parse = urlparse(url)
            except KeyError:
                url = None
                parse = None
                logger.error("Url is None, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                revoke(self.request.id)

            try:
                ignore = kwargs['ignore']
            except KeyError:
                ignore = False

            # cookies
            try:
                cookies = kwargs['cookies']
                cookies = {str(key): str(val) for key, val in cookies.items()}
            except KeyError:
                cookies = None

            # headers
            try:
                headers = kwargs['headers']
            except KeyError:
                headers = None

            # json
            try:
                json = kwargs['json']
            except KeyError:
                json = None

                # params
            try:
                params = kwargs['params']
            except KeyError:
                params = None

            # post
            try:
                post = kwargs['post']
            except KeyError:
                post = None

            if not json:
                try:
                    if params:
                        handle = requests.get(url, cookies=cookies, headers=headers, params=params)
                    else:
                        handle = requests.get(url, cookies=cookies, headers=headers)
                except Exception as e:
                    handle = None
                    if connect and 'connect' in kwargs:
                        del kwargs['connect']
                    logger.error("GET Decorator don't get from: %s" % url)
                    logger.error("%s" % str(e), exc_info=True)
                    if 'RequestsError' in kwargs:
                        if kwargs['RequestsError'] >= 5:
                            revoke(self.request.id)
                            logger.error("RequestsError, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                        else:
                            kwargs['RequestsError'] += 1
                    else:
                        kwargs['RequestsError'] = 1
            else:
                try:
                    if json and not params:
                        handle = requests.post(url, cookies=cookies, headers=headers, json=json)
                    else:
                        handle = requests.post(url, cookies=cookies, headers=headers, params=params, json=json)
                except Exception as e:
                    handle = None
                    if connect and 'connect' in kwargs:
                        del kwargs['connect']
                    logger.error("POST Decorator don't get from: %s" % url)
                    logger.error("%s" % str(e), exc_info=True)
                    if 'RequestsError' in kwargs:
                        if kwargs['RequestsError'] >= 3:
                            revoke(self.request.id)
                            logger.error("RequestsError, Task %s is revoked, %s retries" % (self.request.id, self.request.retries))
                        else:
                            kwargs['RequestsError'] += 1
                    else:
                        kwargs['RequestsError'] = 1

            if handle is None:
                if 'connect' in kwargs:
                    del kwargs['connect']
                self.retry(countdown=1, kwargs=kwargs)

            try:
                status_code = handle.status_code
            except:
                if 'connect' in kwargs:
                    del kwargs['connect']
                self.retry(countdown=1, kwargs=kwargs)

            if status_code == 200:
                kwargs['handle'] = handle
                return func(self, *args, **kwargs)
            else:
                if 'connect' in kwargs:
                    del kwargs['connect']
                if 'RequestsError' in kwargs:
                    if kwargs['RequestsError'] >= 5:
                        revoke(self.request.id)
                        logger.error("RequestsError %s, Task %s is revoked, %s retries" % (status_code, self.request.id, self.request.retries))
                    else:
                        kwargs['RequestsError'] += 1
                else:
                    kwargs['RequestsError'] = 1
                logger.error("RequestsError %s, Task %s, retries %s " % (status_code, self.request.id, self.request.retries))
                logger.error('%s' % handle.content )
                if kwargs['RequestsError'] < 5:
                    logger.error('RequestsError: %s' % kwargs['RequestsError'])
                    self.retry(countdown=1, kwargs=kwargs)

        return function

    return decorator_func


def get_page10():
    '''
    Декоратор для скачивания странички
    kwargs['url'] - урл для скачивания
    kwargs['connect'] - коннект
    kwargs['post'] - параметры для POST запроса
    kwargs['cookies'] - параметры для cookies
    kwargs['connect_timeout'] - параметр connect_timeout
    kwargs['timeout'] - параметр timeout
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            grab_debug = app.conf.get_by_parts("KB", "WORKER_GRAB_DEBUG")
            worker_hostname = app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            if grab_debug:
                procces_index = current_process().index
                path = 'log/' + worker_hostname + '/' + str(procces_index)
                make_dir(path)
            try:
                url = kwargs['url']
            except KeyError:
                url = None
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            try:
                timeout = kwargs['timeout']
            except KeyError:
                timeout = 90
            try:
                connect_timeout = kwargs['connect_timeout']
            except KeyError:
                connect_timeout = 120
            try:
                connect = kwargs['connect']
            except:
                connect = None
            try:
                post = kwargs['post']
            except KeyError:
                post = None
            try:
                referer = kwargs['referer']
            except KeyError:
                referer = None
            try:
                charset = kwargs['charset']
            except KeyError:
                charset = None
            try:
                headers = kwargs['headers']
            except KeyError:
                headers = None

            try:
                cookies = kwargs['cookies']
            except KeyError:
                cookies = None

            try:
                user_agent = kwargs['user_agent']
            except KeyError:
                user_agent = None
            try:
                reuse_cookies = kwargs['reuse_cookies']
            except KeyError:
                reuse_cookies = None

            grab = Grab()
            if grab_debug:
                grab.setup(log_dir=path) #
                grab.setup(debug=True) #
            if reuse_cookies:
                grab.setup(reuse_cookies=reuse_cookies)
            if connect_timeout:
                grab.setup(connect_timeout=connect_timeout)
            if timeout:
                grab.setup(timeout=timeout)
            if connect:
                grab.setup(connect=connect)
            if headers:
                grab.setup(headers=headers)
            if post:
                grab.setup(post=post)
            if referer:
                grab.setup(referer=referer)
            if charset:
                grab.setup(charset=charset)
            if user_agent:
                grab.setup(user_agent=user_agent)
            if cookies:
                if isinstance(cookies, list):
                    manager = CookieManager()
                    for item in cookies:
                        extra = dict((x, y) for x, y in item.items()
                                     if x not in ['name', 'value', 'domain'])
                        manager.set(item['name'], item['value'], item['domain'], **extra)
                    grab.cookies = manager
                else:
                    grab.setup(cookies=cookies)

            try:
                grab.go(url)
            except Exception as e:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabError, url %s. Task %s is retried, %s retries" % (url, self.request.id, self.request.retries))
                logger.error("%s" % str(e))

            if grab.doc.code and grab.doc.code < 400:
#                if 'connect' in kwargs and kwargs['connect']:
#                    token.s(connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens', kwargs={'connect': connect})
                if 'cookies' in kwargs and kwargs['cookies']:
                    token_cookies.s(cookies=cookies, connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens_cookies10', kwargs={'cookies': cookies, 'connect':connect })
                if 'connect' in kwargs:
                    del kwargs['connect']
                if 'cookies' in kwargs:
                    del kwargs['cookies']
                kwargs['grab'] = grab
                return func(self, *args, **kwargs)
            else:
                if 'connect' in kwargs:
                    del kwargs['connect']
                if 'cookies' in kwargs:
                    del kwargs['cookies']
                logger.error("GrabDocCode, Task %s is retried, %s retries" % (self.request.id, self.request.retries))

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 3:
                        kwargs['grab'] = grab
                        return func(self, *args, **kwargs)
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1

                self.retry(countdown=1, kwargs=kwargs)
        return function
    return decorator_func


def get_connect():
    '''
    Декоратор для получения коннекта из очереди
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            worker_hostname = self.app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            worker_shops = self.app.conf.get_by_parts("KB", "WORKER_SHOPS")
            url = kwargs['url']
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            with self.app.connection_for_read() as conn:
                with conn.SimpleQueue(worker_hostname + '_' + hostname_id + '_tokens', no_ack=True) as queue:
                    connects = connect = None
                    try:
#                        msg = queue.get(block=False, timeout=3)
                        msg = queue.get(block=False)
                        task_payload = msg.payload
                        task_kwargs = task_payload[1]
                        try:
                            connect = task_kwargs['connect']
                        except:
                            raise Empty
                        if connect:
                            kwargs['connect'] = connect
                        else:
                             raise Empty
                        return func(self, *args, **kwargs)
                    except Empty:
                        connects = fast_connect(worker_shops, url)
                        if connects:
                            logger.error("connects created")
                            for conn in connects:
                                token.s(connect=conn).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens', kwargs={'connect': conn})
                            self.retry(countdown=1, kwargs=kwargs)
                        return func(self, *args, **kwargs)
        return function
    return decorator_func


def get_cookies_16():
    '''
    Декоратор для получения кукиса для competitior16 из очереди
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            worker_hostname = self.app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            worker_shops = self.app.conf.get_by_parts("KB", "WORKER_SHOPS")
            url = kwargs['url']
            referer = kwargs['referer']
            cookies = None
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            with self.app.connection_for_read() as conn:
                with conn.SimpleQueue(worker_hostname + '_' + hostname_id + '_tokens_cookies_16', no_ack=True) as queue:
                    try:
                        msg = queue.get(block=True, timeout=1)
                        task_payload = msg.payload
                        task_kwargs = task_payload[1]
                        try:
                            cookies = task_kwargs['cookies']
                            logger.error('cookies from queue: %s' % cookies)
                        except:
                            raise Empty
                        kwargs['cookies'] = cookies
                        return func(self, *args, **kwargs)
                    except Empty:
                        connect = kwargs['connect']
                        cookies = gen_cookies_16(connect, url, referer)
                        logger.error('cookies from create: %s' % cookies)
                        kwargs['cookies'] = cookies
                        return func(self, *args, **kwargs)
        return function
    return decorator_func


def get_page16():
    '''
    Декоратор для скачивания странички
    kwargs['url'] - урл для скачивания
    kwargs['connect'] - коннект
    kwargs['post'] - параметры для POST запроса
    kwargs['cookies'] - параметры для cookies
    kwargs['connect_timeout'] - параметр connect_timeout
    kwargs['timeout'] - параметр timeout
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            grab_debug = app.conf.get_by_parts("KB", "WORKER_GRAB_DEBUG")
            worker_hostname = app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            if grab_debug:
                procces_index = current_process().index
                path = 'log/' + worker_hostname + '/' + str(procces_index)
                make_dir(path)
            try:
                url = kwargs['url']
            except KeyError:
                url = None
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            try:
                timeout = kwargs['timeout']
            except KeyError:
                timeout = 90
            try:
                connect_timeout = kwargs['connect_timeout']
            except KeyError:
                connect_timeout = 120
            try:
                connect = kwargs['connect']
            except:
                connect = None
            try:
                post = kwargs['post']
            except KeyError:
                post = None
            try:
                referer = kwargs['referer']
            except KeyError:
                referer = None
            try:
                charset = kwargs['charset']
            except KeyError:
                charset = None
            try:
                headers = kwargs['headers']
            except KeyError:
                headers = None
            try:
                cookies = kwargs['cookies']
            except KeyError:
                cookies = None
            try:
                user_agent = kwargs['user_agent']
            except KeyError:
                user_agent = None
            try:
                reuse_cookies = kwargs['reuse_cookies']
            except KeyError:
                reuse_cookies = None

            if 'sbermarket.ru/api' in url:
#                cookies = {'user_is_adult': 'true', 'identified_address': 'true', 'sessionId': get_sessionId(), 'cookies_consented': 'yes', 'external_analytics_anonymous_id': get_uuid(), 'city_info': get_city_info(), 'rr-testCookie':'testvalue'}
#                cookies = {'user_is_adult': 'true', 'identified_address': 'true', 'sessionId': get_sessionId(), 'cookies_consented': 'yes', 'external_analytics_anonymous_id': get_uuid(), 'rr-testCookie':'testvalue'}
#                cookies = {'ssrMedia':'', 'rr-testCookie':'testvalue'}
#                cookies = {'cw_conversation':'', 'rr-testCookie':'testvalue'}
                cookies = {'user_is_adult':'true', 'identified_address': 'true', 'cookies_consented': 'yes', 'rr-testCookie':'testvalue', 'citi_info': {}}

            grab = Grab()
            if grab_debug:
                grab.setup(log_dir=path) #
                grab.setup(debug=True) #
            if reuse_cookies:
                grab.setup(reuse_cookies=reuse_cookies)
            if connect_timeout:
                grab.setup(connect_timeout=connect_timeout)
            if timeout:
                grab.setup(timeout=timeout)
            if connect:
                grab.setup(connect=connect)
            if headers:
                grab.setup(headers=headers)
            if post:
                grab.setup(post=post)
            if referer:
                grab.setup(referer=referer)
            if charset:
                grab.setup(charset=charset)
            if user_agent:
                grab.setup(user_agent=user_agent)
            if cookies:
                if isinstance(cookies, list):
                    manager = CookieManager()
                    for item in cookies:
                        extra = dict((x, y) for x, y in item.items()
                                     if x not in ['name', 'value', 'domain'])
                        manager.set(item['name'], item['value'], item['domain'], **extra)
                    grab.cookies = manager
                else:
                    grab.setup(cookies=cookies)

            try:
                grab.go(url)
            except Exception as e:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabError, url %s. Task %s is retried, %s retries" % (url, self.request.id, self.request.retries))
                logger.error("%s" % str(e))


            if grab.doc.code and grab.doc.code < 400:
                if 'connect' in kwargs and kwargs['connect']:
                    token.s(connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens', kwargs={'connect': connect})
                if 'connect' in kwargs:
                    del kwargs['connect']
                kwargs['grab'] = grab
                return func(self, *args, **kwargs)
            else:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabDocCode, Task %s is retried, %s retries" % (self.request.id, self.request.retries))

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 3:
                        kwargs['grab'] = grab
                        return func(self, *args, **kwargs)
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1
                self.retry(countdown=1, kwargs=kwargs)
        return function
    return decorator_func


def get_page30():
    '''
    Декоратор для скачивания странички
    kwargs['url'] - урл для скачивания
    kwargs['connect'] - коннект
    kwargs['post'] - параметры для POST запроса
    kwargs['cookies'] - параметры для cookies
    kwargs['connect_timeout'] - параметр connect_timeout
    kwargs['timeout'] - параметр timeout
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            grab_debug = app.conf.get_by_parts("KB", "WORKER_GRAB_DEBUG")
            worker_hostname = app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            if grab_debug:
                procces_index = current_process().index
                path = 'log/' + worker_hostname + '/' + str(procces_index)
                make_dir(path)
            try:
                url = kwargs['url']
            except KeyError:
                url = None
            hostname = get_hostname(url)
            hostname_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()
            try:
                timeout = kwargs['timeout']
            except KeyError:
                timeout = 90
            try:
                connect_timeout = kwargs['connect_timeout']
            except KeyError:
                connect_timeout = 120
            try:
                connect = kwargs['connect']
            except:
                connect = None
            try:
                post = kwargs['post']
            except KeyError:
                post = None
            try:
                referer = kwargs['referer']
            except KeyError:
                referer = None
            try:
                charset = kwargs['charset']
            except KeyError:
                charset = None
            try:
                headers = kwargs['headers']
            except KeyError:
                headers = None

            try:
                cookies = kwargs['cookies']
            except KeyError:
                cookies = None

            try:
                user_agent = kwargs['user_agent']
            except KeyError:
                user_agent = None
            try:
                reuse_cookies = kwargs['reuse_cookies']
            except KeyError:
                reuse_cookies = None

            grab = Grab()
            if grab_debug:
                grab.setup(log_dir=path) #
                grab.setup(debug=True) #
            if reuse_cookies:
                grab.setup(reuse_cookies=reuse_cookies)
            if connect_timeout:
                grab.setup(connect_timeout=connect_timeout)
            if timeout:
                grab.setup(timeout=timeout)
            if connect:
                grab.setup(connect=connect)
            if headers:
                grab.setup(headers=headers)
            if post:
                grab.setup(post=post)
            if referer:
                grab.setup(referer=referer)
            if charset:
                grab.setup(charset=charset)
            if user_agent:
                grab.setup(user_agent=user_agent)
            if cookies:
                if isinstance(cookies, list):
                    manager = CookieManager()
                    for item in cookies:
                        extra = dict((x, y) for x, y in item.items()
                                     if x not in ['name', 'value', 'domain'])
                        manager.set(item['name'], item['value'], item['domain'], **extra)
                    grab.cookies = manager
                else:
                    grab.setup(cookies=cookies)

            try:
                grab.go(url)
            except Exception as e:
                if 'connect' in kwargs:
                    del kwargs['connect']
                logger.error("GrabError, url %s. Task %s is retried, %s retries" % (url, self.request.id, self.request.retries))
                logger.error("%s" % str(e))

            if grab.doc.code and grab.doc.code < 400:
#                if 'connect' in kwargs and kwargs['connect']:
#                    token.s(connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens', kwargs={'connect': connect})
                if 'cookies' in kwargs and kwargs['cookies']:
                    token_cookies.s(cookies=cookies, connect=connect).apply_async(queue=worker_hostname + '_' + hostname_id + '_tokens_cookies30', kwargs={'cookies': cookies, 'connect':connect })
                if 'connect' in kwargs:
                    del kwargs['connect']
                if 'cookies' in kwargs:
                    del kwargs['cookies']
                kwargs['grab'] = grab
                return func(self, *args, **kwargs)
            else:
                if 'connect' in kwargs:
                    del kwargs['connect']
                if 'cookies' in kwargs:
                    del kwargs['cookies']
                logger.error("GrabDocCode, Task %s is retried, %s retries" % (self.request.id, self.request.retries))

                if 'GrabDocCode' in kwargs:
                    if kwargs['GrabDocCode'] >= 3:
                        kwargs['grab'] = grab
                        return func(self, *args, **kwargs)
                    else:
                        kwargs['GrabDocCode'] += 1
                else:
                    kwargs['GrabDocCode'] = 1

                self.retry(countdown=1, kwargs=kwargs)
        return function
    return decorator_func


def get_page14():
    '''
    Декоратор для скачивания странички
    kwargs['url'] - урл для скачивания
    kwargs['connect'] - коннект
    kwargs['post'] - параметры для POST запроса
    kwargs['cookies'] - параметры для cookies
    kwargs['connect_timeout'] - параметр connect_timeout
    kwargs['timeout'] - параметр timeout
    '''
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):

            grab_debug = app.conf.get_by_parts("KB", "WORKER_GRAB_DEBUG")
            worker_hostname = app.conf.get_by_parts("KB", "WORKER_HOSTNAME")
            if grab_debug:
                procces_index = current_process().index
                path = 'log/' + worker_hostname + '/' + str(procces_index)
                make_dir(path)

            try:
                url = kwargs['url']
            except KeyError:
                url = None
                logger.error(
                    "Url is None, Task %s is revoked, %s retries" % (self.request.id, self.request.retries)
                )
                revoke(self.request.id)

            post = kwargs.get('post', {})

            try:
                with get_driver_14() as driver:
                    # driver = get_driver_14()
                    kwargs['driver'] = driver
                    response = None

                    try:
                        response = get_post_response_14(driver, url, post)
                    except Exception as e:
                        logger.error("Exception from: %s" % str(e))
                        driver.quit()
                        kwargs['driver'] = {}
                        set_global_driver_to_none()
                        if 'ConnectionError' in kwargs:
                            if kwargs['ConnectionError'] >= 3:
                                revoke(self.request.id)
                                logger.error(
                                    "ConnectionError, Task %s is revoked, %s retries" % (self.request.id, self.request.retries)
                                )
                            else:
                                kwargs['ConnectionError'] += 1
                        else:
                            kwargs['ConnectionError'] = 1
                        logger.error("Task %s, retries %s " % (self.request.id, self.request.retries))
                        self.retry(countdown=1, kwargs=kwargs)

                    if "RSA PRIVATE KEY" in response:
                        logger.error("Java script did not load the page with captcha")
                        driver.quit()
                        kwargs['driver'] = {}
                        set_global_driver_to_none()
                        if 'CaptchaError' in kwargs:
                            if kwargs['CaptchaError'] >= 3:
                                revoke(self.request.id)
                                logger.error(
                                    "CaptchaError, Task %s is revoked, %s retries" % (self.request.id, self.request.retries)
                                )
                            else:
                                kwargs['CaptchaError'] += 1
                        else:
                            kwargs['CaptchaError'] = 1
                        logger.error("Task %s, retries %s " % (self.request.id, self.request.retries))
                        self.retry(countdown=1, kwargs=kwargs)
                    elif "Неверный формат запроса" in response:
                        logger.error("Response is not valid" % url)
                        driver.quit()
                        logger.error("400 Bad Request, Task %s" % self.request.id)
                    else:
                        kwargs['body'] = response
                        return func(self, *args, **kwargs)
            except Exception as e:
                print(e)
                logger.error("Exception from: %s" % url)
                logger.error("%s" % str(e), exc_info=True)
                if 'NetworkError' in kwargs:
                    if kwargs['NetworkError'] >= 3:
                        revoke(self.request.id)
                        logger.error(
                            "NetworkError, Task %s is revoked, %s retries" % (self.request.id, self.request.retries)
                        )
                    else:
                        kwargs['NetworkError'] += 1
                else:
                    kwargs['NetworkError'] = 1

                self.retry(countdown=1, kwargs=kwargs)

        return function
    return decorator_func