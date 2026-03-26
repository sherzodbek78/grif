import requests

app_id = "5e4a7b36"
app_key ="242719793ddf31b89e4a5bf6e1284ed2"
language = "en-gb"

def getDefinitions(worl_id):
    url = "https://od-api-sandbox.oxforddictionaries.com/api/v2" + language +"/" + worl_id.lower()
    r = requests.get(url, headers={"app_id": app_id, "app_key":app_key})
    res = r.json()
    if 'error' in res.keys():
        return False

    output ={}
    senses = res['results'][0]['entries'][0]['entries'][0]['senses']
    definitions =[]
    for sense in senses:
        definitions.append(f"{sense['definition'][0]}")
    output['definitions'] = "\n".join(definitions)

    if res['results'][0]['lexicalEntries'][0]['entries'][0]['prouniciations'][0].get('audioFile'):
        output['audio'] = res['results'][0]['lexicalEntries'][0]['entries'][0]['prouniciations'][0]['audiofFile']

    return output

if __name__=='__main__':
    from  pprint import pprint as print
    print(getDefinitions("Great Britain"))
    print(getDefinitions('america'))
