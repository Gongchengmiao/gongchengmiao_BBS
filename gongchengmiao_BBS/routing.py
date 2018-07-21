# channel_routing = {
#
# }

from channels.routing import route, include
from channels.staticfiles import StaticFilesConsumer
import consumers

channel_routing = [
    route('http.request', StaticFilesConsumer),
    route('websocket.connect', consumers.ws_connect),
    route('websocket.receive', consumers.ws_receive),
    route('websocket.disconnect', consumers.ws_disconnect),
]
