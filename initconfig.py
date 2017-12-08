from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
class AESCrypto():
    def __init__(self,key):
        if len(key)%16!=0:
            key=key+str((16-len(key)%16)*'0')
        self.key = key
        self.mode = AES.MODE_CBC
        #print(AES.block_size)

    def encrypt(self,text):
        if len(text)%16!=0:
            text=text+str((16-len(text)%16)*'0')
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext).decode("utf-8")

    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode("utf-8").rstrip('0')

def saveToDataFile(userid, userpassword):
    fw = open("config.txt","w")
    try:
        print(userid,file=fw)
        print(userpassword,file=fw)
    except:
        fw.close()

if __name__ == '__main__':
    internat_id = input("Enter your internat id: ")
    internat_pwd = input("Enter your password for " + internat_id + ": ")

    aes_key = input("Enter your encrption password :")
    pc = AESCrypto(aes_key)  # 初始化密钥
    en_user_name = pc.encrypt(internat_id)
    en_user_password = pc.encrypt(internat_pwd)

    saveToDataFile(en_user_name, en_user_password)
