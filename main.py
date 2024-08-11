import ubinascii
import ujson
import network, urequests
import machine
from machine import Pin, ADC, Timer
from time import sleep
from math import floor
import esp32ble

# function: setting battery config
def watching_battery(timer):
    sleep(2)
    global total
    global current_battery
    global temp_battery
    global idel
    global count
    global current_battery_level
    count += 1
    print(count)
   
    for x in range(20):
       total = total + battery.read()  # 取20次
    
    total = floor(total / 20 * 1.8 / 100)  # 調至適合範圍
    if (total == temp_battery):  # 穩定
        idel = idel + 1
        if (idel == 3):
            idel = 0
            current_battery = temp_battery
    else:
        idel = 0
        temp_battery = total
            
    if (current_battery >= 54):
        current_battery_level = 5
    if (current_battery >= 50 and current_battery < 54):
        current_battery_level = 4
    if (current_battery >= 46 and current_battery < 50):
        current_battery_level = 3
    if (current_battery >= 41 and current_battery < 46):
        current_battery_level = 2
    if (current_battery >= 0 and current_battery < 41):
        current_battery_level = 1
        
    current_battery_level_json = ujson.dumps({'UUID': unique_id, 'Battery': current_battery_level})
    battery_send = urequests.post(server_url + '/renewBattery', data=current_battery_level_json)  # remember to confirm IP address
    battery_send.close()

# environment vars (初次使用或更換環境時，請務必確認)
model = 1   # model 1: controlled by itself; model 2: controlled by management system
server_url = 'http://192.168.0.100:5000'  # has to set if it's model 2
wifi_id = 'Hello Stranger'  # has to set if it's model 2
wifi_pwd = '00000000'  # has to set if it's model 2
battery_check_period = 600000 # has to set if it's model 2, default: 600,000 ms = 10 minutes

# get device unique ID
unique_id = ubinascii.hexlify(machine.unique_id()).decode()  # bytes(2) -> bytes(16) -> string
print('device unique ID: ' + unique_id)

# BLE init & start broadcasting
ble = esp32ble.ESP32_BLE('2', unique_id)
if (ble.is_ble_connected):
    ble.send()

# run if it's model 2
if (model == 2):
    # Wi-Fi connecting
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('connecting to network...')
    wlan.connect(wifi_id, wifi_pwd)
    while not wlan.isconnected():
        pass
    print('network config:', wlan.ifconfig())

    # enroll new device
    post_data_json = ujson.dumps({'UUID': unique_id, 'tx': ble.tx_uuid, 'rx': ble.rx_uuid, 'nus': ble.service_uuid})  # obj -> JSON string
    res = urequests.post(server_url + '/newDevice', data=post_data_json)
    res.close()


    timer = Timer(-1)  # for timer function
    current_battery = 54  # the accurate battery value from current run
    temp_battery = 54  # the last battery value
    current_battery_level = 5  # from 1 to 5
    idel = 0  # for battery accuracy
    total = 0  # the battery value from current run
    count = 0
    battery = ADC(Pin(34))
    battery.atten(ADC.ATTN_11DB)  # full range of 3.3v
    timer.init(period=battery_check_period, mode=Timer.PERIODIC, callback=watching_battery)
