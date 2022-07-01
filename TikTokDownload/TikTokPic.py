#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:下载无水印图集
@Date       :2022/04/23 21:01:22
@Author     :JohnserfSeed
@version    :1.0.0
@License    :(C)Copyright 2019-2022, Liugroup-NLPR-CASIA
@Github     :https://github.com/johnserf-seed
@Mail       :johnserfseed@gmail.com
'''
import requests,re,json,sys,getopt,time,os

def printUsage():
    print ('''
                                                    TikTokPic V1.0.0
            使用说明：
                    1、本程序目前仅支持命令行调用，只能用于图集下载
                    2、命令行操作方法：
                            1）将本程序路径添加到环境变量
                            2）控制台输入 TikTokPic -u https://v.douyin.com/Fdf4RWq/
                                -u < url 抖音复制的链接:https://v.douyin.com/Fdf4RWq/ >
                                -h < 帮助说明 >

                    3、如有您有任何bug或者意见反馈请在 https://github.com/Johnserf-Seed/TikTokDownload/issues 发起
                    4、GUI预览版本现已发布，操作更简单 https://github.com/Johnserf-Seed/TikTokDownload/tags 下载
                    5、批量寻找用户主页中的图集将在未来版本中更新

            注意：  目前已经支持app内分享短链和web端长链识别。
    ''')

def out_Print():
    print(r'''
████████╗      ██╗      ██╗  ██╗       ████████╗        ██████╗        ██╗  ██╗        ██████╗        ██╗        ██████╗
╚══██╔══╝      ██║      ██║ ██╔╝       ╚══██╔══╝       ██╔═══██╗       ██║ ██╔╝        ██╔══██╗       ██║       ██╔════╝
   ██║         ██║      █████╔╝           ██║          ██║   ██║       █████╔╝         ██████╔╝       ██║       ██║
   ██║         ██║      ██╔═██╗           ██║          ██║   ██║       ██╔═██╗         ██╔═══╝        ██║       ██║
   ██║         ██║      ██║  ██╗          ██║          ╚██████╔╝       ██║  ██╗        ██║            ██║       ╚██████╗
   ╚═╝         ╚═╝      ╚═╝  ╚═╝          ╚═╝           ╚═════╝        ╚═╝  ╚═╝        ╚═╝            ╚═╝        ╚═════╝''')

    #TikTokPic.exe --url=<抖音复制的链接> --music=<是否下载音频,默认为yes可选no>

def Find(string):
    # findall() 查找匹配正则表达式的字符串
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)


def get_args():
    urlarg=""
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hu:m:",["url=","music="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(0)

    try:
        if opts == []:
            printUsage()
            urlarg = str(input("[  提示  ]:请输入图集链接:"))
            return urlarg
    except:
        pass

    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            sys.exit(0)
        elif opt in ("-u", "--url"):
            urlarg = arg

    return urlarg

# 获取当前时间戳
def now2ticks(type):
    """
    @description  : 获取当前时间戳
    ---------
    @param  : type，返回值类型
    -------
    @Returns  : 1650721580 || '1650721580'
    -------
    """
    if type == 'int':
        return int(round(time.time() * 1000))
    elif type == 'str':
        return str(int(round(time.time() * 1000)))

# 下载图集
def pic_download(urlarg):
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }
        try:
            r = requests.get(url = Find(urlarg)[0])
        # 如果输入链接不正确，则重新输入
        except Exception as error:
            print('[  警告  ]:输入链接有误！\r')
            urlarg = get_args()
            while urlarg == '':
                print('[  提示  ]:请重新输入图集链接!\r')
                urlarg = get_args()
            pic_download(urlarg)
            
        # 2022/05/31 抖音把图集更新为note
        key = re.findall('note/(\d+)?',str(r.url))[0]

        # 官方接口
        jx_url  = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={key}'
        js = json.loads(requests.get(url = jx_url,headers = headers).text)

        try:
            creat_time = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(
                js['item_list'][0]['create_time']))

            pic_title = str(js['item_list'][0]['desc'])
            nickname = str(js['item_list'][0]['author']['nickname'])
            # 检测下载目录是否存在
            if not os.path.exists('Download\\' + 'pic\\' + nickname):
                os.makedirs('Download\\' + 'pic\\' + nickname)
            for i in range(len(js['item_list'][0]['images'])):
                # 尝试下载图片
                try:
                    pic_url = str(js['item_list'][0]['images'][i]['url_list'][0])
                    picture=requests.get(url = pic_url,headers = headers)
                    p_url = 'Download\\' + 'pic\\' + nickname + '\\' + creat_time + pic_title + '_' + str(i) + '.jpeg'# + now2ticks()
                    with open(p_url,'wb') as file:
                        file.write(picture.content)
                        print('[  提示  ]:' + p_url + '下载完毕\r')
                except Exception as error:
                    print('[  错误  ]:'+ error + '\r')
                    print('[  提示  ]:发生了点意外！\r')
                    break
        except Exception as error:
            print('[  错误  ]:'+ error + '\r')
            print('[  提示  ]:获取图集失败\r')
            return

if __name__=="__main__":
    # 设置控制台大小
    os.system("mode con cols=120 lines=25")
    # 输出logo
    out_Print()
    # 获取命令行
    urlarg = get_args()
    # 内容为空则重新输入
    while urlarg == '':
        print('[  提示  ]:请重新输入图集链接!\r')
        urlarg = get_args()
    # 调用下载
    pic_download(urlarg)