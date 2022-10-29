# -*- coding:utf-8 -*-
import tkinter
import threading
import pyaudio
import wave
import transcription
import summarization

start_flag = False
quitting_flag = False
count = 0

def recording():
    global label
    global start_flag
    global quitting_flag
    global count

    CHUNK = 2**10
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    output_path = "./output.wav"
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    while not quitting_flag: #ボタン側で操作する
        if start_flag:
            data = stream.read(CHUNK)
            frames.append(data)
            label.config(text=count)
            count += 1
            
    print("Done.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # 録音データの保存
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # whisperによる文字起こし
    sount2text = transcription.transcription()

    # 要約する
    summary = summarization.summarize(sount2text)
    sorted_summary = sorted(summary['scoring_data'], reverse=True, key=lambda x:x[1])
    # 重要度が高い順の5つの文を表示
    for x in range(5):
        index = sorted_summary[x][0]
        print(summary["summarize_result"][index])


# スタートボタンが押された時の処理
def start_button_click(event):
    global start_flag
    global count

    count = 0
    start_flag = True

# ストップボタンが押された時の処理
def stop_button_click(event):
    global start_flag
    global quitting_flag

    start_flag = False
    quitting_flag = True
    # thread1終了まで待つ
    # thread1.join()

# 終了ボタンが押された時の処理
def quit_app():
    global quitting_flag
    global app
    global thread1

    quitting_flag = True

    # thread1終了まで待つ
    thread1.join()

    # # thread1終了後にアプリ終了
    app.destroy()

# メインウィンドウを作成
app = tkinter.Tk()
app.state('zoomed') # フルスクリーン表示

# ボタンの作成と配置
start_button = tkinter.Button(
    app,
    text="録音開始",
)
start_button.pack()

stop_button = tkinter.Button(
    app,
    text="録音終了",
)
stop_button.pack()


# ラベルの作成と配置
label = tkinter.Label(
    app,
    width=5,
    height=1,
    text=0,
    font=("", 20)
)
label.pack()

# イベント処理の設定
start_button.bind("<ButtonPress>", start_button_click)
stop_button.bind("<ButtonPress>", stop_button_click)
app.protocol("WM_DELETE_WINDOW", quit_app)

#　スレッドの生成と開始
thread1 = threading.Thread(target=recording)
thread1.start()


# メインループ
app.mainloop()