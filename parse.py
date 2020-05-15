import re

class Parse:
    def __init__(self, data):

        self.data = data
        self.result = {}

    def getSNMPLocatoin(self):

        snmpLocation = str()
        pattern = re.compile('snmp-server loc')
        
        print('--- Gathering SNMP-Server Location')
        for elem in self.data:
            match = pattern.search(elem)
            if match:
                snmpLocation = elem.split(' ')[2:]
                break
    
        if snmpLocation:
            self.result['snmpLocation'] = ' '.join(snmpLocation)
        else:
            self.result['snmpLocation'] = 'Not Set'
        
        print(self.result)
        return self.result
                
                