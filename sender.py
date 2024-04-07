class SenderProcess:
    """ Represent the sender process in the application layer  """

    __buffer = list()

    @staticmethod
    def set_outgoing_data(buffer):
        """ To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """ To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer


class RDTSender:
    """ Implement the Reliable Data Transfer Protocol V2.2 Sender Side """

    def __init__(self, net_srv):
        """ This is a class constructor
            It initialize the RDT sender sequence number  to '0' and the network layer services
            The network layer service provide the method udt_send(send_pkt)
        """
        self.sequence = '0'
        self.net_srv = net_srv

    @staticmethod
    def get_checksum(data):
        """ Calculate the checksum for outgoing data
        :param data: one and only one character, for example data = 'A'
        :return: the ASCII code of the character, for example ASCII('A') = 65
        """
        # TODO provide your own implementation
        checksum = ord(data)
        return checksum

    @staticmethod
    def clone_packet(packet):
        """ Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as python dictionary
        """
        pkt_clone = {
            'sequence_number': packet['sequence_number'],
            'data': packet['data'],
            'checksum': packet['checksum']
        }
        return pkt_clone

    @staticmethod
    #when i get the reply packet it will have two things seq and checksum, corruption is relaated to the checksum
    def is_corrupted(reply):
        if(reply['checksum'] == ord(reply['ack'])):
            return False
        return True
    

    @staticmethod
    def is_expected_seq(reply, exp_seq):
        if(exp_seq == reply['ack']):
            return True
        return False

    @staticmethod
    def make_pkt(seq, data, checksum):
        """ Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender want to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        packet = {
            'sequence_number': seq,
            'data': data,
            'checksum': checksum
        }
        return packet

    def rdt_send(self, process_buffer):

        blue_text = '\033[94m'
        end_color = '\033[0m'
        green_text = '\033[92m'
        red_text = '\033[91m'
    
        for data in process_buffer:
            flag = True 
            while flag: 
                checksum = self.get_checksum(data)
                pkt = self.make_pkt(self.sequence, data, checksum) #initially sequence is 0, curr character, checksum as calculated
                print(f'{blue_text}Sender expecting sequence number: {self.sequence}{end_color}')
                print(f'{blue_text}Sender sending: [sequence number: {self.sequence} ] [ data: {data} ] [ checksum: {checksum} ]{end_color}')
                reply = self.net_srv.udt_send(pkt) 
                print(f'{blue_text}Sender received: {reply}{end_color}')
                if (not self.is_corrupted(reply)) and self.is_expected_seq(reply, self.sequence) :
                    flag = False
                    self.sequence = '1' if self.sequence == '0' else '0'
                    print(f'{blue_text}Successful Transmission!{end_color}')
                else:
                    print(f'{red_text}error detected, resending{end_color}')
                print('*******************************************************')

        print(f'{blue_text}Sender Done!{end_color}')
        return
     
            
     
    
        
    



