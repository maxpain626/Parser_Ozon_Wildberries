from urllib.request import Request


req = Request('https://www.ozon.ru/product/tecno-smartfon-pova-neo-3-8-128-gb-chernyy-1090852191/')
req.add_header('Accept-Encoding', 'gzip, deflate, br')
#req.add_header()
#req.add_header()
#req.add_header()
#req.add_header()
content = urllib(req).read()

print()

