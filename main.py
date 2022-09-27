import cc20

# encryption: change the data variable to 'input('what is the data you want to encrypt: ').encode()'
# encryption: change the key variable to 'cc20.key'
# encryption: change the nonce variable to 'cc20.nonce'

# decryption: change the data variable to the ciphertext (add the b)
# decryption: change the key variable to the key provided in the print in the console
# decryption: to switch to decryption, change the nonce variable to the nonce provided in the print in the console

data = input('what is the data you want to encrypt: ').encode()
key = cc20.key
nonce = cc20.nonce
cc20.runchacha20(data, key, nonce)