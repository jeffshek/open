import json
import ssl

from websocket import create_connection

"""
dpy runscript writeup_mock_ws_listeners
"""


def run():
    ws = create_connection(
        "wss://open.senrigan.io/ws/async/writeup/text_generation/session/test/",
        sslopt={"cert_reqs": ssl.CERT_NONE},
        timeout=15,
    )

    valid_data = {"text0": "Yep", "prompt": "Yep", "message_type": "new_request"}
    to_send = json.dumps(valid_data)
    ws.send(to_send)

    result2 = ws.recv()
    print(result2)
    ws.close()
