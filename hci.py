import usb.core
from struct import pack
import threading
import time

hci_device = None

# mapping from a command name to its OCF and OGF
commands_op_code = {
    "reset"                     : (0x3, 0x3),
    "set event mask"            : (0x3, 0x1),
    "le set event mask"         : (0x8, 0x1),
    "set adv params"            : (0x8, 0x6),
    "read adv channel tx power" : (0x8, 0x7),
    "set adv data"              : (0x8, 0x8),
    "set scan rsp data"         : (0x8, 0x9),
    "set adv enable"            : (0x8, 0xa),
                    }
def event_thread(dev):

        global hci_device
        
        while True:
            time.sleep(1)
            
            #hci_device.ctrl_transfer(0x20, 0x00, 0x00, 0x00, msg_empy)
            #hci_device.ctrl_transfer(0x20, 0x00, 0x00, 0x00, msg_empy)
            try:
                code = hci_device.read(0x81, 256 + 2, timeout=0)
                #param_len = hci_device.read(0x81, 1)
                #param = hci_device.read(0x81, param_len)
                
            except:
                print "exception ..."
                raise
            
            print code
            #print param
    
    
class hci_if:
    def __init__(self):
        self.dev = usb.core.find(idVendor=0x0a5c, idProduct=0x21e8)
        if self.dev is None:
            raise ValueError('Our device is not connected')
        self.dev.set_configuration()
        global hci_device
        hci_device = self.dev
        self.event_thread = threading.Thread(target=event_thread, 
                                             name="hci_event_thread",
                                             args=self.dev)
        self.event_thread.start()
        #hci_device.ctrl_transfer(0x20, 0x00, 0x00, 0x00, [0x03 , 0x0c, 0])
        self.reset()
            
        
    def send_cmd(self, ocf, ogf, args):
        # for now only supporting USB
        opcode = (ocf << 6) | ogf
        msg = pack("<HB", opcode, len(args)) + args
        self.dev.ctrl_transfer(0x20, 0x00, 0x00, 0x00, msg)
    
    def reset(self):
        self.send_cmd(0x3, 0x3, "")
        
    def set_evt_mask(self, *events):
        event_mask = []
        for event in events:
            for index in range(8):
                event_mask[index] += event[index]
        self.send_cmd(0x3, 0x1, event_mask)
        
    def le_set_event_mask(self, *le_events):
        le_event_mask = []
        for event in le_events:
            for index in range(8):
                le_event_mask[index] += event[index]
        self.send_cmd(0x8, 0x1, le_event_mask)
        
    def set_adv_params(self, Advertising_Interval_Min,
                Advertising_Interval_Max,
                Advertising_Type,
                Own_Address_Type,
                Peer_Address_Type,
                Peer_Address,
                Advertising_Channel_Map,
                Advertising_Filter_Policy
                ):
        
        args = pack("<HHBBBBBB",Advertising_Interval_Min,
                Advertising_Interval_Max,
                Advertising_Type,
                Own_Address_Type,
                Peer_Address_Type,
                Peer_Address,
                Advertising_Channel_Map,
                Advertising_Filter_Policy)
        
        self.send_cmd(0x8, 0x6, args)