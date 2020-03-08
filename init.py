
from flask import Flask, render_template,flash,request
import requests
import json,socket
from random import random
import reverse_geocoder as rg 
import phonenumbers
from phonenumbers import carrier,timezone,geocoder
import pprint

URL = 'https://www.sms4india.com/api/v1/sendCampaign'
URL2 = 'https://www.sms4india.com/api/v1/sendCampaign'


app = Flask(__name__, template_folder='app/templates')    

def reverseGeocode(coordinates): 
    result = rg.search(coordinates) 
      
    # result is a list containing ordered dictionary. 
    # pprint.pprint(result)
    return result

def sendGetRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.get(reqUrl, req_params)
# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)

@app.route('/')   
def main():
    """Say hello"""
    return render_template('map.html')
@app.route('/number',methods = ['POST']) 
def number():
    data = request.form["num"]
    # random_number = random.randint(1, 1000)
    print(data)
    """  Function To Print GeoIP Latitude & Longitude """
    
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +my_ip + '.json')
    geo_data = geo_request.json()
    print({'latitude': geo_data['latitude'], 'longitude': geo_data['longitude']})
    coordinates =(geo_data['latitude'], geo_data['longitude']) 
    ro = phonenumbers.parse(data,"RO")
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name) 
    # rest = phonenumbers.PhoneMetadata.load_all()
    # ro_number = phonenumbers.parse(data, "RO")
    carr = carrier.name_for_number(ro, "en")
    timez = timezone.time_zones_for_number(ro)
    geo = geocoder.description_for_number(ro, "en")
    print(carr)
    print(timez)
    print(geo)
    print(request.remote_addr)
    sender = reverseGeocode(coordinates)
    map = './map.html'
    d = "http://bit.ly/2Tz25pN"
    print(d)
        # get response
    response = sendPostRequest(URL, 'EAAWTVR19VMQOWB6TGOU0KJX1LQ981VT', 'HIQ247XV8GRQ7Z31','stage', data, 'SMSIND',"Bas Kar kinni Gallan Krni aa")
    # print(response.text)
        # get response
    # response1 = sendGetRequest(URL, 'VX456E299QDCERQ7BJV1YXO8IVS6N4ES', 'S3J2ROXIS9J5ZPKP', 'stage', '7303820799', 'SMSIND', 'message-text' )
    """
    Note:-
        you must provide apikey, secretkey, usetype, mobile, senderid and message values
        and then requst to api
    """
    # print response if you want
    return response.text 

if __name__ == '__main__': 
    app.run(debug=True)  