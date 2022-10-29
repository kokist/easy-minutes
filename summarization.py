from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

def summarize(sound2text):
    document = sound2text
    # 自動要約のオブジェクトを生成
    auto_abstractor = AutoAbstractor()
    # トークナイザー（単語分割）にMeCabを指定
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # 文書の区切り文字を指定
    auto_abstractor.delimiter_list = ["。", "\n"]
    # キュメントの抽象化、フィルタリングを行うオブジェクトを生成
    abstractable_doc = TopNRankAbstractor()
    # 文書の要約を実行
    result_dict = auto_abstractor.summarize(document, abstractable_doc)
    # print(result_dict["summarize_result"])
    #要約結果の取り出し
    # for x in result_dict["summarize_result"]:
    #     print(x)
    # 行番号と重要度
    # print(result_dict['scoring_data'])
    return result_dict