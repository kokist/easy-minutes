import whisper

def transcription():
    model = whisper.load_model("small")
    # size	parameters
    # tiny	39M
    # base	74M
    # small	244M
    # medium	769M
    # large	1550M

    path ="./output.wav"
    # path = output_path #音声path
    result = model.transcribe(path, verbose=True, language='ja') # verboseはlogの表示
    # result = model.transcribe(path, verbose=True, language='ja',task="translate") 英語への翻訳
    # print(result)
    # print(result["text"])

    # ここで 。区切りのテキストを生成する
    sound2text = ""
    # print(len(result['segments']))
    for i in range(len(result['segments'])):
        sound2text += result['segments'][i]['text'] + "。"
    print(sound2text)
    
    return sound2text