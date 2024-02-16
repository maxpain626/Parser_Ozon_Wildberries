#from urllib.request import Request, urlopen
import urllib.request as urllib2
import re
import zipfile
import hashlib
import os.path
#import requests

def query_http(url):
    req = urllib2.Request(url)
    #req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
    #req.add_header("Accept-Encoding", "gzip, deflate, br")
    #req.add_header("Accept-Language", "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3")
    #req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0")
    #req.add_header("Host", "www.ozon.ru")
    #req.add_header("Cookie", "cf_clearance=ZsDsBEDn5cukn5CXbPCpi6MaqWvVJFCWR2rPqUUFCx0-1708101139-1.0-AXCrkBrrK8nEnNcVfv3mi+RmHDU3peSXFs2L4NszB+RdKE4vCcSc5GBEhs15yARjCRhsJiD0WU8aKcRZn1tRWuE=; abt_data=b19a8bbf747e7978ccffa5df7e96ed74:2436cfdeb640d0f2369b0f5b654057da5c3e65ea417e3d19bdcfd50d1e10d68ed2d220accc3b6e1e8c704cc1d580f1c30af89b8bb07704d140bd69b9030f0435d4fb7499543c66514af79dd996290ad3a383cac26905cc661c80f96f378f8905dcc54af03abd516e274c8e50290195158c25ded80f60e95d663336367390c1e2e47ea09a008851d9694847a21c653cd40b515e7ea4b12c6552eeb6ce63bf4d891f84709db964b5d286114bedf280b2be0eef616fcd0074d5b42dcce00b5fff10; __Secure-ext_xcid=0b7adc1cfba4cbab75b84b84c15ea664; __Secure-refresh-token=4.0.osEq-RpPRC66wfmlCBX29A.36.Af-FNm28ksKjwJp7g08QSuWGG0uRUeMt4MnYIcCEqHYIFZ82vAjz1e7JdGxgCc_blw..20240216183217.-U4yHnHyl932D79kFslX7_v0ITR_69CNOOpfPDwqoXE; __Secure-access-token=4.0.osEq-RpPRC66wfmlCBX29A.36.Af-FNm28ksKjwJp7g08QSuWGG0uRUeMt4MnYIcCEqHYIFZ82vAjz1e7JdGxgCc_blw..20240216183217.uI0qxvmm0ZzsGkffOywHqzfpcb6ps98WYs0PUbi7dEQ; __Secure-ab-group=36; __Secure-user-id=0; is_cookies_accepted=1; xcid=0b7adc1cfba4cbab75b84b84c15ea664; guest=true; ADDRESSBOOKBAR_WEB_CLARIFICATION=1708101141; rfuid=LTE5NTAyNjU0NzAsMzUuNzQ5OTY4MjIzMjczNzU0LDEzNzAwNjM5MTUsTGludXggeDg2XzY0LDE2ODg4NzQ2NjcsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSXNJbkoxTFZKVklpd2ljblVpTENKbGJpMVZVeUlzSW1WdUlsMD0sMCwxLDAsMjQsMjM3NDE1OTMwLC0xLDIyNzEyNjUyMCwwLDEsMCwtNDkxMjc1NTIzLElFNWxkSE5qWVhCbElFZGxZMnR2SUV4cGJuVjRJSGc0Tmw4Mk5DQTFMakFnS0ZneE1Ta2dNakF4TURBeE1ERWdUVzk2YVd4c1lRPT0sZTMwPSw2NSwtMTI4NTU1MTMsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1NDg4NywyOTI0MzUzODMsNA==")
    response = urllib2.urlopen(req)
    return response.read()

def cache(url):
    hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    fname = "cache/" + hash
    if not os.path.isfile(fname):
        content = query_http(url)
        f = open(fname, "wb")
        f.write(content)
        f.close()
    else:
        f = open(fname, "rb")
        content = f.read()
    return content
    

def unzip(data):
    with zipfile._ZipStream(data) as zip_ref:
        content = zip_ref.extract()

    return ""

def query(url):
    zip_data = query_http(url)
    return unzip(zip_data)
    #req = Request(url)

def test_ozon():
    url = "https://www.ozon.ru/product/tecno-smartfon-pova-neo-3-8-128-gb-chernyy-1090852191/"
    content = query(url)

#content = cache("https://www.ozon.ru/product/tecno-smartfon-pova-neo-3-8-128-gb-chernyy-1090852191/")
content = cache("https://www.wildberries.ru/")