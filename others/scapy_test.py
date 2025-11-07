from scapy.all import srp, Ether, ARP


def get_remote_mac(ip):
    # Создаем ARP-запрос для указанного IP-адреса
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

    # Отправляем запрос и получаем ответы
    answered, _ = srp(arp_request, timeout=2, verbose=False)

    # Извлекаем MAC-адрес из ответа
    for _, received in answered:
        return received[Ether].src

    return None


remote_ip = '10.253.5.16'  # IP-адрес удаленного устройства
remote_mac = get_remote_mac(remote_ip)
if remote_mac:
    print(f'MAC адрес удаленного устройства {remote_ip}: {remote_mac}')
else:
    print(f'Не удалось получить MAC адрес для {remote_ip}')
