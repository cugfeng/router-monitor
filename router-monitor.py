#!/usr/bin/env python

import sys
import json
import time
import random
import urllib2
import pexpect
import os, os.path
import logging
import logging.config

g_urls = [
        "http://www.qq.com/",
        "http://www.taobao.com/",
        "http://www.tmall.com/",
# Remove baidu since it's easy to report false alarm
#        "http://www.baidu.com/",
        "http://www.jd.com/",
        "http://www.163.com/",
        "http://www.sina.com.cn/",
        "http://www.sohu.com/",
        "http://www.iqiyi.com/",
        "http://www.youku.com/",
        ]
g_logger = None

def gen_json(json_path):
    data = {
        "host": "x.x.x.x",
        "username": "xxxxxx",
        "password": "xxxxxx"
    }

    with open(json_path, "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)
    g_logger.info("Please set host/username/password in {}".format(json_path))

def parse_json(json_path):
    with open(json_path) as infile:
        data = json.load(infile)
        g_logger.debug("Host    : {}".format(data["host"]))
        g_logger.debug("Username: {}".format(data["username"]))
        g_logger.debug("Password: {}".format(data["password"]))

    return (data["host"], data["username"], data["password"])

def internet_on():
    try:
        url = random.choice(g_urls)
        g_logger.debug("Try to open URL {}".format(url))
        urllib2.urlopen(url, timeout=3)
        return True
    except Exception as e:
        g_logger.debug(e)
        return False

def reboot_router(host, username, password):
    g_logger.info("Reboot router...")
    child = pexpect.spawn("telnet {}".format(host))
    child.expect(".*login:")
    child.sendline(username)
    child.expect("Password:")
    child.sendline(password)
    child.expect(".*#")
    child.sendline("reboot")
    child.expect(pexpect.EOF)
    g_logger.info("Reboot router done")

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    global g_logger
    logging.config.fileConfig(os.path.join(dir_path, "logging.conf"))
    g_logger = logging.getLogger("root")

    json_path = os.path.join(dir_path, "secret.json")
    if not os.path.exists(json_path):
        gen_json(json_path)
        sys.exit(0)
    host, username, password = parse_json(json_path)

    fail_count = 0
    while True:
        a = time.time()
        is_on = internet_on()
        b = time.time()
        g_logger.debug("Status {} Time {}".format(is_on, b - a))
        if not is_on:
            fail_count += 1
            if fail_count >= 10:
                reboot_router(host, username, password)
                fail_count = 0
        else:
            fail_count = 0
        time.sleep(30)

if __name__ == "__main__":
    main()
