
import json
#from typing import Text
import requests
from requests.auth import HTTPBasicAuth
import re
from bs4 import BeautifulSoup
import pandas
import time


m = "1620202405:AAHpyroIAGtJPhQEf_bMc5cyIvdvTVpPMio"
    
#actions("cancel",None,'cancel')
#time.sleep(10)
#session.hold()
def FortinetSession():
    FortinetSession = "http://172.16.14.97/nagios/cgi-bin/extinfo.cgi?type=2&host=DC_Fortinet_27.5&service=FortinetCluster+Sesstions"
    r = requests.get(FortinetSession,auth=HTTPBasicAuth('vanhanh', 'vanhanh@2016'))
    session = re.findall(r'\d{5,9}',r.text)
    text = "Báo cáo hệ thống:h123443221e\n- Login: OK\n- CCU: %s \n- Fortinet session: %s\n- Kafka: %s \n- Rabbit: %s \n- Email: OK " %(getCCU(),session[0],AllKafka(),Rabbit())
    return text

def crawData(url):
    r = requests.get(url,auth=HTTPBasicAuth('vanhanh', 'vanhanh@2016'))
    html = BeautifulSoup(r.text, 'html.parser')
    tb = html.find('table',{'class':'status'})
    td = tb.prettify()
    df = pandas.read_html(td)
    return df[0]

def checkData(table):
    err = {table['Host'][0]:[]}
    idx = table.index[table['Status']!='OK']
    for i in idx:
        a = {
            'Service': table['Service'][i],
            'State': table['Status'][i],
            'Info': table['Status Information'][i]
        }
        err.setdefault(table['Host'][0],[])
        err[table['Host'][0]].append(a)
    return err

def returnResult(err,host):
    if err[host]:
        return json.dumps(err,indent=3,ensure_ascii=False)
    else:
        return 'OK'

def Rabbit():
    RabbitURL = "http://172.16.14.97/nagios/cgi-bin/status.cgi?host=DC_RabbitMQ_14.28"
    # RabbitURL="http://172.16.14.97/nagios/cgi-bin/status.cgi?host=DC_Monitor_14.97"
    table = crawData(RabbitURL)
    err = checkData(table)
    return returnResult(err,table['Host'][0])

def Kafka(a):
    KafkaURL = "http://172.16.14.97/nagios/cgi-bin/status.cgi?host=DC_Server_Lixi2021_Kafka_55.%s" %(a)
    table = crawData(KafkaURL)
    err = checkData(table)
    return returnResult(err,table['Host'][0])

def AllKafka():
    url = [175,176,177,178,179]
    err= ""
    for i in url:
        if Kafka(i)!='OK':
            dicttest  = json.loads(Kafka(i))
            for key in dicttest.keys():
               message =  "\n" + key + ": \n" + "    " + dicttest[key][0]["Service"]+ "-" + dicttest[key][0]["Info"] + "\n"
               err = err + message
    if err:
        return err
      #return json.dumps(err,indent=3,ensure_ascii=False,)
	#return 'test'
    else:
        return "OK"

def getCCU():
    try:
        CCU = "http://45.76.158.15/nagios/cgi-bin/extinfo.cgi?type=2&host=MOMO_APP_v2&service=MOMOv2+Total+CCU"
        r = requests.get(CCU,auth=HTTPBasicAuth('vanhanh', 'v@nh@nh@2017'))
        session = re.findall(r'\=\d{4,9}',r.text)
        return session[0][1:]
    except:
        return "Check Manualy Please!"

link = "https://api.telegram.org/bot%s/sendMessage?chat_id=-715246096&text=%s" %(m,FortinetSession())
a = requests.get(link)
