#!/usr/bin/python3
from datetime import datetime
import websocket
import json
import requests

deviceId = 999999
wfToken = your token

ws = websocket.WebSocket()
try:
    ws.connect("wss://ws.weatherflow.com/swd/data?token={}".format(wfToken))
    ws.send('{"type":"listen_start", "device_id":{}, "id": "Tempest"}'.format(deviceId))
    while True:
        print("Waiting for data")
        data = ws.recv()
        d = json.loads(data)
        print(d)
        print()
        if d['type'] == "obs_st":
            print("Device ID: " + str(d['device_id']))
            for o in d['obs']:
                print("Epoch: " + str(o[0]) + " " + str(datetime.fromtimestamp(o[0])))
                print("Wind Lull: " + str(o[1]) + "m/s")
                print("Wind Avg: " + str(o[2]) + "m/s")
                print("Wind Gust: " + str(o[3]) + "m/s")
                print("Wind Direction: " + str(o[4]) + chr(176))
                print("Wind Sample Interval: " + str(o[5]) + " seconds")
                print("Station Pressure: " + str(o[6]) + "MB")
                print("Air Temperature: "  + str(o[7]) + "C")
                print("Relative Humidity: " + str(o[8]) + "%")
                print("Illuminance: " + str(o[9]) + " Lux")
                print("UV: " + str(o[10]) + " Index")
                print("Solar Radiation: " + str(o[11]) + " W/m^2")
                print("Rain Accumulated: " + str(o[12]) + "mm")
                print("Precipitation Type: " + str(o[13]) + " 0 = none, 1 = rain, 2 = hail")
                print("Lightning Strike Avg Distance: " + str(o[14]) + "km")
                print("Lightning Strike Count: " + str(o[15]))
                print("Battery: " + str(o[16]) + " Volts")
                print("Report Interval: " + str(o[17]) + " Minutes")
                print("Local Daily Rain Accumulation: " + str(o[18]) + "mm")
                print("Rain Accumulated Rain Check: " + str(o[19]) + "mm")
                print("Local Daily Rain Accumulation Rain Check: " + str(o[20]) + "mm")
                print("Precipitation Analysis Type: " + str(o[21]) + " 0 = none, 1 = Rain Check on, 2 = Rain Check off")
            print("Pressure Trend: " + d['summary']['pressure_trend'])
            print("Strike Count 1h: " + str(d['summary']['strike_count_1h']))
            print("Strike Count 3h: " + str( d['summary']['strike_count_3h']))
            print("Strike Last Dist: " + str(d['summary']['strike_last_dist']))
            print("Strike Last Epoch: " + str(d['summary']['strike_last_epoch']))
            print("Precip Total 1h: " + str(d['summary']['precip_total_1h']))
            print("Precip Accum Yesterday: " + str(d['summary']['precip_accum_local_yesterday']))
            print("Precip Accum Yesterday Rain Check: " + str(d['summary']['precip_accum_local_yesterday_final']))
            print("Precip Ananlysis Type Yesterday: " + str(d['summary']['precip_analysis_type_yesterday']))
            print("Precip Minutes Yesterday: " + str(d['summary']['precip_minutes_local_yesterday']))
            print("Precip Minutes Today: " + str(d['summary']['precip_minutes_local_day']))
            print("Feels Like: " + str(d['summary']['feels_like']))
            print("Heat Index: " + str(d['summary']['heat_index']))
            print("Wind Chill: " + str(d['summary']['wind_chill']))
            print("Air Density: " + str(d['summary']['air_density']))
            print("Dew Point: " + str(d['summary']['dew_point']))
            print("Wet Bulb Temp: " + str(d['summary']['wet_bulb_temperature']))
            print("Web Bulb Globe Temp: " + str(d['summary']['wet_bulb_globe_temperature']))
            print()
            try:
                i = 0
                for m in d['summary']['raining_minutes']:
                    print("Rain " + str(i) + " hours ago: " + str(m))
                    i = i + 1
            except KeyError:
                pass
        elif d['type'] == "evt_precip":
            print("****Precipitation Event*****")
        elif d['type'] == "evt_strike":
            print("****Lightning Strike****")
            print("Strike Epoch: " + str(d['evt'][0]))
            print("Strike Dist: " + str(d['evt'][1]) + "km")
            
except KeyboardInterrupt:
    print("Exiting")
    ws.send('{"type":"listen_stop", "device_id":{}, "id": "Tempest"}'.format(deviceId))
    ws.close()
