import requests


def get_geoweb_cookie():
    url = "https://goy.geoweb.kr/Member/Login"

    payload = "IDSave=false&LoginID=%EB%B3%B4%EB%A6%AC%EC%95%BD%ED%92%88&Password=1234&returnUrl="
    headers = {
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "host": "goy.geoweb.kr",
    }
    session = requests.Session()
    response = session.post(url, headers=headers, data=payload)
    return session.cookies.get_dict()
