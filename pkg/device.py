"""octopi adapter for Mozilla IoT Gateway."""

from gateway_addon import Device
from .property import GProperty


class GDevice(Device):
    def __init__(self, adapter, _id, deviceDescription, octopi):

        Device.__init__(self, adapter, _id)

        self.octopi = octopi
        self.name = deviceDescription['name']
        self.type = deviceDescription['type']
        self.description = deviceDescription

        for propertyName in self.description['properties']:
            print('Property :' + propertyName)
            self.propertyDescription = self.description['properties'][propertyName]
            property = GProperty(self, propertyName, self.propertyDescription)
            self.properties[propertyName] = property

        """
        for actionName in self.description['actions']:
            print('Action :' + actionName)
            self.propertyDescription = self.description['properties'][propertyName]
            self.property = Property(self, propertyName, self.propertyDescription)
            this.properties.set(propertyName, self.property)
        """