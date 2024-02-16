def query(url):
    print("url:" + url)
    return 12000

def storage(site):
    return ["https://ozonr.ru/product1", "https://ozonr.ru/product2", "test"]
        
urls = storage("ozon")
print(urls)

prices = {}
for a in urls:
    print("a = " + a)
    prices[a] = query(a)
    
print(prices)
