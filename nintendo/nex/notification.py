
from nintendo.common import signal
from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class NotificationEvent(common.Structure):
	def load(self, stream):
		self.pid = stream.uint()
		self.type = stream.u32()
		self.param1 = stream.uint()
		self.param2 = stream.uint()
		self.text = stream.string()
		
		if self.version >= 0:
			self.param3 = stream.uint()

			
class NotificationHandler:
	process_notification_event = signal.Signal()


class NotificationServer:

	METHOD_PROCESS_NOTIFICATION_EVENT = 1

	PROTOCOL_ID = 0xE

	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NOTIFICATION_EVENT: self.process_notification_event
		}
		self.handler = NotificationHandler()
	
	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NotificationServer received request with unsupported method id: %i", method_id)

	def process_notification_event(self, client, call_id, method_id, stream):
		#--- request ---
		event = stream.extract(NotificationEvent)
		
		logger.info("NotificationServer.process_notification_event(%i, %i)", event.type, event.pid)
		self.handler.process_notification_event(event)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)
