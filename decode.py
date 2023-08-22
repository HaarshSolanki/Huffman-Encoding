class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__reverseCodes=codes_dict

    def __removePadding(self,text):
        padded_info=text[:8]
        extra_padding= int(padded_info,2)
        text=text[8:]
        text_after_padding_removed=text[:-1*extra_padding]
        return text_after_padding_removed
    
    def __decodeText(self,text):
        decoded_text=""
        current_bits=""
        for bit in text:
            current_bits += bit
            if current_bits in self.__reverseCodes:
                character = self.__reverseCodes[current_bits]
                decoded_text += character
                current_bits =""
        return  decoded_text
    
    def decompress(self):
        output_path='decoded'+'.txt'
        with open(self.path,'rb') as file , open(output_path,'w') as output:
            bit_string=""
            byte=file.read(1)
            while byte:
                byte = ord(byte)
                bits =bin(byte)[2:].rjust(8,'0')
                bit_string +=bits
                byte=file.read(1)
            actual_text=self.__removePadding(bit_string)
            decompressed_text = self.__decodeText(actual_text)
            output.write(decompressed_text)
        return

def readcodes():
    binary_dict = {}
    with open("codes.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                char, binary = line.split(":")
                binary_dict[binary] = char
    return binary_dict

path = 'compressed.bin'
codes_dict=readcodes()
h = HuffmanCoding(path)
h.decompress()

