
class l2cap_signaling:
    
    def __init__(self, handle):
        self.handle = handle
        
        
    def process_packet(self, packet):
        print("l2cap sig handle 0x%x, pacet is " % self.handle + packet.tostring())
    
