
class smp:
    
    def __init__(self, handle):
        self.handle = handle
        
        
    def process_packet(self, packet):
        print("SMP handle 0x%x, pacet is " % self.handle + packet)
    
