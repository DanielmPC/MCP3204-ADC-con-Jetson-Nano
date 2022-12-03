from .adafruit_bus_device import SPIDevice

class MCP3xxx:
    """
    This abstract base class is meant to be inherited by `MCP3008`_, `MCP3004`_,
    or `MCP3002`_ child classes.

    :param ~adafruit_bus_device.spi_device.SPIDevice spi_bus: SPI bus the ADC is connected to.
    :param ~digitalio.DigitalInOut cs: Chip Select Pin.
    :param float ref_voltage: Voltage into (Vin) the ADC.
    """

    def __init__(self, spi_bus, cs, ref_voltage=3.3):  # pylint: disable=invalid-name
        self._spi_device = SPIDevice(spi_bus, cs)
        self._out_buf = bytearray(3)
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

    @property
    def reference_voltage(self):
        """Returns the MCP3xxx's reference voltage. (read-only)"""
        return self._ref_voltage

    def read(self, pin, is_differential=False):
        """SPI Interface for MCP3xxx-based ADCs reads. Due to 10-bit accuracy, the returned
        value ranges [0, 1023].

        :param int pin: individual or differential pin.
        :param bool is_differential: single-ended or differential read.

        .. note:: This library offers a helper class called `AnalogIn`_ for both single-ended
            and differential reads. If you opt to not implement `AnalogIn`_ during differential
            reads, then the ``pin`` parameter should be the first of the two pins associated with
            the desired differential channel mapping.
        """
        self._out_buf[1] = ((not is_differential) << 7) | (pin << 4)
        with self._spi_device as spi:
            # pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf)
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]
