
from flask import Flask, render_template,flash,request
import requests
import json,socket
import geoip2.webservice,geoip2.database
from random import random
from pygeocoder import Geocoder
import gspread
import IP2Location
from oauth2client.service_account import ServiceAccountCredentials
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
    return render_template('index.html')
@app.route('/number',methods = ['POST']) 
def number():
    data = request.form["num"]
    # random_number = random.randint(1, 1000)
    print(data)
    """  Function To Print GeoIP Latitude & Longitude """ 

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('UserLocationService.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('UserLocation').sheet1
    telemedicine = sheet.get_all_values()
    print(telemedicine[0][0])
       
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +str(telemedicine[0][0]) + '.json')
    geo_data = geo_request.json()
    print({'latitude': geo_data['latitude'], 'longitude': geo_data['longitude']})
    coordinates =(geo_data['latitude'], geo_data['longitude']) 
    ro = phonenumbers.parse(data,"RO")
    # location = Geocoder.reverse_geocode(float(geo_data['latitude']),float(geo_data['longitude']))
    # print(location.city)
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name)


    carr = carrier.name_for_number(ro, "en")
    timez = timezone.time_zones_for_number(ro)
    geo = geocoder.description_for_number(ro, "en")
    print(carr)
    print(timez)
    print(host_ip)
    print(request.remote_addr)
    sender = reverseGeocode(coordinates)
    print(list(sender[0].values())[2])
    d = "https://docs.google.com/spreadsheets/d/191xprUg90E12ms29X1kZZokhslvy8-nr6ewn3qQf1zM/edit?usp=sharing"
    print(d)
        # get response
    response = sendPostRequest(URL, 'EAAWTVR19VMQOWB6TGOU0KJX1LQ981VT', 'HIQ247XV8GRQ7Z31','stage', data, 'SMSIND',d)
    # print(response.text)
        # get response
    # response1 = sendGetRequest(URL, 'VX456E299QDCERQ7BJV1YXO8IVS6N4ES', 'S3J2ROXIS9J5ZPKP', 'stage', '7303820799', 'SMSIND', 'message-text' )
    """
    Note:-
        you must provide apikey, secretkey, usetype, mobile, senderid and message values
        and then requst to api
    """
    res = list(sender[0].values())[2]+','+list(sender[0].values())[3]+','+list(sender[0].values())[4]
    # print response if you want
    return res

if __name__ == '__main__': 
    app.run(debug=True)  