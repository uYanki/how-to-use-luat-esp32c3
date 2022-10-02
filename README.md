## how-to-use-luat-esp32c3

https://wiki.luatos.com/chips/esp32c3/index.html

经典款：以USB-TTL的方式连接ESP32C3芯片。（CH343P芯片）

新款：USB直连ESP32C3芯片。

#### 板载资源

* 板载 4MB Flash，最高支持 16MB Flash。

更换 Flash 后，需更改分区表，并且重新编译固件，再烧录固件。

https://wiki.luatos.com/chips/esp32c3/change_flash.html

* 板载 2 颗用户 LED：

| LED  | GPIO | DESC       |
| ---- | ---- | ---------- |
| D4   | IO12 | 高电平有效 |
| D5   | IO13 | 高电平有效 |

#### 开发方式

|             | 经典款 | 新款 |
| ----------- | ------ | ---- |
| ESP-IDF     | √      | √    |
| LuatOS      | √      | ×    |
| Micropython | √      | √    |
| Arduino     | √      | √    |

新款若要使用 LuatOS，需外接 USB-TTL 模块连接到 UART0，以进行刷机和查看日志。

| GPIO | FUNCTION |
| ---- | -------- |
| IO20 | UART0_RX |
| IO21 | UART0_TX |
| IO19 | USB_D+   |
| IO18 | USB_D-   |

#### 注意事项

* BOOT（IO09）管脚上电前不能下拉，否则芯片会自动进入下载模式。

* GPIO11 默认为 SPI flash 的 VDD 引脚，需按以下操作配置后才能作为 GPIO 使用。

  注：更改后不能复原，因为是设置熔丝位，而不是寄存器。

```
1.pip install esptool
2.espefuse.py -p COMx burn_efuse VDD_SPI_AS_GPIO 1
3.BURN
```

* IO08 管脚为低电平时，不能使用串口进行下载。
* 为增加可用 GPIO 数量，开发板选择采用 2 线 SPI 的 DIO 模式，因此烧录固件时需选择 DIO 模式。（Arduino - flash mode - DIO mode）

