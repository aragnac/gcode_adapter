"""octopi adapter for Mozilla IoT Gateway."""

import json
import ast
from gateway_addon import Property


class GProperty(Property):
    """Octopi property type."""

    def __init__(self, device, name, propertyDescription):
        """
        Initialize the object.
        device -- the Device this property belongs to
        name -- name of the property
        description -- description of the property, as a dictionary
        value -- current value of this property
        """
        print('properyDescription:' + json.dumps(propertyDescription))
        Property.__init__(self, device, name, propertyDescription)
        self.device = device
        self.unit = propertyDescription['unit']
        self.description = propertyDescription
        self.value = propertyDescription['value']
        self.set_cached_value(self.value)
        #self.device.notify_property_changed(self)

    def set_value(self, value):
        """
        Set the current value of the property.
        value -- the value to set
        """
        if self.name == 'x_axes':
            self.set_position('x', value)
        elif self.name == 'y_axes':
            self.set_position('y', value)
        elif self.name == 'z_axes':
            self.set_position('z', value)
        elif self.name == 'feed_rate':
            self.set_feedRate(value)
        elif self.name == 'connected?':
            self.manage_connection(value)
        else:
            return

        self.set_cached_value(value)
        self.device.notify_property_changed(self)

    def update(self, sysinfo, emeter):
        """
        Update the current value, if necessary.
        sysinfo -- current sysinfo dict for the device
        emeter -- current emeter for the device
        """
        if self.name == 'x_axes':
            value = self.device.is_on(sysinfo)
        elif self.name == 'y_axes':
            value = self.device.power(emeter)
        elif self.name == 'z_axes':
            value = self.device.voltage(emeter)
        else:
            return

        if value != self.value:
            self.set_cached_value(value)

        self.device.notify_property_changed(self)

    def set_position(self, axes, distance):
        if axes == 'x':
            self.device.octopi.jog(x=distance)
        elif axes == 'y':
            self.device.octopi.jog(y=distance)
        elif axes == 'z':
            self.device.octopi.jog(z=distance)

    def manage_connection(self, value):
        if value:
            self.device.octopi.connect(port=self.device.adapter.Port, baudrate=self.device.adapter.Baudrate,
                                       autoconnect='true', save='true')
        else:
            self.device.octopi.disconnect()

    def set_feedRate(self, value):
        self.device.octopi.feedrate(value)