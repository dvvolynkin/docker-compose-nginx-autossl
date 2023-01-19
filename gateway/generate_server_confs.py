import json
import os

RESTY_CONF_DIR = os.environ["RESTY_CONF_DIR"]
NGINX_CONF_DIR = os.environ["NGINX_CONF_DIR"]
GATEWAY_SERVERS_CONFIG_FILE = os.environ["GATEWAY_SERVERS_CONFIG_FILE"]
MAIN_DOMAIN = os.environ["MAIN_DOMAIN"]
NGINX_STUBS_SERVER_NAME = os.environ.get('NGINX_STUBS_SERVER_NAME', 'gateway')

if __name__ == '__main__':
    # Читаем шаблон server-proxy.conf
    with open('./gateway.json') as f:
        gateway_conf = json.load(f)
    with open(f"{RESTY_CONF_DIR}/server-proxy.conf", "r") as template_file:
        server_proxy_template = template_file.read()

    # Читаем шаблон server-proxy-location.conf
    with open(f"{RESTY_CONF_DIR}/server-proxy-location.conf", "r") as template_file:
        server_proxy_location_template = template_file.read()

    # Для каждого сайта из списка SITES
    for subdomain in gateway_conf['subdomains']:
        # Извлекаем информацию о сайте
        server_name = subdomain["name"] + '.' + MAIN_DOMAIN
        if subdomain["name"] == '_':
            server_name = '_'
        if subdomain["name"] == '':
            server_name = MAIN_DOMAIN
        locations = subdomain["locations"]

        # Создаем строку с описанием locations
        locations_str = ""
        for location, server_endpoint in locations.items():
            # Заполняем шаблон server-proxy-location.conf соответствующими значениями
            location_str = server_proxy_location_template.replace("$LOCATION", location).replace("$SERVER_ENDPOINT", server_endpoint)
            # Добавляем location_str к locations_str
            locations_str += location_str

        # Заполняем шаблон server-proxy.conf соответствующими значениями
        server_proxy_str = server_proxy_template.replace("$SERVER_NAME", server_name).replace("$LOCATIONS", locations_str)

        # Записываем результат в файл ${NGINX_CONF_DIR}/{server_name}.conf
        with open(f"{NGINX_CONF_DIR}/{server_name}.conf", "w") as out_file:
            out_file.write(server_proxy_str)

    with open(f'{RESTY_CONF_DIR}/stubs-server.conf', 'r') as template_file:
        template = template_file.read()
        result_config = template.replace('$STUBS_SERVER_NAME', NGINX_STUBS_SERVER_NAME)
        with open(f"{NGINX_CONF_DIR}/{NGINX_STUBS_SERVER_NAME}.conf", "w") as out_file:
            out_file.write(result_config)

