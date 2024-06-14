import json
import network
import uasyncio
from microdot import Microdot, Request, cors
from microdot.websocket import with_websocket, WebSocket
import ubinascii

import camera

print('Connecting to Pátečník WIFI...')
sta_if: network.WLAN = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Pátečník', 'qwertyuiop')
while not sta_if.isconnected():
    pass
print('Connected')

brain_ip: str = '192.168.4.1'
ip: str = '192.168.4.69'
ifconfig: tuple[str, str, str, str] = (ip, '255.255.255.0', brain_ip, brain_ip)
sta_if.ifconfig(ifconfig)
print(f'ip: {sta_if.ifconfig()[0]}')

app: Microdot = Microdot()
cors.CORS(app, '*')


@app.route('/')
@with_websocket
async def video(request: Request, websocket: WebSocket):
    print('established connection')
    message = await websocket.receive()
    print(message)
    while True:
        await uasyncio.sleep(1 / 50)
        image: bytes | bool = False
        while not image:
            image = camera.capture()
        base64: str = ubinascii.b2a_base64(image, newline=False).decode('utf-8')
        base64 = 'data:image/jpg;base64, ' + base64
        response: dict = {
            'endpoint': 'live-feed',
            'data': {
                'image': base64
            }
        }
        await websocket.send(json.dumps(response))


camera.deinit()
camera.init(
    0,
    format=camera.JPEG,
    fb_location=camera.PSRAM
)
camera.framesize(camera.FRAME_CIF)

app.run(port=80)
