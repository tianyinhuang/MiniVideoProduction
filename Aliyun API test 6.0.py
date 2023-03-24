import http.client
import urllib.parse
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

#creat token for Aliyun syAudio
def get_token():
   # 创建AcsClient实例
   client = AcsClient(
      "AppIDXXXXXXXXXXXXXX,
      "AppkeyXXXXXXXXXXXXX",
      "servercode"
   );

   # Create request and set paremeters 创建request，并设置参数。
   request = CommonRequest()
   request.set_method('POST')
   request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
   request.set_version('2019-02-28')
   request.set_action_name('CreateToken')

   try : 
      response = client.do_action_with_exception(request)
      print(response)

      jss = json.loads(response)
      if jss.has_key('Token') and jss['Token'].has_key('Id'):
         token = jss['Token']['Id']
         expireTime = jss['Token']['ExpireTime']
         print("token = " + token)
         print (token)
         print("expireTime = " + str(expireTime))
   except Exception as e:
      print(e)

   token= jss.get('Token', {}).get('Id', '')

   print (token)
   return token

# GETrequest Aliyun syAudio
def processGETRequest(appKey, token, text, audioSaveFile, format, sampleRate) :
    host = 'nls-gateway-cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'
    # 设置URL请求参数
    url = url + '?appkey=' + appKey
    url = url + '&token=' + token
    url = url + '&text=' + text
    url = url + '&format=' + format
    url = url + '&sample_rate=' + str(sampleRate)
    print(url)

    conn = http.client.HTTPSConnection(host)
    conn.request(method='GET', url=url)
    # Process return data 处理服务端返回的响应。
    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status ,response.reason)
    contentType = response.getheader('Content-Type')
    print(contentType)
    body = response.read()
    if 'audio/mpeg' == contentType :
        with open(audioSaveFile, mode='wb') as f:
            f.write(body)
        print('The GET request succeed!')
    else :
        print('The GET request failed: ' + str(body))
    conn.close()

def processPOSTRequest(appKey, token, text, audioSaveFile, format, sampleRate, enable_subtitle) :
    host = 'nls-gateway-cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'
    # set HTTPS Headers 设置HTTPS Headers。
    httpHeaders = {
        'Content-Type': 'application/json'
        }
    # set HTTPS body 设置HTTPS Body。
    body = {'appkey': appKey, 'token': token, 'text': text, 'format': format, 'sample_rate': sampleRate, 'enable_subtitle': True}
    body = json.dumps(body)
    print('The POST request body content: ' + body)
    conn = http.client.HTTPSConnection(host)
    conn.request(method='POST', url=url, body=body, headers=httpHeaders)
    # process return 处理服务端返回的响应。
    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status ,response.reason)
    contentType = response.getheader('Content-Type')
    print(contentType)
    body = response.read()
    if 'audio/mpeg' == contentType :
        with open(audioSaveFile, mode='wb') as f:
            f.write(body)
        print('The POST request succeed!')
    else :
        print('The POST request failed: ' + str(body))
    conn.close()
    

file = open("texttts.txt", "r", encoding="utf-8")
appKey = 'AppkeyXXXXXXXXXX'
token = get_token()
text = file.read()
# Use the RFC 3986 specification for urlencode encoding. 采用RFC 3986规范进行urlencode编码。
textUrlencode = text
textUrlencode = urllib.parse.quote_plus(textUrlencode)
textUrlencode = textUrlencode.replace("+", "%20")
textUrlencode = textUrlencode.replace("*", "%2A")
textUrlencode = textUrlencode.replace("%7E", "~")
print('text: ' + textUrlencode)
audioSaveFile = 'syAudio.mp3'
format = 'mp3'
sampleRate = 16000
# GET request format请求方式
processGETRequest(appKey, token, textUrlencode, audioSaveFile, format, sampleRate)
# POST request format请求方式
#processPOSTRequest(appKey, token, text, audioSaveFile, format, sampleRate, enable_subtitle)
