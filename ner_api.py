import json
import requests
import string


API_URL = "https://api-inference.huggingface.co/models/hatmimoha/arabic-ner"


def read_ai_credentials(creds_file: str = "ai_credentials.json"):
    with open(creds_file, 'r') as json_file:
        return json.load(json_file)


def query(payload):
    response = requests.post(API_URL, headers=read_ai_credentials(), json=payload)
    return response.json()


def raw_ner_from_message(msg):
    if not is_arabic_sentence(msg):
        return []
    return query({
        "inputs": msg,
    })


def ner_from_message(msg):
    res = {}
    for item in raw_ner_from_message(msg):
        if item['entity_group'] not in res.keys():
            res[item['entity_group']] = [item['word']]
        else:
            res[item['entity_group']] = res[item['entity_group']] + [item['word']]
    return res


def is_arabic_char(ch):
    return ('\u0600' <= ch <= '\u06FF' or
            '\u0750' <= ch <= '\u077F' or
            '\u08A0' <= ch <= '\u08FF' or
            '\uFB50' <= ch <= '\uFDFF' or
            '\uFE70' <= ch <= '\uFEFF' or
            '\U00010E60' <= ch <= '\U00010E7F' or
            '\U0001EE00' <= ch <= '\U0001EEFF')


def is_arabic_sentence(sentence, prob=0.9):
    # At least prob of the sentence is arabic
    return sum(is_arabic_char(c) or c in string.punctuation or c in string.whitespace for c in sentence) > \
        prob * len(sentence)


def main():
    print(ner_from_message('و هذا ما نفاه المعاون السياسي للرئيس نبيه بري ، النائب علي حسن خليل'))
    print(ner_from_message('رغم الهدنة .. معارك قره باغ متواصلة وأذربيجان تعلن سيطرتها على مزيد من القرى'))
    # Will return nothing since not arabic
    print(ner_from_message('Hello my name is enigo montoia'))
    print(ner_from_message('שלום לכם ילדים וילדות'))


if __name__ == '__main__':
    main()
