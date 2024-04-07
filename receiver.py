class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(packet):
        if packet['checksum'] == ord(packet['data']):
            return False 
        return True



    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        if(exp_seq == rcv_pkt['sequence_number']):
            return True
        return False


    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    def rdt_rcv(self, rcv_pkt):

        green_text = '\033[92m'
        end_color = '\033[0m'

        print(f'{green_text}Receiver: expecting sequence number:{self.sequence}{end_color}')
        print(f'{green_text}Receiver Received:{rcv_pkt}{end_color}')

        #if it is not corrupted and the seq number is correct
        if(not self.is_corrupted(rcv_pkt) and self.is_expected_seq(rcv_pkt ,self.sequence)):
            ReceiverProcess.deliver_data(rcv_pkt['data'])
            reply_pkt = self.make_reply_pkt(self.sequence,ord(self.sequence))
            print(f'{green_text}Receiver: reply with: [ack: {reply_pkt['ack']}, checksum: {reply_pkt['checksum']}]{end_color}')
            self.sequence = '1' if self.sequence == '0' else '0'  
        else:
            if(self.sequence == '0'):
                reply_pkt = self.make_reply_pkt('1', ord('1')) 
            else: 
                reply_pkt =  self.make_reply_pkt('0', ord('0'))
            print(f'{green_text}Receiver: reply with: [ack: {reply_pkt['ack']}, checksum: {reply_pkt['checksum']}]{end_color}')
            
        return reply_pkt
