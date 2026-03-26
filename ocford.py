import requests

app_id = "5e4a7b36"
app_key = "242719793ddf31b89e4a5bf6e1284ed2"
language = "en-gb"

def getDefinitions(word_id):
    url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/{language}/{word_id.lower()}"
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    res = r.json()

    if 'error' in res:
        print(f"Xatolik: {res['error']}")
        return False

    output = {}

    try:
        senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        definitions = [sense['definitions'][0] for sense in senses if 'definitions' in sense]
        output['definitions'] = "\n".join(definitions)
    except (KeyError, IndexError):
        output['definitions'] = "Ta’rif topilmadi."

    try:
        pronunciations = res['results'][0]['lexicalEntries'][0].get('pronunciations', [])
        for p in pronunciations:
            if 'audioFile' in p:
                output['audio'] = p['audioFile']
                break
        else:
            output['audio'] = "Audio mavjud emas."
    except (KeyError, IndexError):
        output['audio'] = "Audio topilmadi."

    return output

if __name__ == '__main__':
    from pprint import pprint as print
    print(getDefinitions("apple"))
