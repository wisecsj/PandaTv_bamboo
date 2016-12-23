# coding:utf-8

import sys
import time
import uuid
import math
import random
from io import BytesIO
import traceback
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from aux2 import trail

driver = webdriver.Chrome()
driver.maximize_window()  # 最大化浏览器窗口
# driver.implicitly_wait(3)
driver.get('http://www.geetest.com/exp_popup')
# element = WebDriverWait(driver, 6).until(
#         EC.presence_of_element_located((By.ID, "popup-submit"))
#     )
btn = driver.find_element_by_id('popup-submit')
btn.click()


def get_image():
    im1 = driver.find_element_by_class_name("gt_box")
    location = im1.location
    # print(location)
    size = im1.size
    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x'] + size['width'])
    bottom = int(location['y'] + size['height'])
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    crop = screenshot.crop((left, top, right, bottom))
    return crop
    # crop.show()


def cmp_pixel(im1, im2, x, y):
    pix1 = im1.load()[x, y]
    pix2 = im2.load()[x, y]
    if (abs(pix1[0] - pix2[0]) < 80) and (abs(pix1[1] - pix2[1]) < 80) and (
                abs(pix1[2] - pix2[2]) < 80):
        return True
    else:
        return False


# 通过测试，每个滑块与其四个边缘都是差5px
def cmp_image(im1, im2, start_column):
    diff_column = 0
    flag = False
    width, height = im1.size
    for x in range(start_column, width):
        for y in range(height):
            if not cmp_pixel(im1, im2, x, y):
                diff_column = x
                flag = True
                break
        if flag:
            break
    return diff_column


def get_diff(tries=3):
    if tries > 0:
        start_column = 64
        im1 = get_image()
        # im1.show()
        im1.save('3.png')
        slide = driver.find_element_by_class_name("gt_slider_knob")  # get the slide element
        slide.click()
        time.sleep(2.8)  # 滑块点击后出错信息会显示在image的底部，所以得sleep等出错信息消失后再crop

        im2 = get_image()
        im2.save('4.png')
        # im2.show()
        time.sleep(2)

        diff_column = cmp_image(im1, im2, start_column)
        if diff_column == start_column:
            refresh_btn = driver.find_element_by_class_name("gt_refresh_button")
            refresh_btn.click()
            time.sleep(2)
            return get_diff(tries=tries - 1)  # 需要注意
        return diff_column
    else:
        sys.exit('tries is less than 0')


if __name__ == "__main__":
    diff_column = int(get_diff())
    print(diff_column)
    action = ActionChains(driver)
    slide = driver.find_element_by_class_name("gt_slider_knob")  # get the slide element

    trail_list = trail(diff_column - 7)
    action.move_to_element(to_element=slide).perform()
    action.click_and_hold(on_element=slide).perform()

    for x, y, t in trail_list:
        print(x, y, t)
        action.move_by_offset(xoffset=x, yoffset=y).perform()
        # action.move_to_element_with_offset(to_element=slide, xoffset=22 + x, yoffset=y + 22).perform()
        # action.click_and_hold().perform()
        time.sleep(t)
    action.release(on_element=slide).perform()
