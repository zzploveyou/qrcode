# coding:utf-8

import qrcode
from PIL import Image
import os


def openpic(filename):
    os.system("eog " + filename)

# 生成二维码图片


def make_qr(string, pic_name):
    qr = qrcode.QRCode(
        version=4,  # 生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # L:7% M:15% Q:25% H:30%
        box_size=10,  # 每个格子的像素大小
        border=2,  # 边框的格子宽度大小
    )
    qr.add_data(string)
    qr.make(fit=True)

    img = qr.make_image()
    img.save(pic_name)
    openpic(pic_name)

# 生成带logo的二维码图片


def make_logo_qr(string, logo, pic_name):
    # 参数配置
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=8,
        border=2
    )
    # 添加转换内容
    qr.add_data(string)
    #
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    #
    img = img.convert("RGBA")

    # 添加logo
    if logo and os.path.exists(logo):
        icon = Image.open(logo)
        # 获取二维码图片的大小
        img_w, img_h = img.size

        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        # logo图片的大小不能超过二维码图片的1/4
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        # 计算logo在二维码图中的位置
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)

    # 保存处理后图片
    img.save(pic_name)
    openpic(pic_name)


if __name__ == '__main__':
    print
    print "usage: input text, then input empty line to stop input"
    print "       or input q or nothing to stop the script!"
    print
    path = os.path.dirname(os.path.realpath(__file__))
    qrcode_pic = os.path.join(path, 'theqrcode.png')  # 生成后的保存文件
    logo = os.path.join(path, 'logo.png')  # logo图片
    string = "start"
    stop_strings = ["q", "exit", ""]
    while(1):
        string = raw_input("input:\n")
        if(string.strip() in stop_strings):
            break

        # 输入内容允许有空格
        while True:
            line = raw_input()
            if(line == ''):
                break
            else:
                string = string + "\n" + line

        #make_qr(string, qrcode_pic)
        make_logo_qr(string, logo, qrcode_pic)
