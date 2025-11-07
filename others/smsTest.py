import requests
import logging
from xml.etree.ElementTree import Element, SubElement, tostring

class SMSClient:
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    url = 'https://xml.sms16.ru/xml/'

    def __init__(self, sender, receivers, credentials):
        self.sender = sender
        if isinstance(receivers, str):
            receivers = [receivers]
        self.receivers = receivers
        self.username, self.password = credentials

        # Создание XML-запроса
        request_node = Element('request')

        security_node = SubElement(request_node, 'security')
        SubElement(security_node, 'login', {'value': self.username})
        SubElement(security_node, 'password', {'value': self.password})

        message_node = SubElement(request_node, 'message', {'type': 'sms'})
        sender_node = SubElement(message_node, 'sender')
        sender_node.text = self.sender
        self.text_node = SubElement(message_node, 'text')

        for idx, abonent in enumerate(self.receivers):
            SubElement(message_node, 'abonent', {'phone': abonent, 'number_sms': str(idx + 1)})

        self.xml_tree = request_node

    @property
    def xml(self):
        """Возвращает XML-запрос в виде строки"""
        return tostring(self.xml_tree, encoding='utf-8')

    def send_sms(self, message):
        """Отправляет SMS через API"""
        try:
            self.text_node.text = message
            response = requests.post(url=self.url, headers=self.headers, data=self.xml)
            return response.text  # Вернёт ответ сервера
        except requests.RequestException as e:
            logging.error(f"Ошибка при отправке SMS: {e}")
            return None


if __name__ == "__main__":
    sender = "KrasnoBeloe"
    receivers = ["79168135607"]  # Номера получателей
    credentials = ("krasnoebeloe74", "qwertyQ11")

    sms_client = SMSClient(sender, receivers, credentials)
    response = sms_client.send_sms("тест1")
    print(response)
