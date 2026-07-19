import os
import sys
import time
import msvcrt
import ctypes
from ctypes import wintypes
from tkinter import Tk, filedialog

winmm = ctypes.WinDLL("winmm.dll")
mci = winmm.mciSendStringW

while True:
    try:
        i = input("输入你要做的事…（中文）：").strip( )
        if i == "退出hetMP" or i == "我要出去！" or i == "退出":
            print("再见（别说是你写错）")
            break
        elif i == "播放" or i == "播放歌曲" or i == "我要听歌" or i == "听歌":
            if len(sys.argv) > 1:
                path = sys.argv[1]
            else:
                root = Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                path = filedialog.askopenfilename(
                    title="选择一个音频文件（不支持FLAC，播放会没声！）：",
                    filetypes=[("音频文件（.wav或.mp3）", "*.wav;*.mp3"), ("所有文件", "*.*")]
                )
                root.destroy()

            if not path or not os.path.isfile(path):
                print("没有选文件/文件不存在，下一个")
                continue
            else:
                alias = "player"
                mci(f'open "{path}" alias {alias}', None, 0, None)
                mci(f'play {alias}', None, 0, None)
                print(f"正在播放：{os.path.basename(path)}")
                print("输入“暂停或继续”暂停或继续，输入“加”加音量，输入“减”减音量，输入“停”或“停停停”停止，输入“退出”退出，输入“当前状态”查询当前状态，输入“换歌”或”下一首“或“切歌”切换歌曲")
                volume = 510
                mci(f'setaudio {alias} volume to {volume}', None, 0, None)
                pause = False
                while True:
                    cmd = input("输入想做的事……")
                    if cmd == "暂停或继续":
                        if pause:
                            mci(f'resume {alias}', None, 0, None)
                            pause = False
                            print("已继续(owo)")
                        else:
                            mci(f'pause {alias}', None, 0, None)
                            pause = True
                            print("已暂停⏸⏸⏸(-w-)")
                    elif cmd == "停" or cmd == "停停停":
                        mci(f'stop {alias}', None, 0, None)
                        mci(f'close {alias}', None, 0, None)
                        print("已停止(>w<)")
                        break
                    elif cmd == "加":
                        if volume >= 640:
                            print("到顶了，不能再加了(awa)")
                        else:
                            st = int(input("输入想增加的音量："))
                            if st <= 0:
                                print("你是不是没输音量？")
                            else:
                                if volume + st > 640:
                                    print("你输入的数字过大")
                                else:
                                    volume = volume + st
                                    mci(f'setaudio {alias} volume to {volume}', None, 0, None)
                                    print(f"音量加好了(^w^)，现在音量：{volume//10}%")
                    elif cmd == "减":
                        if volume <= 0:
                            print("不能再减音量了")
                        else:
                            st = int(input("输入想减少的音量："))
                            if st <= 0:
                                print("你是不是又没输音量？")
                            elif volume - st < 0:
                                print("你输入的数字过大")
                            else:
                                volume = volume - st
                                mci(f'setaudio {alias} volume to {volume}', None, 0, None)
                                print(f"音量减好了(^w^)，现在音量：{volume//10}%")
                    elif cmd == "让我出去" or cmd == "退出":
                        mci(f'stop {alias}', None, 0, None)
                        mci(f'close {alias}', None, 0, None)
                        print("拜拜")
                        break
                    elif cmd == "当前状态":
                        if not pause:
                            print(f"正在播放：{os.path.basename(path)}")
                        else:
                            print(f"已暂停：{os.path.basename(path)}")
                        print(f"当前音量：{volume//10}%")
                    elif cmd == "换歌" or cmd == "下一首" or cmd == "切歌":
                        if not pause:
                            mci(f'pause {alias}', None, 0, None)
                            pause = True
                        rot = Tk()
                        rot.withdraw()
                        rot.attributes('-topmost', True)
                        new_path = filedialog.askopenfilename(
                            title="选择新音频",
                            filetypes=[("音频", "*.wav;*.mp3"), ("所有", "*.*")]
                        )
                        rot.destroy()
                        if new_path and os.path.isfile(new_path):
                            mci(f'stop {alias}', None, 0, None)
                            mci(f'close {alias}', None, 0, None)
                            path = new_path
                            mci(f'open "{path}" alias {alias}', None, 0, None)
                            mci(f'play {alias}', None, 0, None)
                            mci(f'setaudio {alias} volume to {volume}', None, 0, None)
                            pause = False
                            print(f"已换歌：{os.path.basename(path)}")
                        else:
                            mci(f'resume {alias}', None, 0, None)
                            pause = False
                            print("已恢复原歌")
                    else:
                        print("你在说什么？再说一遍")
        elif i == "读取JSON文件" or i == "读取" or i == "读取JSON":
            rot = Tk()
            rot.withdraw()
            rot.attributes('-topmost', True)
            json_path = filedialog.askopenfilename(
                title="选择JSON文件",
                filetypes=[("JSON文件", "*.json"), ("所有", "*.*")]
            )
            rot.destroy()
            if not json_path:
                print("你没有选择文件(OwO)")
            else:
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        print(f.read())
                except UnicodeDecodeError:
                    print("这个JSON文件似乎并非UTF-8($w$)")
                    try:
                        with open(json_path, "r", encoding="gbk") as f:
                            print(f.read())
                    except Exception as ec:
                        print("好像也并非GBK，用祖传GB2312试试")
                        try:
                            with open(json_path, "r", encoding="gb2312") as f:
                                print(f.read())
                        except Exception as e:
                            print("我真的不会了(qwq)")
        elif i == "关于":
            print("Het v1.0.0")
            time.sleep(0.1)
            print("好了，回去听歌吧")
            continue
        elif i == "":
            pass
        else:
            print("你这人在说啥呢我听不懂")
    except KeyboardInterrupt:
        print("这里不可以按Ctrl+C")
    except ValueError:
        print("记得输数字")
    except Exception as ex:
        print(f"错误：{ex}")