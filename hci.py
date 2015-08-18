import usb.core
from struct import pack
import threading
import time
import code
from _struct import unpack
import hci_constants

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

event_handlers = {}

cmd_done_condition = threading.Condition()
done_events = {}

def event_thread(dev):

        global hci_device
        
        while True:
            #time.sleep(1)
            
            #hci_device.ctrl_transfer(0x20, 0x00, 0x00, 0x00, msg_empy)
            #hci_device.ctrl_transfer(0x20, 0x00, 0x00, 0x00, msg_empy)
            try:
                evt_packet = hci_device.read(0x81, 256 + 2, timeout=0)
                code = evt_packet[0]
                param_len = evt_packet[1] # hci_device.read(0x81, 1)
                param = evt_packet[2 : 2 + param_len] #hci_device.read(0x81, param_len)
                
            except:
                print "exception ..."
                raise
            
            try:
                event_handlers[code](param.tostring())
            except KeyError:
                print "recieved event %d with no handler" % code
                
def cmd_done_evt_handler(param):
    # post the event into the list of done events
    cmd_done_condition.acquire()
    opcode = unpack("<H", param[1:3])[0]
    status = param[3:]
    done_events[opcode] = status
    cmd_done_condition.notify_all() 
    cmd_done_condition.release()
    
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
        self.register_event_handler(14, cmd_done_evt_handler)
        self.event_thread.start()
        #hci_device.ctrl_transfer(0x20, 0x00, 0x00, 0x00, [0x03 , 0x0c, 0])
        self.reset()
            
    def register_event_handler(self, evt_code, handler):
        event_handlers[evt_code] = handler
        
    def send_cmd(self, ocf, ogf, args):
        # for now only supporting USB
        opcode = (ocf << 10) | ogf
        msg = pack("<HB", opcode, len(args)) + args
        self.dev.ctrl_transfer(0x20, 0x00, 0x00, 0x00, msg)
        
        # wait for an event
        ret_status = None
        while ret_status is None:
            cmd_done_condition.acquire()
            cmd_done_condition.wait()
            if opcode in done_events:
                ret_status = done_events[opcode]
                del done_events[opcode]
            cmd_done_condition.release()
            
        err_code = unpack("<B", ret_status[0:1])[0]
            
        if err_code != 0:
            raise Exception("HCI command returned %d"% err_code)
            
    
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
        
    def le_set_adv_params(self, Advertising_Interval_Min,
                Advertising_Interval_Max,
                Advertising_Type = hci_constants.advertising_types.ADV_IND,
                Own_Address_Type = hci_constants.advertising_address_types.PUBLIC,
                Peer_Address_Type = hci_constants.advertising_address_types.PUBLIC,
                Peer_Address = "\x00\x00\x00\x00\x00\x00",
                Advertising_Channel_Map = hci_constants.advertising_channel_map.CHANNEL_ALL,
                Advertising_Filter_Policy = hci_constants.advertising_filter_policy.NONE
                ):
        
        args = pack("<HHBBBsBB",Advertising_Interval_Min,
                Advertising_Interval_Max,
                Advertising_Type,
                Own_Address_Type,
                Peer_Address_Type,
                Peer_Address,
                Advertising_Channel_Map,
                Advertising_Filter_Policy)
        
        self.send_cmd(0x8, 0x6, args)
        
    def le_set_adv_data(self, data):
        args = pack("<Bs", len(data), data)
        self.send_cmd(0x8, 0x8, args)
        
    def le_set_scan_rsp_data(self, data):
        args = pack("<Bs", len(data), data)
        self.send_cmd(0x8, 0x9, args)
        
    def le_set_adv_enable(self, enabled = True):
        if enabled:
            args = "\x01"
        else:
            args = "\x00"
        self.send_cmd(0x8, 0xa, args)
        