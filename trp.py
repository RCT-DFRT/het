
from tkinter import Tk, filedialog
from just_playback import Playback

playback = Playback()

play = ["播放", "听歌", "播放歌曲"]
exin = ["退出", "让我出去", "离开"]

while True:
    try:
        print("输入“退出”退出哦~")
        i = input("输入你想做的事：").strip( )
        if i in exin:
            print("请等候音频停止播放")
            playback.stop()
            break
        elif i in play:
            print("请选择音频文件……")
            root = Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            play_path = filedialog.askopenfilename(
                title="请选择音频文件",
                filetypes=[("支持的音频文件", "*.wav;*.mp3;*.flac;*.m4a;*.ogg"), ("所有文件", "*.*")]
            )
            root.destroy()
            if not play_path:
                print("你没选文件或文件不存在")
            else:
                try:
                    playback.stop()
                    playback.load_file(play_path)
                    playback.play()
                    print(f"正在播放：{play_path}")
                    while True:
                        try:
                            tr = input("输入“加”或“加音量”加大音量，输入“减”或“减音量”减小音量，暂停时输入“暂停”可继续播放，播放时输入“暂停”可暂停，输入“退出”停止音乐并退出，输入“当前状态”可查询当前状态")
                            if tr == "加" or tr == "加音量":
                                print(f"当前音量：{playback.volume}")
                                if playback.volume >= 1:
                                    print("已经最高了")
                                else:
                                    try:
                                        c = float(input("添加多少音量？"))
                                        if playback.volume + c > 1:
                                            print("想增加的音量过大")
                                        else:
                                            v = playback.volume + c
                                            playback.set_volume(v)
                                            print(f"完成！当前音量：{v}")
                                    except ValueError:
                                        print("输入数字！")
                            elif tr == "减" or tr == "减音量":
                                print(f"当前音量：{playback.volume}")
                                if playback.volume <= 0:
                                    print("已经静音了")
                                else:
                                    try:
                                        c = float(input("减少多少音量？"))
                                        if playback.volume - c < 0:
                                            print("想减少的音量过大")
                                        else:
                                            v = playback.volume - c
                                            playback.set_volume(v)
                                            print(f"完成！当前音量：{v}")
                                    except ValueError:
                                        print("输入数字！")
                            elif tr == "暂停":
                                if playback.paused:
                                    playback.resume()
                                else:
                                    playback.pause()
                            elif tr == "退出":
                                playback.stop()
                                print("再见！")
                                break
                            elif tr == "当前状态":
                                if not playback.active:
                                    print("未加载(qwq)")
                                elif playback.paused:
                                    print(f"已暂停：{play_path}，进度：{playback.curr_pos:.1f}s / {playback.duration:.1f}s")
                                elif playback.playing:
                                    print(f"正在播放：{play_path}，进度：{playback.curr_pos:.1f}s / {playback.duration:.1f}s")
                                else:
                                    print(f"已停止：{play_path}，但仍然加载")
                        except Exception as ec:
                            print(f"其他错误：{ec}")
                except FileNotFoundError:
                    print("找不到文件")
                except Exception as ex:
                    print(f"错误：{ex}")
    except Exception as e:
        print(f"错误：{e}")