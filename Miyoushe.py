import time
import json
import random
import hashlib
import requests
import string
from Loguru import my_logger
from Global import *


def randomStr(n):
    return (''.join(random.sample(string.ascii_lowercase, n))).upper()


def get_ds():
    timestamp = str(int(time.time()))
    random_string = randomStr(6)
    ds_string = 'salt=' + salt + '&t=' + timestamp + '&r=' + random_string
    ds_md5 = hashlib.md5(ds_string.encode(encoding='UTF-8')).hexdigest()
    ds = timestamp + ',' + random_string + ',' + ds_md5
    return ds


def cookie_str2dict(cookie_string):
    cookie = cookie_string.replace(" ", "").split(";")
    cookies = {}
    for i in cookie:
        cookies[i.split("=")[0]] = i.split("=")[1]
    return cookies

class miyoushe:
    def __init__(self,mysCookie,i):
        self.i = i
        self.cookies = cookie_str2dict(mysCookie)
        self.miyoubi = {}
        self.headers = {
            "DS": get_ds(),
            "x-rpc-client_type": client_type,
            "x-rpc-app_version": mysVersion,
            "x-rpc-sys_version": "6.0.1",
            "x-rpc-channel": "miyousheluodi",
            "x-rpc-device_id": randomStr(20) + randomStr(12),
            "x-rpc-device_name": randomStr(random.randint(1, 10)),
            "x-rpc-device_model": "Mi 10",
            "Referer": "https://app.mihoyo.com",
            "User-Agent": "okhttp/4.8.0"
        }

    def miyoushe_sign(self):
        req = requests.get(gameinfoUrl, cookies=self.cookies)
        game_info = json.loads(req.text)
        if (game_info['retcode'] != 0):
            my_logger.error("米游社签到失败！配置文件第" + str(self.i) + "行")
            my_logger.info(game_info)
        else:
            my_logger.info("米游社执行成功！配置文件第" + str(self.i) + "行")
            my_logger.info(game_info)
            post_data = {
                "act_id": "e202009291139501",
                "region": game_info['data']['list'][0]['region'],
                "uid": game_info['data']['list'][0]['game_uid']
            }
            req = requests.post(url=bbssignUrl, data=json.dumps(post_data), headers=self.headers, cookies=self.cookies)
            result = json.loads(req.text)
            my_logger.info(result)

    def miyoubi_all(self):
        self.miyoubi_login()
        if len(self.miyoubi) > 0:
            self.miyoubi_signIn()
            self.articleList = self.miyoubi_getList()
            self.miyoubi_readArticle()
            self.miyoubi_upVote()
            self.miyoubi_share()
            my_logger.info("米游币任务全部完成")



    def miyoubi_login(self):
        if "login_ticket" in self.cookies:
            Cookie = {"login_ticket":self.cookies["login_ticket"]}
            req = requests.get(url=cookieUrl.format(self.cookies["login_ticket"]))
            data = json.loads(req.text.encode('utf-8'))
            if "成功" in data["data"]["msg"]:
                Cookie["stuid"] = str(data["data"]["cookie_info"]["account_id"])
                req = requests.get(url=cookieUrl2.format(Cookie["login_ticket"], Cookie["stuid"]))
                data = json.loads(req.text.encode('utf-8'))
                Cookie["stoken"] = data["data"]["list"][0]["token"]
                self.miyoubi = Cookie
                print("米哈游通行证登录成功！")
            else:
                print("cookie已失效,请重新登录米哈游通行证抓取cookie")
        else:
            print("cookie中没有'login_ticket'字段,请重新登录米哈游通行证抓取cookie!")

    def miyoubi_signIn(self):
        my_logger.info("米游币讨论区正在签到......")
        for i in gameList:
            req = requests.post(url=signUrl.format(i["id"]), cookies=self.miyoubi, headers=self.headers)
            if req.status_code == 200:
                data = json.loads(req.text.encode('utf-8'))
                if "err" not in data["message"]:
                    my_logger.info(str(i["name"] + data["message"]))
                    time.sleep(2)
                else:
                    my_logger.info("签到失败，你的cookie可能已过期，请重新设置cookie。")
            else:
                my_logger.info("请求失败，请检查请求链接")

    def miyoubi_getList(self):
        List = []
        my_logger.info("正在获取帖子列表......")
        for i in gameList:
            req = requests.get(url=listUrl.format(i["forumId"]), headers=self.headers)
            data = json.loads(req.text.encode('utf-8'))
            for n in range(10):
                List.append([data["data"]["list"][n]["post"]["post_id"], data["data"]["list"][n]["post"]["subject"]])
            my_logger.info("已获取{}个帖子".format(len(List)))
            time.sleep(2)
        return List

    def miyoubi_readArticle(self):
        my_logger.info("正在看帖......")
        for i in range(3):
            req = requests.get(url=detailUrl.format(self.articleList[i][0]), cookies=self.miyoubi, headers=self.headers)
            data = json.loads(req.text.encode('utf-8'))
            if data["message"] == "OK":
                my_logger.info("看帖：{} 成功".format(self.articleList[i][1]))
            time.sleep(2)

    def miyoubi_upVote(self):
        my_logger.info("正在点赞......")
        for i in range(5):
            req = requests.post(url=voteUrl, cookies=self.miyoubi, headers=self.headers,
                                json={"post_id": self.articleList[i][0], "is_cancel": False})
            data = json.loads(req.text.encode('utf-8'))
            if data["message"] == "OK":
                my_logger.info("点赞：{} 成功".format(self.articleList[i][1]))
            time.sleep(2)

    def miyoubi_share(self):
        my_logger.info("正在分享......")
        req = requests.get(url=shareUrl.format(self.articleList[0][0]), cookies=self.miyoubi, headers=self.headers)
        data = json.loads(req.text.encode('utf-8'))
        if data["message"] == "OK":
            my_logger.info("分享：{} 成功".format(self.articleList[0][1]))