# import json
#
# import requests
#
# url = 'https://portal.krasnoe-beloe.ru/rest/kb.telegram.openline.add.json'
# data = {'chat_id': 820818455, 'first_name': 'Влад', 'username': 'vladbi4', 'last_name': 'Ерофеев'}
# params = {'auth': "eaaadd650065fd06005b0f0e00000001000007cb9bd916266a9a13d3bbb8e0b9012934"}
# body = requests.post(url, params=params, json=data)
# print(body.text)
# response = json.loads(body.content)
# result = response['result']
# print(result)

# e595dd650065fd06005b0f0e00000001000007ec39c87a7d9d0d68e629b0073ac5383e



import requests

# cookies = {
#     'currentRegion': 'RU-MOW',
#     'currentPOS': 'C027',
#     'anonymous-consents': '%5B%7B%22templateCode%22%3A%22adpr%22%2C%22templateVersion%22%3A1%2C%22consentState%22%3Anull%7D%2C%7B%22templateCode%22%3A%22generic%22%2C%22templateVersion%22%3A1%2C%22consentState%22%3Anull%7D%5D',
#     'cookie-notification': 'NOT_ACCEPTED',
#     'flocktory-uuid': '70d1b280-c583-4645-ac34-b8edb2f30feb-0',
#     '_ym_uid': '169962824892776562',
#     '_ym_d': '1705398202',
#     'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
#     'mindboxDeviceUUID': '4993bb6a-a0a4-46b7-8a2a-4b7b7cd914ff',
#     'directCrm-session': '%7B%22deviceGuid%22%3A%224993bb6a-a0a4-46b7-8a2a-4b7b7cd914ff%22%7D',
#     'currentDeliveryMode': 'pickup',
#     'avifActive': 'true',
#     'webpActive': 'true',
#     'dtCookie': 'v_4_srv_35_sn_A9E9E64293104748D3A4B3B5870C37DA_perc_100000_ol_0_mul_1_app-3Ab08f9e5bb12c9b66_1',
#     'rxVisitor': '1712742062088KGPA46SVJM7B5IL1EAU9NP2N8U2N8A0J',
#     '_ym_isad': '1',
#     'advcake_track_id': '0c79db4e-9e81-9280-fe11-b4a1af51e4df',
#     'advcake_session_id': '79b3b0eb-d84d-7e8b-f514-0ad1fed243fe',
#     '_userGUID': '0:lutmehl5:L3VZm63PleU1DfLuAmzhmwp9ejd_Lc8f',
#     '_gid': 'GA1.2.845174445.1712742063',
#     'JSESSIONID': '91e40b26-970a-4a4c-9289-89e7f9285f7b',
#     'age-confirmed': '1',
#     'siteWineLab-cart': '310ceed5-776b-4bc3-9e22-0aa7ce430361',
#     'qrator_ssid': '1712758278.729.4xsQGvCWZRO42r0u-40sj632gq3naor82l5rtevvpqt2gqvfs',
#     '_ym_visorc': 'b',
#     '_gat_UA-125169834-1': '1',
#     'dSesn': 'f6bc1136-c697-c916-6c9f-d2d0d3096331',
#     '_dvs': '0:lutw2264:DSy1bseD9gWIL7nsLGy_42yP1VwyiBft',
#     'qrator_jsr': '1712758285.469.Gp4ZhGGtzkDHzfH2-g06tofsiaj6524rdg5u3likcj39h9rb6-00',
#     'qrator_jsid': '1712758285.469.Gp4ZhGGtzkDHzfH2-64qp61dcpcem6qhmqnes0aggtsmjo1j9',
#     'dtSa': '-',
#     'advcake_track_url': '%3D20240408ljwQVbyRwniYwiI2a4HCc%2BB0Y%2FrhBT%2FBPgaFBu8RvC2fiwC9LeIt5SijsqO3IAXxvjW3nxUguplr35bmRvhRyROnFcWWb7RF74bgZ7XmPEbMGoEJ2lsXQ6ZOESI4kzl5NZxC3ZREVyXFUwGYK1KMz8WJE4j4mBrMyvOEzvP9qufJ1dSFXdBF7CD%2FLXUwDLj%2FJI57W0ySOZIm0q4w7GWW3ttssNlggjnUI5gHNpX5kuz7Y6wLv%2BIpB0Fyr3YqFLEGfes5XHn%2BZnm9gSaaRU%2F6Rhsitl2R1kiZF5bwe1qzHn2lza7YyW5zOB722vukr%2FCOg%2FrYI7hs%2F%2FXLYdaA3zJWQnJdAa9dNg9YnZL7gZIk6lGakgeF7AEItzt9y7BMXcg0RkSa8yNovytvwzS%2BzJj2ZYkwnPTYpdinfaEXMgFVCv9mzj4lbByggFyNfeTiDVWp9UXqMXAE4tfgNwIMeS3xzit8Qqzv3enkwoXcZtqvA4tq%2Flv%2BPTWIjpoM7sn81TXDiWkjzLxaDiPBpGw8Ia70KxJtNB5yzMoDQmLXRywt%2FcL%2FCOSyWgv82%2BaVbp3yefbawXDvj1gLfQJ1gH4RKF%2F8KBWBuykL8FgCzjcRbMV95g3Hqh5b6EWDeXg%2FsQ99%2BZ1KEfUdP4TdNCUfu0TPYsPeCvZ0RD3zH4voQwA6lKrGdZss7i6M0S2BU%2Bg%3D',
#     '_ga_M2S97XLR16': 'GS1.1.1712758278.7.1.1712758290.48.0.0',
#     'digi_uc': 'W1siY3YiLCIxMDI0NjU2IiwxNzEyNzQyNDU0NzkyXSxbImN2IiwiMTAwNDEwNCIsMTcxMjc1ODI5MDE4MV1d',
#     'rxvt': '1712760090265|1712758278345',
#     '_ga_9YHSC7Y1FD': 'GS1.1.1712758278.7.1.1712758290.0.0.0',
#     '_ga': 'GA1.1.1126286248.1705398202',
#     'dtPC': '35$358286918_78h-vFTDRUCMLWHUIFSPAEIHHMMCTQLKOJMQS-0e0',
# }
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7',
#     'cache-control': 'max-age=0',
#     # 'cookie': 'currentRegion=RU-MOW; currentPOS=C027; anonymous-consents=%5B%7B%22templateCode%22%3A%22adpr%22%2C%22templateVersion%22%3A1%2C%22consentState%22%3Anull%7D%2C%7B%22templateCode%22%3A%22generic%22%2C%22templateVersion%22%3A1%2C%22consentState%22%3Anull%7D%5D; cookie-notification=NOT_ACCEPTED; flocktory-uuid=70d1b280-c583-4645-ac34-b8edb2f30feb-0; _ym_uid=169962824892776562; _ym_d=1705398202; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; mindboxDeviceUUID=4993bb6a-a0a4-46b7-8a2a-4b7b7cd914ff; directCrm-session=%7B%22deviceGuid%22%3A%224993bb6a-a0a4-46b7-8a2a-4b7b7cd914ff%22%7D; currentDeliveryMode=pickup; avifActive=true; webpActive=true; dtCookie=v_4_srv_35_sn_A9E9E64293104748D3A4B3B5870C37DA_perc_100000_ol_0_mul_1_app-3Ab08f9e5bb12c9b66_1; rxVisitor=1712742062088KGPA46SVJM7B5IL1EAU9NP2N8U2N8A0J; _ym_isad=1; advcake_track_id=0c79db4e-9e81-9280-fe11-b4a1af51e4df; advcake_session_id=79b3b0eb-d84d-7e8b-f514-0ad1fed243fe; _userGUID=0:lutmehl5:L3VZm63PleU1DfLuAmzhmwp9ejd_Lc8f; _gid=GA1.2.845174445.1712742063; JSESSIONID=91e40b26-970a-4a4c-9289-89e7f9285f7b; age-confirmed=1; siteWineLab-cart=310ceed5-776b-4bc3-9e22-0aa7ce430361; qrator_ssid=1712758278.729.4xsQGvCWZRO42r0u-40sj632gq3naor82l5rtevvpqt2gqvfs; _ym_visorc=b; _gat_UA-125169834-1=1; dSesn=f6bc1136-c697-c916-6c9f-d2d0d3096331; _dvs=0:lutw2264:DSy1bseD9gWIL7nsLGy_42yP1VwyiBft; qrator_jsr=1712758285.469.Gp4ZhGGtzkDHzfH2-g06tofsiaj6524rdg5u3likcj39h9rb6-00; qrator_jsid=1712758285.469.Gp4ZhGGtzkDHzfH2-64qp61dcpcem6qhmqnes0aggtsmjo1j9; dtSa=-; advcake_track_url=%3D20240408ljwQVbyRwniYwiI2a4HCc%2BB0Y%2FrhBT%2FBPgaFBu8RvC2fiwC9LeIt5SijsqO3IAXxvjW3nxUguplr35bmRvhRyROnFcWWb7RF74bgZ7XmPEbMGoEJ2lsXQ6ZOESI4kzl5NZxC3ZREVyXFUwGYK1KMz8WJE4j4mBrMyvOEzvP9qufJ1dSFXdBF7CD%2FLXUwDLj%2FJI57W0ySOZIm0q4w7GWW3ttssNlggjnUI5gHNpX5kuz7Y6wLv%2BIpB0Fyr3YqFLEGfes5XHn%2BZnm9gSaaRU%2F6Rhsitl2R1kiZF5bwe1qzHn2lza7YyW5zOB722vukr%2FCOg%2FrYI7hs%2F%2FXLYdaA3zJWQnJdAa9dNg9YnZL7gZIk6lGakgeF7AEItzt9y7BMXcg0RkSa8yNovytvwzS%2BzJj2ZYkwnPTYpdinfaEXMgFVCv9mzj4lbByggFyNfeTiDVWp9UXqMXAE4tfgNwIMeS3xzit8Qqzv3enkwoXcZtqvA4tq%2Flv%2BPTWIjpoM7sn81TXDiWkjzLxaDiPBpGw8Ia70KxJtNB5yzMoDQmLXRywt%2FcL%2FCOSyWgv82%2BaVbp3yefbawXDvj1gLfQJ1gH4RKF%2F8KBWBuykL8FgCzjcRbMV95g3Hqh5b6EWDeXg%2FsQ99%2BZ1KEfUdP4TdNCUfu0TPYsPeCvZ0RD3zH4voQwA6lKrGdZss7i6M0S2BU%2Bg%3D; _ga_M2S97XLR16=GS1.1.1712758278.7.1.1712758290.48.0.0; digi_uc=W1siY3YiLCIxMDI0NjU2IiwxNzEyNzQyNDU0NzkyXSxbImN2IiwiMTAwNDEwNCIsMTcxMjc1ODI5MDE4MV1d; rxvt=1712760090265|1712758278345; _ga_9YHSC7Y1FD=GS1.1.1712758278.7.1.1712758290.0.0.0; _ga=GA1.1.1126286248.1705398202; dtPC=35$358286918_78h-vFTDRUCMLWHUIFSPAEIHHMMCTQLKOJMQS-0e0',
#     'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Linux"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
# }

# response = requests.get('https://www.winelab.ru/catalog/vino/results', cookies=cookies, headers=headers)
cookies = {
    'spid': '1713278825283_2a13bb682738db2f98ceb601e4f7756f_fau6e1gqbd0ien5l',
    'spsc': '1713278825283_bc667f85c1ff41ca34c135ef22386470_2dc4c47e5beb4aae25be080fa9d16c8093e7e989cef732b63b8bada59af3d7da',
    # 'PHPSESSID': 'lKvof0kO7dREGnuLw6kT4DyYsIO53HC1',
    # 'tmr_lvid': 'ee10b78ffa9af0837fa84a3f6c1b281a',
    # 'tmr_lvidTS': '1713279254684',
    # '_ym_uid': '1713279255936338365',
    # '_ym_d': '1713279255',
    # '_ym_isad': '1',
    # 'domain_sid': 'dLhQAlVDqqgVehQ0R4WFQ%3A1713279254859',
    # '_ym_visorc': 'w',
    # 'BX_USER_ID': '218e1f35283aeba3d0721d0909335283',
    # 'tmr_detect': '1%7C1713279262246',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    # 'cookie': 'spid=1713278825283_2a13bb682738db2f98ceb601e4f7756f_fau6e1gqbd0ien5l; spsc=1713278825283_bc667f85c1ff41ca34c135ef22386470_2dc4c47e5beb4aae25be080fa9d16c8093e7e989cef732b63b8bada59af3d7da; PHPSESSID=lKvof0kO7dREGnuLw6kT4DyYsIO53HC1; tmr_lvid=ee10b78ffa9af0837fa84a3f6c1b281a; tmr_lvidTS=1713279254684; _ym_uid=1713279255936338365; _ym_d=1713279255; _ym_isad=1; domain_sid=dLhQAlVDqqgVehQ0R4WFQ%3A1713279254859; _ym_visorc=w; BX_USER_ID=218e1f35283aeba3d0721d0909335283; tmr_detect=1%7C1713279262246',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'lang': 'ru',
}

response = requests.get('https://www.okmarket.ru/ajax/buy_list/user/', params=params, cookies=cookies, headers=headers)

print(response.text)