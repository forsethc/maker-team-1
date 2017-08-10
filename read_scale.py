import usb
import time
from post_image import post_image
from camera/capture-still import capture

scale1 = None
scale1IsEmpty = False
scale2 = None
DATA_MODE_OUNCES = 11
DATA_MODE_GRAMS = 2
EMPTY_CARAFE_WEIGHT = 3460
EMPTY_CARAFE_BUFFER = 200
EMPTY_CARAFE_NOTIFICATION = "Carafe on {} is empty"

def main():
    global scale1, scale2
    VENDOR_ID = 0x0922
    devices = usb.core.find(find_all=True, idVendor=VENDOR_ID)

    for device in devices:
        if device.is_kernel_driver_active(0) is True:
            device.detach_kernel_driver(0)
        if scale1 is None:
            scale1 = device
        elif scale2 is None:
            scale2 = device

    while True:
        checkScaleOne()

        time.sleep(1)

def getLatestImage():
    return "http://team1.widen.com/coffee/images/image.jpg"

def bitchAboutNoCoffee():
    capture()
    post_image("Thirsty? Blame this person... " + getLatestImage(), "")

def checkScaleOne():
    global scale1IsEmpty
    weight = readScaleOne()
    if weight is not None:
        print "Scale 1 is at weight : '" + str(weight) +"' g"
        if weight < EMPTY_CARAFE_WEIGHT + EMPTY_CARAFE_BUFFER:
            print EMPTY_CARAFE_NOTIFICATION.format("scale 1")
            if scale1IsEmpty == False:
                bitchAboutNoCoffee()
            scale1IsEmpty = True
        else:
            scale1IsEmpty = False

def readScaleOne():
    global scale1
    return readWeight(scale1)

def readScaleTwo():
    global scale2
    return readWeight(scale2)

# returns scale reading in grams
def readWeight(device):
    endpoint = device[0][(0,0)][0]

    attempts = 10
    data = None
    while data is None and attempts > 0:
        try:
            data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):
                attempts -= 1
                # print e
                continue

    raw_weight = data[4] + (256 * data[5])

    if data[2] == DATA_MODE_OUNCES:
        ounces = raw_weight * 0.1
        weight = "%s oz" % ounces
    elif data[2] == DATA_MODE_GRAMS:
        grams = raw_weight
        weight = "%s g" % grams

    reading = weight
    # print "raw reading '" + reading +"'"

    readval = float(reading.split(" ")[0])
    readunit = reading.split(" ")[1]
    ## if the units are ounces ("oz") then convert to "g"
    if readunit == "oz" and readval !=0:
        readval = readval*28.3495
        # print "converted oz to g"

    return readval

main()