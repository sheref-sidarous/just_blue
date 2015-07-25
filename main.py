import usb.core
import time
import hci

if False:    
    dev = usb.core.find(idVendor=0x0a5c, idProduct=0x21e8)
    if dev is None:
        raise ValueError('Our device is not connected')
        
    print "device found !!"
    
    msg = [0x03 , 0x0c] # the reset command
    dev.set_configuration()
    cfg = dev.get_active_configuration()
    print dev[0][(0,0)][0]
    while True:
        dev.ctrl_transfer(0x20, 0x00, 0x00, 0x00, msg)
        try:
            evt = dev.read(0x81, 16, 10)
        except:
            continue
        print evt
        print len(evt)
        break
else:
    hci_interface = hci.hci_if()
    #hci_interface.reset()
