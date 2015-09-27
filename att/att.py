
import att_constants
import uuid

to_hex = lambda x : "0x%02x" % ord(x)

class att:
    
    attributes = { }
    
    def exchange_mtu_request_routine(self):
        pass
    
    def find_information_request_routine(self):
        pass
    
    def find_by_type_value_request_routine(self, packet):
        print map(to_hex,packet)

    def read_by_type_request_routine(self, packet):
        print map(to_hex,packet)
        
    def read_request_routine(self, packet):
        print map(to_hex,packet)
        
    def read_blob_request_routine(self, packet):
        print map(to_hex,packet)
        
    def read_multiple_request_routine(self, packet):
        print map(to_hex,packet)
        
    def read_by_group_type_request_routine(self, packet):
        print map(to_hex,packet)
        
    def write_request_routine(self, packet):
        print map(to_hex,packet)
        
    def write_command_routine(self, packet):
        print map(to_hex,packet)
        
    def prepare_write_request_routine(self, packet):
        print map(to_hex,packet)
        
    def execute_write_request_routine(self, packet):
        print map(to_hex,packet)
        
    def handle_value_confirmation_routine(self, packet):
        print map(to_hex,packet)
        
    def signed_write_command_routine(self, packet):
        print map(to_hex,packet)
    
    att_server_routines = {
            att_constants.EXCHANGE_MTU_REQUEST : exchange_mtu_request_routine,
            att_constants.FIND_INFORMATION_REQUEST : find_information_request_routine,
            att_constants.FIND_BY_TYPE_VALUE_REQUEST : find_by_type_value_request_routine,
            att_constants.READ_BY_TYPE_REQUEST : read_by_type_request_routine,
            att_constants.READ_REQUEST : read_request_routine,
            att_constants.READ_BLOB_REQUEST : read_blob_request_routine,
            att_constants.READ_MULTIPLE_REQUEST : read_multiple_request_routine,
            att_constants.READ_BY_GROUP_TYPE_REQUEST : read_by_group_type_request_routine,
            att_constants.WRITE_REQUEST : write_request_routine,
            att_constants.WRITE_COMMAND : write_command_routine,
            att_constants.PREPARE_WRITE_REQUEST : prepare_write_request_routine,
            att_constants.EXECUTE_WRITE_REQUEST : execute_write_request_routine,
            att_constants.HANDLE_VALUE_CONFIRMATION : handle_value_confirmation_routine,
            att_constants.SIGNED_WRITE_COMMAND : signed_write_command_routine,
        }
        
    def __init__(self, handle):
        self.handle = handle
        
        
    def process_packet(self, packet):
        print "ATT handle 0x%x" % self.handle
        print map(to_hex,packet)
        self.att_server_routines[ord(packet[0])](self, packet[1:])
        
        


