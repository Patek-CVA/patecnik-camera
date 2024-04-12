import network
from microdot import Microdot, Request, cors
from microdot.microdot import MultiDict

import camera

ap_if: network.WLAN = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(
    essid='Páteční kamera',
    password='qwertyuiop',
    authmode=network.AUTH_WPA_WPA2_PSK
)

print(f'ip: {ap_if.ifconfig()[0]}')

app: Microdot = Microdot()
cors.CORS(app, '*')


class Stream:
    def __aiter__(self):
        return self

    async def __anext__(self):
        buf: bool | bytes = camera.capture()
        while not buf:
            pass
        return b'Content-Type: image/jpeg\r\n\r\n' + \
            buf + b'\r\n--frame\r\n'

    async def aclose(self):
        print('Stopping video stream')


@app.route('/video')
async def video(request: Request):
    args: MultiDict = request.args
    resolution: str = args.get('res')
    camera.framesize(getattr(camera, 'FRAME_' + resolution))
    return Stream(), 200, {
        'Content-Type': 'multipart/x-mixed-replace; boundary=frame'
    }


camera.deinit()
camera.init(
    0,
    format=camera.JPEG,
    fb_location=camera.PSRAM
)
camera.framesize(camera.FRAME_HD)

app.run(port=80)
