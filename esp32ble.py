from machine import Pin
from machine import Timer
import ubluetooth


class ESP32_BLE:
    def __init__(self, type, device_id):
        self.name = 'HS-' + device_id
        self.service_uuid = '20010602-aaa1-1e11-0de' + type + '-' + device_id
        self.tx_uuid = '20010602-bbb1-1e11-0de' + type + '-' + device_id
        self.rx_uuid = '20010602-ccc1-1e11-0de' + type + '-' + device_id

        # using blue LED
        # blinking -> pairing, lighting -> connecting
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.is_ble_connected = False

        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        self.is_ble_connected = True
        self.led.value(1)  # blue LED lighting
        self.timer1.deinit()
        print('Connected!')

    def disconnected(self):
        self.is_ble_connected = False
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))
        print('Disconnected')

    def ble_irq(self, event, data):
        if event == 1:
            self.connected()

        elif event == 2:
            self.advertiser()
            self.disconnected()

        elif event == 3:
            buffer = self.ble.gatts_read(self.rx)
            ble_msg = buffer.decode('UTF-8').strip()

    def register(self):
        service = ubluetooth.UUID(self.service_uuid)
        tx = (ubluetooth.UUID(self.tx_uuid), ubluetooth.FLAG_NOTIFY)
        rx = (ubluetooth.UUID(self.rx_uuid), ubluetooth.FLAG_WRITE)

        ble_uart = (service, (tx, rx,))
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services((ble_uart, ))

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")

    def send(self):
        self.ble.gatts_notify(0, self.tx, device_id)
