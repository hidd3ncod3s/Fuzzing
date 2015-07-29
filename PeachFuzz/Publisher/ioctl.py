'''
Windows IOCTL publishers.

@author: 

'''

try:
	import time, sys, pywintypes, signal, os
	import win32file
except:
	pass
from Peach.publisher import Publisher

class IOCTL(Publisher):
	_devicename = None
	_devicehandle = None
	_methodFormat = None #  Not used
	_lastReturn = None   #  Not used
	
	def __init__(self, devicename):
		Publisher.__init__(self)
		self._devicename = devicename
		print "[DEBUG]Passed devicename: [%s]" % self._devicename
		# Disabling this
		#self.withNode = True
	
	def start(self):
		try:
			self._devicehandle = None
			self._devicehandle = win32file.CreateFile(self._devicename, 0, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, 0, None)
		
		except:
			print "Caught unkown exception opening device file [%s]" % sys.exc_info()[0]
			raise
	
	def stop(self):
		win32file.CloseHandle(self._devicehandle)
		self._devicehandle = None
	
	#def callWithNode(self, method, args, argNodes):
	def call(self, method, args):
		self._lastReturn = None
		
		'''
		BOOLEAN DeviceIoControl(
			HANDLE Device,             	// Code 
			DWORD IoControlCode,       	// Device handle
			LPVOID InBuffer,           	// Buffer TO driver
			DWORD InBufLen,            	// Size of InBuffer
			LPVOID OutBuffer,          	// Buffer FROM driver
			DWORD OutBufLen,           	// Size of OutBuffer
			LPDWORD BytesReturned,    	// Bytes output
			LPOVERLAPPED Overlapped 	// Overlapped struc
		);
		
		win32file.DeviceIoControl
			str/buffer = DeviceIoControl(Device, IoControlCode , InBuffer , OutBuffer , Overlapped )
		'''
		
		callStr =  "win32file.%s(" % str(method)
		callStr += "self._devicehandle,"
		
		#h = win32file.CreateFile(....)
		#windll.kernel32.DeviceIoControl(h.handle, ...)
		
		if len(args) > 0:
			for i in range(0, len(args)):
				if i == 0:
					callStr += "int(args[%d],16)," % i
					continue
				if args[i] == "":
					callStr += "None,"
				else:
					callStr += "args[%d]," % i
				#print "Arg : %s" % (args[i])
			callStr += "None)"
		else:
			callStr += ")"
		
		print "[DEBUG]callStr: %s" % callStr
		try:
			ret = None
			try:
				# OK. Send the IOCTL now.
				ret = eval(callStr)
				print "test"
			except:
				print "Caught unkown exception when sending IOCTL"
				raise
			return ret
			
		except NameError, e:
			print "Caught NameError on call [%s]" % e
			raise
		
		except:
			print "IOCTL::Call(): Caught unknown exception"
			raise
		
		return None

# end

