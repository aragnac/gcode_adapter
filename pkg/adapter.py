#!/usr/bin/env python
"""octopi adapter for Mozilla IoT Gateway."""

import io
import json

from gateway_addon import Adapter
from lib.octoclient.client import OctoClient
from .device import GDevice

_TIMEOUT = 3
_URL = 'http://192.168.254.120'
_APIKEY = '10BF52B18BEC4E75B87193CF6BB1D45C'
_PORT = '/dev/ttyACM0'
_BAUDRATE = 115200

class GcodeAdapter(Adapter):
    def __init__(self, verbose=False):
        """Initialize the object.
        verbose -- whether or not to enable verbose logging"""

        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'GcodeAdapter',
                         'GcodeAdapter',
                         verbose=verbose)

        with open('things.json') as json_data:
            deviceDescription = json.load(json_data)

        self.Port = _PORT
        self.Baudrate = _BAUDRATE
        self.pairing = False
        self.pairDevice(deviceDescription['name'], deviceDescription)
        self.startPairing()



    def addDevice(self, deviceId, deviceDescription):
        """
        * Add a MockDevice to the MockAdapter

        * @param {String} deviceId ID of the device to add.
        * @return {Promise} which resolves to the device added.
        """
        if deviceId in self.devices:
            print('Device: ' + deviceId + ' already exists.')
            return False
        else:
            device = GDevice(self, deviceId, deviceDescription, self.octopi)
            self.handle_device_added(device)
            print('Device: ' + deviceId + 'added')
            return True

    def removeDevice(self, deviceId):
        """
        :param deviceId: deviceId ID of the device to remove.
        :return:
        """
        device = self.devices[deviceId]
        if device is not None:
            self.handle_device_removed(device)
            return True
        else:
            print('Device: ' + deviceId + ' not found.')
            return False

    def pairDevice(self, deviceId, deviceDescription):
        self.pairDeviceId = deviceId
        self.pairDeviceDescription = deviceDescription

    def unpairDevice(self, deviceId):
        self.unpairDeviceId = deviceId

    def startPairing(self):
        print('GcodeAdapter:', self.name, 'id', self.pairDeviceId, 'pairing started')
        if(self.pairDeviceId):
            #Initialise object for connection with Octoprint
            self.octopi = OctoClient(url=_URL, apikey=_APIKEY)
            #Get connection Info
            string = self.octopi.connection_info()
            currentstate = string["current"]["state"]

            # Conection to the octoprint server
            if currentstate != "operational":
                self.octopi.connect(port=_PORT, baudrate=_BAUDRATE, save='true', autoconnect='true')
                print('Connected !')
            else:
                print('Already connected')

            deviceId = self.pairDeviceId
            deviceDescription = self.pairDeviceDescription
            self.pairDeviceId = None
            self.pairDeviceDescription = None
            if self.addDevice(deviceId, deviceDescription):
                print('GcodeAdapter: device:', deviceId, 'was paired.')
            else:
                print('GcodeAdapter: unpairing', deviceId, 'failed')

    def cancelPairing(self):
        print('GcodeAdapter:', self.name, 'id', self.pairDeviceId,
                'pairing cancelled')

    def removeThing(self, device):
        print('GcodeAdapter:', self.name, 'id', self.id, 'removeThing(', device.id, ') started')

        if self.removeDevice(device.id):
            print('GcodeAdapter: device:', device.id, 'was unpaired.')
        else:
            print('GcodeAdapter: unpairing', device.id, 'failed')