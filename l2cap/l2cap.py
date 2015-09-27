'''
Created on 3 Sep 2015

@author: shiro
'''
from _struct import unpack
import l2cap_constants
import l2cap_signaling
from att import att
from smp import smp

class l2cap(object):
    
    def __init__(self, handle):
        self.handle = handle
        self.channels = {}
        self.channels[l2cap_constants.cids.ATT] = att.att(handle)
        self.channels[l2cap_constants.cids.SIGNALING] = l2cap_signaling.l2cap_signaling(handle)
        self.channels[l2cap_constants.cids.SMP] = smp.smp(handle)
    
    def process_packet(self, packet):
        (length, cid) = unpack("<HH", packet[0:4])
        self.channels[cid].process_packet(packet[4:4+length])
