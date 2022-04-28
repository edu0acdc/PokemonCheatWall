from staticInfo import get_data_order, get_fields, get_pokemon_name, xor_hex


class Pokemon():
    def __init__(self, attributes={}):
        self.attributes = attributes
        self.pokemonData = None
        if int(attributes['personality_value'], 16) > 0:
            self.pokemonData = PokemonData(
                attributes['data'], attributes['personality_value'], attributes['ot_id'], attributes['checksum'])

    def changeFieldHex(self, field, value):
        if field in self.attributes:
            self.attributes[field] = value
        else:
            self.pokemonData.updateFieldHEX(field, value)


class SubStructure():
    def __init__(self, name, encrypted_words, decrypt_key) -> None:
        self.name = name
        self.fields = {}
        self.decrypt_key = decrypt_key
        decrypted_words_joined = []
        for enc_word in encrypted_words:
            dyc_word = xor_hex(enc_word, self.decrypt_key)
            dyc_word = dyc_word[2:].upper()
            while len(dyc_word) < 8:
                dyc_word = '0' + dyc_word
            decrypted_words_joined.insert(0, dyc_word)

        decrypted_words_joined = ''.join(decrypted_words_joined)
        self.fields = get_fields(self.name)
        for field in self.fields:
            offset = self.fields[field][0]
            size = self.fields[field][1]
            # hex_value = decrypted_words_joined[offset*2:(offset+size)*2]
            new_offset = len(decrypted_words_joined)-offset*2
            hex_value = decrypted_words_joined[new_offset -
                                               (size*2):new_offset]

            dec_value = int(hex_value, 16)
            self.fields[field] = (offset, size, hex_value, dec_value)

    def changeFieldHEX(self, field, hex_value):
        vals = self.fields[field]
        self.fields[field] = (vals[0], vals[1], hex_value, int(hex_value, 16))

    def changeFieldDEC(self, field, dec_value):
        vals = self.fields[field]
        self.fields[field] = (vals[0], vals[1], hex(dec_value), dec_value)

    def fieldsToWords(self):
        hex_values = []
        current_bytes = 0
        current_word = ""
        for field in self.fields:
            current_word = self.fields[field][2] + current_word
            current_bytes += self.fields[field][1]
            if current_bytes == 4:
                current_bytes = 0
                hex_values.append(current_word)
                current_word = ""
        return hex_values

    def getChecksum(self):
        hex_values = self.fieldsToWords()
        suma = 0
        for hex_v in hex_values:
            suma += int(hex_v, 16)
        return suma

    def getEncryptedString(self):
        hex_values = self.fieldsToWords()
        s = ""
        for hex_val in hex_values:
            i = 0
            enc_val = xor_hex(hex_val, self.decrypt_key)
            enc_val = enc_val[2:].upper()
            word1 = enc_val[:2]
            word2 = enc_val[2:4]
            word3 = enc_val[4:6]
            word4 = enc_val[6:8]
            s += word4 + " " + word3 + " " + word2 + " " + word1 + " "
        return s

    def getString(self):
        s = ""
        for field in self.fields:
            s += field + " =>  "+str(self.fields[field]) + "\n"

        return s

    def __repr__(self) -> str:
        # return str(self.decrypted_words) + " || "+str(self.encrypted_words)
        return self.getString()

    def __str__(self) -> str:
        return self.getString()


class PokemonData():
    def __init__(self, encrypted_string, personality_value, ot_id, original_checksum) -> None:
        self.original_checksum = original_checksum
        self.current_checksum = original_checksum
        self.ot_id = ot_id
        self.personality_value = personality_value
        self.encrypted_string = encrypted_string.replace("0x", "")
        self.data = {}
        self.encrypted_data = {}
        self.buildData()
        self.calculateChecksum()

    def buildData(self):
        decrypt_key = xor_hex(self.personality_value, self.ot_id)
        data_str_split = [self.encrypted_string[i:i+8]
                          for i in range(0, len(self.encrypted_string), 8)]
        data_str_split.reverse()
        groups = get_data_order(self.personality_value)
        for group in groups:
            self.encrypted_data[group] = []

        for i in range(len(data_str_split)):
            self.encrypted_data[groups[int(i/3)]].append(data_str_split[i])
        # while i < len(data_str_split) - 3:
        #     index = int(i / 12)
        #     word = ""
        #     byte1 = data_str_split[i]
        #     byte2 = data_str_split[i+1]
        #     byte3 = data_str_split[i+2]
        #     byte4 = data_str_split[i+3]
        #     word += byte4
        #     word += byte3
        #     word += byte2
        #     word += byte1

        #     i += 4

        for group in self.encrypted_data:
            self.data[group] = SubStructure(
                group, self.encrypted_data[group], decrypt_key)

    def getEncryptedData(self):
        s = ""
        for group in self.data:
            s += self.data[group].getEncryptedString()
        return s

    def calculateChecksum(self):
        sum = 0
        for group in self.data:
            sum += self.data[group].getChecksum()
        sum = hex(sum)
        self.current_checksum = int(
            sum[2:6], 16) + int(sum[6:10], 16)

    def updateChecksum(self):
        self.calculateChecksum()
        self.original_checksum = self.current_checksum

    def updateFieldHEX(self, field, hex_value):
        for group in self.data:
            if field in self.data[group].fields:
                self.data[group].changeFieldHEX(field, hex_value)
                break
        self.updateChecksum()

    def updateFieldDEC(self, group, field, dec_value):
        self.data[group].changeFieldDEC(field, dec_value)
        self.updateChecksum()

    def __repr__(self) -> str:
        name = get_pokemon_name(self.data['G'].fields['Species'][-1])
        s = "------------------------------\n"+name+"\n------------------------------\n"
        for group in self.data:
            s += str(self.data[group]) + "\n"

        s += "-----------------------\n"
        s += "CURRENT CHECKSUM "+str(self.current_checksum)+"\n"
        s += "ORIGINAL CHECKSUM "+str(self.original_checksum)+"\n"
        return s
