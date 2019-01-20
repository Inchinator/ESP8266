import network
import socket
import utime

class wlan_watchdog():
	server_address = ["89.163.145.12", 5802]
	wlan_address = ["XXXXXXXX", "XXXXXXXX"] #TODO: insert wlan address-info [ESSID, password]
	logfile = "wifi_watchdog.log"
	command = "ping"
	debug = True
	
	counter = 0
	endcounter = 999999
	active = True
	sta_if = network.WLAN(network.STA_IF)
	ap_if = network.WLAN(network.AP_IF)
	
	startlog = """
-------------------------------------
pingcounter - {}
"""
	successlog = """
ping was successful
round trip time = {}ms
-------------------------------------
"""
	errorlog = """
Ping failed ({})
count: {}
STA status: {}
	connected: {}
	cfg: {}
AP status: {}
	connected: {}
	cfg: {}	

Exception:
{}
-------------------------------------
"""
	
	def __init__(self):
		self.do_log("Execution start: \n" + str(self.get_time()) + " \n")
		self.init_wlan()
		self.watchdog_start()
		self.do_log("Execution end: \n" + str(self.get_time()) + " \n")
		self.debug_print("wlan_watchdog was killed")
	
	def init_wlan(self):
		if not self.sta_if.isconnected():
			self.debug_print("connecting to network...")
			self.sta_if.active(True)
			self.sta_if.connect(self.wlan_address[0], self.wlan_address[1])
			while not self.sta_if.isconnected():
				pass
			self.debug_print("network config:".format(self.sta_if.ifconfig()))
	
	
	def do_log(self, logdata):
		f = open(self.logfile, "a+")
		f.write(logdata)
		f.close()


	def log_header(self):
		self.do_log(self.startlog.format(self.counter))


	def log_success(self, rtt):
		self.do_log(self.successlog.format(rtt))


	def log_error(self, exception):
		self.do_log(self.errorlog.format(self.get_time(), self.counter, self.sta_if.active(), self.sta_if.isconnected(), self.sta_if.ifconfig(), self.ap_if.active(), self.ap_if.isconnected(), self.ap_if.ifconfig(), exception))
	
	
	def debug_print(self, message):
		if (self.debug): print(message)
	
	
	def get_time(self):
		time = utime.localtime()
		return "{}.{} - {}:{}:{}".format(time[2], time[1], time[3], time[4], time[5])
	
	
	def kill(self):
		self.active = False
	
	
	def watchdog_start(self):
		while self.active:
			self.counter += 1 
			self.debug_print("pinging... #" + str(self.counter))
			#self.log_header()
			
			try:
				clientsocket = socket.socket()
				clientsocket.connect(self.server_address)
				starttime = utime.ticks_ms()
				clientsocket.send(self.command.encode("ascii"))
				data = clientsocket.recv(1024)
				endtime = utime.ticks_ms()
				#self.log_success(endtime-starttime)
				self.debug_print("successfull ping ({}ms)".format(endtime-starttime))
				
			except Exception as e:
				self.log_error(e)
				self.debug_print("Exception on pinging")
			
			finally:
				clientsocket.close()
				
			utime.sleep_ms(10000)
			if(self.counter >= self.endcounter): self.kill()
		
