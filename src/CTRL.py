##
## Let's Ignore PEP8 for this file, so that we can align stuff
##

# Registers
STATUS_REG_AUX  = 0x07
OUT_ADC1_L      = 0x08
OUT_ADC1_H      = 0x09
OUT_ADC2_L      = 0x0A
OUT_ADC2_H      = 0x0B
OUT_ADC3_L      = 0x0C
OUT_ADC3_H      = 0x0D
INT_COUNTER_REG = 0x0E
WHO_AM_I        = 0x0F
TEMP_CFG_REG    = 0x1F
CTRL_REG1       = 0x20
CTRL_REG2       = 0x21
CTRL_REG3       = 0x22
CTRL_REG4       = 0x23
CTRL_REG5       = 0x24
CTRL_REG6       = 0x25
REFERENCE       = 0x26
STATUS_REG2     = 0x27
OUT_X_L         = 0x28
OUT_X_H         = 0x29
OUT_Y_L         = 0x2A
OUT_Y_H         = 0x2B
OUT_Z_L         = 0X2C
OUT_Z_H         = 0x2D
FIFO_CTRL_REG   = 0x2E
FIFO_SRC_REG    = 0x2F
INT1_CFG        = 0x30
INT1_SRC        = 0x31
INT1_THS        = 0x32
INT1_DURATION   = 0x33
CLICK_CFG       = 0x38
CLICK_SRC       = 0x39
CLICK_THS       = 0x3A
TIME_LIMIT      = 0x3B
TIME_LATENCY    = 0x3C
TIME_WINDOW     = 0x3D
ACT_THS         = 0x3E
INACT_DUR       = 0x3F

# Data Rate
DATARATE_POWER_DOWN     = 0x00
DATA_RATE_1HZ           = 0x01
DATA_RATE_10HZ          = 0x02
DATA_RATE_25HZ          = 0x03
DATA_RATE_50HZ          = 0x04
DATA_RATE_100HZ         = 0x05
DATA_RATE_200HZ         = 0x06
DATA_RATE_400HZ         = 0x07
DATA_RATE_LOW_POWER_15  = 0x08
DATA_RATE_LOW_POWER_5   = 0x09

# Power Modes
POWER_MODE_NORMAL   = 0x00
POWER_MODE_LOW      = 0x01

# Device ID
DEVICE_ID = 0x33

# ADC Pins
ADC_PIN1 = 0b01
ADC_PIN2 = 0x02
ADC_PIN3 = 0x03
