from googletrans import Translator

translator = Translator(service_urls=['translate.google.com'])


def translate_message(msg, dest='he'):

    return translator.translate(msg, dest=dest).text


if __name__ == '__main__':
    # "Hello my name is"
    print(translate_message('Привет меня зовут'))
    print(translate_message('Привет меня зовут', dest='en'))
