#!/usr/bin/env python

import os
import time
import random
import urllib2
import logging
import logging.config
import RPi.GPIO as GPIO

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
g_port = 17
g_logger = None

def internet_on():
    try:
        url = random.choice(g_urls)
        g_logger.debug("Try to open URL {}".format(url))
        urllib2.urlopen(url, timeout=3)
        return True
    except Exception as e:
        g_logger.debug(e)
        return False

def gpio_set_output(is_high):
    if is_high:
        g_logger.debug("GPIO {} output high".format(g_port))
        GPIO.output(g_port, GPIO.HIGH)
    else:
        g_logger.debug("GPIO {} output low".format(g_port))
        GPIO.output(g_port, GPIO.LOW)

def reset_router():
    g_logger.info("Power off router")
    gpio_set_output(True)
    time.sleep(10)
    g_logger.info("Power on router")
    gpio_set_output(False)
    time.sleep(20)

def main():
    global g_logger
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(os.path.join(dir_path, "logging.conf"))
    g_logger = logging.getLogger("root")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(g_port, GPIO.OUT, initial=GPIO.LOW)

    fail_count = 0
    while True:
        a = time.time()
        is_on = internet_on()
        b = time.time()
        g_logger.debug("Status {} Time {}".format(is_on, b - a))
        if not is_on:
            fail_count += 1
            if fail_count >= 10:
                reset_router()
        else:
            fail_count = 0
        time.sleep(30)

if __name__ == "__main__":
    main()
