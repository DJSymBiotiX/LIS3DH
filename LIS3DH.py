import logging
import rpI2C

log = logging.getLogger(__name__)


class LIS3DH(object):
    # Registers
    STATUS_REG_AUX = 0x07
    OUT_ADC1_L = 0x08
    OUT_ADC1_H = 0x09
    OUT_ADC2_L = 0x0A
    OUT_ADC2_H = 0x0B
    OUT_ADC3_L = 0x0C
    OUT_ADC3_H = 0x0D
    INT_COUNTER_REG = 0x0E
    WHO_AM_I = 0x0F
    TEMP_CFG_REG = 0x1F
    CTRL_REG1 = 0x20
    CTRL_REG2 = 0x21
    CTRL_REG3 = 0x22
    CTRL_REG4 = 0x23
    CTRL_REG5 = 0x24
    CTRL_REG6 = 0x25
    REFERENCE = 0x26
    STATUS_REG2 = 0x27
    OUT_X_L = 0x28
    OUT_X_H = 0x29
    OUT_Y_L = 0x2A
    OUT_Y_H = 0x2B
    OUT_Z_L = 0X2C
    OUT_Z_H = 0x2D
    FIFO_CTRL_REG = 0x2E
    FIFO_SRC_REG = 0x2F
    INT1_CFG = 0x30
    INT1_SRC = 0x31
    INT1_THS = 0x32
    INT1_DURATION = 0x33
    CLICK_CFG = 0x38
    CLICK_SRC = 0x39
    CLICK_THS = 0x3A
    TIME_LIMIT = 0x3B
    TIME_LATENCY = 0x3C
    TIME_WINDOW = 0x3D
    ACT_THS = 0x3E
    INACT_DUR = 0x3F

    # Data Rate
    DATARATE_POWER_DOWN = 0b0000
    DATA_RATE_1HZ = 0b0001
    DATA_RATE_10HZ = 0b0010
    DATA_RATE_25HZ = 0b0011
    DATA_RATE_50HZ = 0b0100
    DATA_RATE_100HZ = 0b0101
    DATA_RATE_200HZ = 0b0110
    DATA_RATE_400HZ = 0b0111
    DATA_RATE_LOW_POWER_15 = 0b1000
    DATA_RATE_LOW_POWER_5 = 0b1001

    # Power Modes
    POWER_MODE_NORMAL = 0x00
    POWER_MODE_LOW = 0x01

    # Device ID
    DEVICE_ID = 0x33

    # ADC Pins
    ADC_PIN1 = 0x01
    ADC_PIN2 = 0x10
    ADC_PIN3 = 0x11

    def __init__(self, address=0x18, bus=None):
        self.i2c = rpI2C.I2C(address, bus=bus)
        self.address = address  # don't need?

        self.get_device_id()

        self.low_power_mode = False
        self.x_enable = True
        self.y_enable = True
        self.z_enable = True
        self.data_rate = self.DATA_RATE_400HZ

        self.temperature_enable = False
        self.ADC_enable = True

        self.__update_temperature_adc_register()
        self.__update_control_register_one()
        print self.read_status_register()
        print self.read_adc_data(self.ADC_PIN1)
        print self.read_adc_data(self.ADC_PIN2)
        print self.read_adc_data(self.ADC_PIN3)

    def get_device_id(self):
        try:
            value = self.i2c.read_unsigned_byte(self.WHO_AM_I)

            if value != self.DEVICE_ID:
                log.exception(
                    (
                        "Device ID incorrect. Expecting 0x%02X, but received "
                        "0x%02X at address 0x%02X"
                    ) % (
                        self.DEVICE_ID, value, self.address
                    )
                )
                raise
            log.debug(
                "Successfully connected to LIS3DH on address 0x%02X" %
                self.address
            )
        except Exception as e:
            log.exception(
                "Could not connect to LIS3DH on address 0x%02X" %
                self.address
            )
            raise

    def set_data_rate(self, data_rate, update=False):
        self.data_rate = data_rate
        if update:
            self.__update_control_register_one()

    def set_power_mode(self, power_mode, update=False):
        if power_mode == self.POWER_MODE_NORMAL:
            self.low_power_mode = false
        if update:
            self.__update_control_register_one()

    def read_status_register(self):
        status = self.i2c.read_unsigned_byte(self.STATUS_REG_AUX)
        log.debug("Status: %s" % self.__print_bin(status))
        result = {
            "overrun_321":          self.__torf(status & (0b10000000 >> 7)),
            "overrun_3":            self.__torf(status & (0b01000000 >> 6)),
            "overrun_2":            self.__torf(status & (0b00100000 >> 5)),
            "overrun_1":            self.__torf(status & (0b00010000 >> 4)),
            "data_available_321":   self.__torf(status & (0b00001000 >> 3)),
            "data_available_3":     self.__torf(status & (0b00000100 >> 2)),
            "data_available_2":     self.__torf(status & (0b00000010 >> 1)),
            "data_available_1":     self.__torf(status & (0b00000001))
        }
        return result

    def read_adc_data(self, pin):
        if pin == self.ADC_PIN1:
            low_reg = self.OUT_ADC1_L
            high_reg = self.OUT_ADC1_H
        elif pin == self.ADC_PIN2:
            low_reg = self.OUT_ADC2_L
            high_reg = self.OUT_ADC2_H
        elif pin == self.ADC_PIN3:
            low_reg = self.OUT_ADC3_L
            high_reg = self.OUT_ADC3_H
        else:
            log.error("read_adc_data: Must supply a valid ADC Pin")
            return 0x00

        # Read data
        low = self.i2c.read_unsigned_byte(low_reg)
        high = self.i2c.read_unsigned_byte(high_reg)
        result = self.__twos_complement((high << 8) | low)
        return result

    def __update_temperature_adc_register(self):
        temp_enable = self.__zoro(self.temperature_enable)
        adc_enable = self.__zoro(self.ADC_enable)
        data = 0x00 | adc_enable << 7 | temp_enable << 6
        self.i2c.write_byte(self.TEMP_CFG_REG, data)

    def __update_control_register_one(self):
        low_power = self.__zoro(self.low_power_mode)
        x = self.__zoro(self.x_enable)
        y = self.__zoro(self.y_enable)
        z = self.__zoro(self.z_enable)
        data = (
            (self.data_rate << 4) |
            (low_power << 3) |
            (z << 2) |
            (y << 1) |
            x
        )
        self.i2c.write_byte(self.CTRL_REG1, data)

    def __print_bin(self, value):
        return format(value, '#10b')

    def __twos_complement(self, value, bits=16):
        """
        Compute the 2's complement of an integer value with bit count == bits
        """
        # If the sign bit is set
        if value & (1 << (bits - 1)) != 0:
            # Compute the negative value
            value = value - (1 << bits)
        return value

    def __torf(self, value):
        """
        Return True if value is 1 else return False
        """
        if value == 0x01:
            return True
        return False

    def __zoro(self, value):
        """
        Return 1 if value is True else return 0
        """
        if value:
            return 0x01
        return 0x00


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s'
    )

    x = LIS3DH()


if __name__ == '__main__':
    main()
