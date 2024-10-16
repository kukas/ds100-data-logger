#!/usr/bin/env python
import usb.core
import struct

VENDOR = 0x1941
PRODUCT = 0x8021

def open_ws():
    '''
    Open a connection to the device, using the PRODUCT and VENDOR information
    @return reference to the device
    '''
    usb_device = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)

    if usb_device is None:
        raise ValueError('Device not found')

    usb_device.get_active_configuration()

    # If we don't detach the kernel driver we get I/O errors
    if usb_device.is_kernel_driver_active(0):
        usb_device.detach_kernel_driver(0)

    return usb_device


def read_block(device, offset):
    '''
    Read a block of data from the specified device, starting at the given
    offset.
    @Inputs
    device
        - usb_device
    offset
        - int value
    @Return byte array
    '''

    least_significant_bit = offset & 0xFF
    most_significant_bit = offset >> 8 & 0xFF

    # Construct a binary message
    tbuf = struct.pack('BBBBBBBB',
                       0xA1,
                       most_significant_bit,
                       least_significant_bit,
                       32,
                       0xA1,
                       most_significant_bit,
                       least_significant_bit,
                       32)

    timeout = 1000  # Milliseconds
    retval = device.ctrl_transfer(0x21,  # USB Requesttype
                               0x09,  # USB Request
                               0x200,  # Value
                               0,  # Index
                               tbuf,  # Message
                               timeout)

    return device.read(0x81, 32, timeout)

# Open up a connection to the device
dev = open_ws()
dev.set_configuration()

i = 0
data_end = False
print("Temperature, Humidity")
while True:
    # start at offset 256 and read 32 bytes at a time
    block = read_block(dev, 256+i)
    # print(block, len(block))
    for j in range(0, 8):
        # go through the block 4 bytes at a time
        block_4bytes = block[j*4:j*4+4]
        if list(block_4bytes) == [0xFF, 0xFF, 0xFF, 0xFF]:
            data_end = True
            break

        indoor_humidity = block_4bytes[2]

        # temperature is encoded in two bytes
        tlsb = block_4bytes[1]
        tmsb = block_4bytes[0] & 0x7f
        tsign = block_4bytes[0] >> 7
        indoor_temperature = (tmsb * 256 + tlsb) * 0.1 - 40
        if tsign:
            indoor_temperature *= -1
        indoor_temperature = round(indoor_temperature, 1)

        print(indoor_temperature, ",", indoor_humidity)
    if data_end:
        break
    i += 32
