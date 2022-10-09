# 功能: ap模式下配置ssid和key

import network

ap = network.WLAN(network.AP_IF)
ap.config(ssid='ap', security=4, key='password')
ap.active(True)
