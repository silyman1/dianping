# -*- coding: utf-8 -*-
import requests

def geocodeG(address):
    par = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    GPS=answer['geocodes'][0]['location'].split(",")
    return GPS[0],GPS[1]