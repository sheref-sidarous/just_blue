'''
Created on 17 Aug 2015

@author: shiro
'''

class event_codes():
    COMMAND_DONE = 14
    

"""as defined in Vol 2, Part E, Secion 7.8.5"""
class advertising_types():
    """Connectable undirected advertising (default)"""
    ADV_IND = 0x00 
    
    '''Connectable high duty cycle directed advertising'''
    ADV_DIRECT_IND_high = 0x01 
    
    '''Scannable undirected advertising'''
    ADV_SCAN_IND = 0x02

    '''Non connectable undirected advertising'''
    ADV_NONCONN_IND = 0x03
    
    '''Connectable low duty cycle directed advertising'''
    ADV_DIRECT_IND_low = 0x04 

"""as defined in Vol 2, Part E, Secion 7.8.5"""
class advertising_address_types():
    '''Public Device Address ( default )'''
    PUBLIC = 0x00 
    
    '''Random Device Address'''
    RANDOM = 0x01
    
    '''Controller generates Resolvable Private Address based on the local
    IRK from resolving list. If resolving list contains no matching entry,
    use public address.'''
    RESOLVABLE_OR_PUBLIC = 0x02 

    '''Controller generates Resolvable Private Address based on the local
    IRK from resolving list. If resolving list contains no matching entry,
    use random address from LE_Set_Random_Address.'''
    RESOLVABLE_OR_RANDOM = 0x03 
    
class advertising_channel_map():
    CHANNEL_37 = 0x1
    CHANNEL_38 = 0x2
    CHANNEL_39 = 0x4
    CHANNEL_ALL = CHANNEL_37 | CHANNEL_38 | CHANNEL_39
    
class advertising_filter_policy():
    '''Process scan and connection requests from all devices (i.e., the White List
    is not in use) ( default )'''
    NONE = 0x00 
    
    '''Process connection requests from all devices and only scan requests from
    devices that are in the White List.'''
    FILTER_SCAN_REQUESTS = 0x01
    
    '''Process scan requests from all devices and only connection requests from
    devices that are in the White List..'''
    FILTER_CONNECTION_REQUESTS = 0x02 
    
    '''Process scan and connection requests only from devices in the White List.'''
    FILTER_SCAN_AND_CONNECTION = 0x03
    
    
        