## Adopting pyMulti to custom stage

Replace **zaber_motion** library in pyMulti.py (imports lines 22-25) with the corresponding stage library. 

Imported zaber_motion objects for Zaber stage (pyMulti, lines 22-25) to be replaced: Library, Connection, Units, CommandFailedException

**Library**: Grants access to local file system used to store device information.In particular important for zaber_motion. 
* Initialized in pyMUlti main: (line 523) Library.enable_device_db_store()

**Connection**: Establishes and handles the serial port connection to the Zaber stage. Gets the serial port name of the device as a string. Initialized in pyMUlti: (line 190) device_list = connection.detect_devices()

* Establish connection to seiral port (pyMUlti, line 187) >> connection = Connection.open_serial_port(commPort)
* Link serial port with devices (pyMUlti, line 190) >> device_list = connection.detect_devices()
* Select device instance (pyMUlti, line 203) >> self.device = device_list[1] 
* Select axis objects of device class (e.g. pyMUlti, line 244) >> self.XAxis = self.device.get_axis(1)
* Use device axis class functions for stage control (e.g. pyMUlti, line 315) self.XAxis.move_absolute(self.homeX,Units.LENGTH_MILLIMETRES)
* Close device connection via (pyMUlti, line 244) >> self.device.connection.close()
 
**Calls of axis instances (to move the stage) to be replaced**: 
* pyMulti lines: 88, 89, 95, 96, 113, 315, 316, 329, 330, 358, 390, 391

**Units**: Used with axis instance to ensure that movements are performed in millimeter scale.

**CommandFailedException**: used for device specific display of error codes (exception message). (pyMUlti, Line: 393)