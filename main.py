# Developer tg tag: @cryonicx
from tabnanny import check
import requests, string, random, names, json, traceback, threading, urllib3, asyncio, pyautogui, os
from bs4 import BeautifulSoup
import webbrowser as sp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = json.loads(open("./config.json", "r", encoding="utf-8").read())


refCode = config["ref_code"]
succesMessage = 0
badMessage = 0
totalMessage = 0

working_proxies = []
all_proxies = []


class color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET_ALL = "\033[0m"


def write(file, text):
    with open(file, "a+") as f:
        return f.write(text)

def randomstr(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def generate_password() -> str:
    characters = string.ascii_letters + string.punctuation + string.digits
    password = "".join(random.choice(characters) for x in range(random.randint(8, 16)))
    return password

def succes_event():
    global succesMessage
    succesMessage = succesMessage+1

def bad_event():
    global badMessage
    badMessage = badMessage+1

def total_event():
    global totalMessage
    totalMessage = totalMessage+1

def random_userAgent():
    with open("./assets/user_agents.txt", encoding="utf-8") as f:
        lines = f.readlines()
        randomLine = random.choice(lines)
    return randomLine.split("\n")[0]

def get_proxy():
    if config['proxy_type'] == "socks5":
        with open('./assets/proxies.txt', encoding="utf-8") as f:
            lines = f.readlines()
            landline = random.choice(lines).split('\n')[0]
        return {'http': f'socks5://{landline}', 'https': f'socks5://{landline}'}

    elif config['proxy_type'] == "http/https":
        with open('./assets/proxies.txt', encoding="utf-8") as f:
            lines = f.readlines()

            landline = random.choice(lines).split('\n')[0]

        return {"http": f"http://{landline}", "https": f"https://{landline}"}

    elif config['proxy_type'] == "http":
        with open('./assets/proxies.txt', encoding="utf-8") as f:
            lines = f.readlines()
            landline = random.choice(lines).split('\n')[0]

        return {"http": f"http://{landline}"}

def checkProxy(proxyType, proxy):
    proxy = proxy[0]
    prxys = {
        "http": "{}://{}".format(proxyType, proxy),
        "https": "{}://{}".format(proxyType, proxy)
    }
    try:
        res = requests.get("http://ip-api.com/json/", proxies=prxys, timeout=7)
        if res.status_code == 200 or res.status_code == 429: 
            working_proxies.append(prxys)
            print(f"{color.GREEN}[WORKING] {proxy}{color.RESET_ALL}")
    except:
        print(f"{color.RED}[INVALID] {proxy} {color.RESET_ALL}")
        pass


 

class Fuck_Legion_Network:

    def __init__(self, proxy, procces) -> None:
        self.proxy = proxy
        self.session = requests.Session()
        self.session.proxies.update(self.proxy)
        self.count = procces
        self.user_Agent = random_userAgent()

        """
        options = webdriver.ChromeOptions()
        if config["headles_browser"]:
            options.headless = True

        options.add_argument("disable-popup-blocking")
        options.add_argument("disable-notifications")
        options.add_argument("disable-gpu")
        options.add_argument(f"--proxy-server={self.proxy['https']}")
        options.add_argument('ignore-certificate-errors')
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(800, 600)
        """


    def verify_link(self, email):
        import time
        inbox = []
        emailSession = self.session
        retryCount = 1

        #while inbox == []:
        while retryCount <= 6:
            print(f"{color.YELLOW}[{self.count}] Checking email inbox... [ {email} ] {color.RESET_ALL}")
            time.sleep(10)
            responsexd = emailSession.get(f"https://cryptogmail.com/api/emails?inbox={email}", verify=False)
            if responsexd.status_code != 404:
                inbox = responsexd.json()
                break
        headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate",
                "accept-language": "tr,tr-TR;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        discordVerifHtml = emailSession.get(f"https://cryptogmail.com/api/emails/{inbox['data'][0]['id']}", headers=headers, verify=False)
        discordVerifHtml = discordVerifHtml.text
        #print(discordVerifHtml)
        soup = BeautifulSoup(discordVerifHtml, "html.parser")
        #print(soup)
        message_link = [a['href'] for a in soup.find_all('a')]
        #a = soup.find("a", attrs= {"style":'text-decoration:none;line-height:100%;background:#5865f2;color:white;font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:15px;font-weight:normal;text-transform:none;margin:0px;'})
        try:
            discordVerify = message_link[1]
            print(f"{color.GREEN}[{self.count}] Extracted verify link. {discordVerify} {color.RESET_ALL}")
            return discordVerify
        except IndexError:
            print(f"{color.RED}[{self.count}] List index out of range. {color.RESET_ALL}")
            discordVerify = None

            return discordVerify

    
    def verify_email(self, link):
        #self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        #self.driver.get(link)
        #time.sleep(10)
        #self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 

        sp.open(link)
        print(f"{color.GREEN}[{self.count}] Email verified successfully. {color.RESET_ALL}")
        time.sleep(7)
        pyautogui.hotkey('ctrl', 'w')
        print(f"{color.GREEN}[{self.count}] +5$ has been successfully credited to your account. {color.RESET_ALL}")
        """
        token = link.split("=")[0]
        payload = {
            "token": token
        }

        headers = {
            "authority": "verify.legionnetwork.io",
            "path": f"/?token={token}",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru",
            "cache-control": "max-age=0",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "cookie": "__cf_bm=mw3LfYtyqkaEDqAzDpWralPwpB8JDMkH6kC.um6.JVg-1644690417-0-ARbzfoU/K+rNJi+a+sepmWEFmZBrPBuq2AfD3r56nsWXzlO+CfkGN3CqW5KFIUbYlDvHtFWL43w7Gg1lQT7pMffHDZ4Z55I8mRligqBwSUNojC5WQJLRfLLC/tw8vZYoKQ==",
            "upgrade-insecure-requests": "1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": self.user_Agent

        }
        ver = self.session.get(link, headers=headers, json=payload)
        if ver.status_code == 200:
            print(f"{color.GREEN}[{self.count}]{color.RESET_ALL} Email verified successfully.")
            print(f"{color.GREEN}[{self.count}] +5$ has been successfully credited to your account. {color.RESET_ALL}")

        else:
            print(f"{color.RED}[{self.count}]{color.RESET_ALL} Email could not be verified.\n{ver.text}")
        """
    
    def createAccount(self):

            username = randomstr(10)
            first_name = names.get_first_name(gender='male')
            uuid = f"{''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(8))}-{''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(4))}-{''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(4))}-{''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(12))}"
            password = generate_password()

            payload = {
                "email": f"{username}@labworld.org",
                "password": password,
                "name": first_name,
                "udid": uuid,
                "referralCode": refCode
            }

            headers = {
                "Content-Type": "application/json",
                "cf-visitor": "https",
                "User-Agent": "Legion/5.2 CFNetwork/1209 Darwin/20.2.0",
                "Connection": "keep-alive",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru",
                "x-forwarded-proto": "https",
                "Accept-Encoding": "gzip, deflate, br"
            }

            try:
                __req = self.session.post(f"https://api.legionnetwork.io/api1/user/create", headers=headers, json=payload, timeout=500)
                
                if __req.status_code == 200:
                    print(f"{color.GREEN}[{self.count}] Successfully registered. {color.GREEN}[ {payload['email']} | {payload['password']} ]{color.RESET_ALL}")
                    write("./accounts.txt", f"{payload['email']}|{payload['password']}\n")
                    print(f"{color.YELLOW}[{self.count}] Starting the email verification process... [ {payload['email']} ]  {color.RESET_ALL}")

                    try:
                        _verify_link = self.verify_link(payload["email"])
                        if _verify_link:
                            self.verify_email(_verify_link)
                        else:
                            print(f"{color.YELLOW}[{self.count}] Please click the link:{color.RESET_ALL}\n{_verify_link}")
                    except Exception as er:
                        print(f"{color.RED}[{self.count}]{color.RESET_ALL} Error: {er}")

            except Exception as err:
                print(f"{color.RED}[{self.count}] Error: {err}{color.RESET_ALL}")
                pass


def tharding(thread, adet):
    print(len(working_proxies))
    import time
    try:
        tx = []
        for i in range(adet):
            if threading.active_count() <= thread:
                try:
                    if len(working_proxies) <= 0:
                        return
                    mT = threading.Thread(target=Fuck_Legion_Network(random.choice(working_proxies), i+1).createAccount)
                    all_proxies.clear()
                    mT.daemon = True
                    mT.start()
                    tx.append(mT)
                except Exception as err:
                    traceback.print_exc()
                    print(f"passed {err}")
                    return

        for t in tx:
            t.join(75)
    except Exception as e:
        traceback.print_exc()
        pass


def proxy_handler():

    proxies = open("./assets/proxies.txt", encoding="utf-8").readlines()
    print(f"{color.GREEN}[+]{color.RESET_ALL} Checking proxies.. [{len(proxies)}]")
    check_list = []
    for proxy in proxies:
        x = threading.Thread(target=checkProxy, args=(config["proxy_type"],proxy.split("\n"[0]),)).start()
        check_list.append(x)




if __name__ == "__main__":
    import time
    if config["check_proxy"]:
        proxy_handler()
        time.sleep(10)
        os.system("cls")
        tharding(100,999999999999)