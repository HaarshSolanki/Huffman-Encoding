class BinaryTreeNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.freq_dict = {}
        self.codes = {}
        self.reverse_codes = {}

    def __make_frequency_dict(self, text):
        freq_dict = {char: 0 for char in "abcdefghijklmnopqrstuvwxyz0123456789,. "}
        for char in text:
            freq_dict[char] += 1
        sorted_chars = " ,.0123456789abcdefghijklmnopqrstuvwxyz"
        freq_dict = {char: freq_dict[char] for char in sorted_chars}
        # Generating frequency table text file
        with open("frequency.txt", "w") as f:
            for key, value in freq_dict.items():
                f.write("%s:%s\n" % (key, value))
        return freq_dict

    def __build_heap(self, freq_dict):
        heap = [BinaryTreeNode(key, value) for key, value in freq_dict.items()]
        return heap

    def __build_tree(self, heap):
        while len(heap) > 1:
            heap.sort(key=lambda x: x.freq)
            node1 = heap.pop(0)
            node2 = heap.pop(0)
            freq_sum = node1.freq + node2.freq
            new_node = BinaryTreeNode(None, freq_sum)
            new_node.left = node1
            new_node.right = node2
            heap.insert(0, new_node)
        return heap[0]

    def __build_codes_helper(self, root, curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.codes[root.value] = curr_bits
            self.reverse_codes[curr_bits] = root.value
            return
        self.__build_codes_helper(root.left, curr_bits + "1")
        self.__build_codes_helper(root.right, curr_bits + "0")

    def __build_codes(self, root, freq_dict):
        self.__build_codes_helper(root, "")

        # Generating codes.txt file
        with open("codes.txt", "w") as f:
            sorted_dict = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
            for keyf, valuef in sorted_dict.items(): 
                for key, value in self.codes.items():
                    if(keyf==key):
                        f.write("%s:%s\n" % (key, value))

    def __get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def __get_padded_encoded_text(self, encoded_text):
        padded_amount = 8 - (len(encoded_text) % 8)
        for _ in range(padded_amount):
            encoded_text += "0"
        padded_info = "{0:08b}".format(padded_amount)
        padded_encoded_text = padded_info + encoded_text
        return padded_encoded_text

    def __get_bytes_array(self, padded_encoded_text):
        array = []
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i : i + 8]
            array.append(int(byte, 2))
        return array

    def compress(self):
        # Read text from file
        output_path = "compressed" + ".bin"
        with open(self.path, "r+") as file, open(output_path, "wb") as output:
            text_ini = file.read()
            text_ini = text_ini.rstrip()
            # Make all whitespace characters change to regular space
            text_ini = text_ini.replace("\n", " ").replace("\t", " ").replace("\r", " ")
            # Convert all text to lowercase
            text_ini = text_ini.lower()
            # Ignore all characters except: A–Z, a–z, 0–9, comma, period, whitespace
            cleaned_lines = [
                "".join(c for c in line if c.isalnum() or c in "., ")
                for line in text_ini.split("\n")
            ]
            text = "\n".join(cleaned_lines)
            # Make freq_dict using the text
            self.freq_dict = self.__make_frequency_dict(text)
            # Construct the heap from the frequency_dict
            heap = self.__build_heap(self.freq_dict)
            # Construct the binary tree from the heap
            tree_root = self.__build_tree(heap)
            # Construct the codes from the binary tree
            self.__build_codes(tree_root, self.freq_dict)
            # Creating the encoded text using the codes
            encoded_text = self.__get_encoded_text(text)
            # Put this encoded text in the binary file
            # Pad this encoded text
            padded_encoded_text = self.__get_padded_encoded_text(encoded_text)
            bytes_array = self.__get_bytes_array(padded_encoded_text)
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
        return output_path


path = 'test1.txt'  # Enter name with extension
h = HuffmanCoding(path)
output_path = h.compress()
