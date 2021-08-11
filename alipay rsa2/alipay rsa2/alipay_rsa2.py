from Crypto.Hash import  SHA256
from Crypto.Signature import PKCS1_v1_5 as Sig_pk
from Crypto.PublicKey import RSA
import base64
from urllib.parse import urlencode
from urllib import request
import json
import time
from alipay_cert import getsn
def sign_str(parm):
  #参数排序
    str_parm = ''
    for p in sorted(parm):
        if p in ['sign','signType'] or not parm[p]:
            continue
        elif isinstance(parm[p], dict):
            str_parm += str(p) + "=" + json.dumps(parm[p])+ "&"
        else: 
            str_parm += str(p) + "=" + str(parm[p]) + "&"
    str_parm=str_parm.replace(", ",",")
    str_parm=str_parm.replace(": ",":")
    return str_parm[:-1]

def sign_by_private_key(sortData,private_key):
    """
    ras2签名
    """
    # 获取私钥
    key = base64.b64decode(private_key)

    rsakey = RSA.importKey(key)
    # 根据sha算法处理签名内容  (此处的hash算法不一定是sha,看开发)
    data = SHA256.new(sortData.encode())

    # 私钥进行签名
    sig_pk = Sig_pk.new(rsakey)
    signer = sig_pk.sign(data)
    # 将签名后的内容，转换为base64编码
    result = base64.b64encode(signer)
    # 签名结果转换成字符串
    data = result.decode()
    return  data

def url_code(dict):
    keynum=len(dict["biz_content"])
    url=urlencode(dict)
    '''由于py库和网关的urlencode标准规范有些许不同，需自行替换编码'''
    url=url.replace("%27","%22",keynum*4)
    url=url.replace("+","%20",1)
    url=url.replace("+","")#若请求参数值中有空格要单独处理
    return url

def trade_precreate(out_trade_no,total_amount,subject):
    parm={"timestamp":"",
          "method":"alipay.trade.precreate",
          "app_id":"2021000117696885",#不同商家应用需更改
          "sign_type":"RSA2",
          "version":"1.0",
          "charset":"UTF-8",
          "biz_content":{"out_trade_no":"","total_amount":"","subject":""}}
    parm["biz_content"]["out_trade_no"]=str(out_trade_no)
    parm["biz_content"]["total_amount"]=str(total_amount)
    parm["biz_content"]["subject"]=str(subject)
    #获取时间
    time_tuple = time.localtime(time.time())
    if time_tuple[1]<10:
        month="0"+str(time_tuple[1])
    else :
        month=str(time_tuple[1])
    if time_tuple[2]<10:
        day="0"+str(time_tuple[2])
    else :
        day=str(time_tuple[2])
    if time_tuple[3]<10:
        hour="0"+str(time_tuple[3])
    else :
        hour=str(time_tuple[3])
    if time_tuple[4]<10:
        min="0"+str(time_tuple[4])
    else :
        min=str(time_tuple[4])
    if time_tuple[5]<10:
        sec="0"+str(time_tuple[5])
    else :
        sec=str(time_tuple[5])
    parm["timestamp"]=str(time_tuple[0])+"-"+month+"-"+day+" "+hour+":"+min+":"+sec
    return parm
    pass

def trade_query(out_trade_no):
    parm={"timestamp":"",
          "method":"alipay.trade.query",
          "app_id":"2021000117696885",#不同商家应用需更改
          "sign_type":"RSA2",
          "version":"1.0",
          "charset":"UTF-8",
          "biz_content":{"out_trade_no":""}}
    parm["biz_content"]["out_trade_no"]=str(out_trade_no)
    time_tuple = time.localtime(time.time())
    if time_tuple[1]<10:
        month="0"+str(time_tuple[1])
    else :
        month=str(time_tuple[1])
    if time_tuple[2]<10:
        day="0"+str(time_tuple[2])
    else :
        day=str(time_tuple[2])
    if time_tuple[3]<10:
        hour="0"+str(time_tuple[3])
    else :
        hour=str(time_tuple[3])
    if time_tuple[4]<10:
        min="0"+str(time_tuple[4])
    else :
        min=str(time_tuple[4])
    if time_tuple[5]<10:
        sec="0"+str(time_tuple[5])
    else :
        sec=str(time_tuple[5])
    parm["timestamp"]=str(time_tuple[0])+"-"+month+"-"+day+" "+hour+":"+min+":"+sec
    return parm
    pass

def trade_cancel(out_trade_no):
    parm={"timestamp":"",
          "method":"alipay.trade.cancel",
          "app_id":"2021000117696885",#不同商家应用需更改
          "sign_type":"RSA2",
          "version":"1.0",
          "charset":"UTF-8",
          "biz_content":{"out_trade_no":""}}
    parm["biz_content"]["out_trade_no"]=str(out_trade_no)
    time_tuple = time.localtime(time.time())
    if time_tuple[1]<10:
        month="0"+str(time_tuple[1])
    else :
        month=str(time_tuple[1])
    if time_tuple[2]<10:
        day="0"+str(time_tuple[2])
    else :
        day=str(time_tuple[2])
    if time_tuple[3]<10:
        hour="0"+str(time_tuple[3])
    else :
        hour=str(time_tuple[3])
    if time_tuple[4]<10:
        min="0"+str(time_tuple[4])
    else :
        min=str(time_tuple[4])
    if time_tuple[5]<10:
        sec="0"+str(time_tuple[5])
    else :
        sec=str(time_tuple[5])
    parm["timestamp"]=str(time_tuple[0])+"-"+month+"-"+day+" "+hour+":"+min+":"+sec
    return parm
    pass
if __name__ == '__main__':
    parm=trade_precreate(1628577848069,10.00,"subject_name")
    #parm=trade_query(1628577848069)
    #parm=trade_cancel(1628577848069)
    private_key_path=''
    if method:#加签方式
        #普通公钥
        private_key_path='private.txt'
        with open(private_key_path,'r') as f:
            private_key_string=f.read()
            pass
        pass
    else:
        #公钥证书
        private_key_path='cert_private.txt'
        with open(private_key_path,'r') as f:
            private_key_string=f.read()
            pass
        cert_list=getsn()
        parm["app_cert_sn"]=cert_list[0]
        parm["alipay_root_cert_sn"]=cert_list[1]
        pass
    #加签
    sort_data=sign_str(parm)
    data=sign_by_private_key(sort_data,private_key_string)
    parm["sign"]=data
    request_str="https://openapi.alipaydev.com/gateway.do?"+url_code(parm)
    #发送http请求
    response=request.urlopen(request_str)
    print(response.read().decode("utf-8"))
    pass