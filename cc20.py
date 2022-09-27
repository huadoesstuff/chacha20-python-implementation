import struct
import os

def xor_stream(key, nonce, position=0):
  #define bit rotation
  def rotate(v, c):
    return ((v << c) & 0xffffffff) | v >> (32 - c)
  
  # define the quarter round
  def quarter_round(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 16)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 12)
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 8)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 7)

  # define the state <- copilot wrote that
  ctx = [0] * 16
  
  # first 4 constant words
  ctx[:4] = (1634760805, 857760878, 2036477234, 1797285236)
  
  # next 8 pieces are the key
  ctx[4 : 12] = struct.unpack('<8L', key)
  
  # next 2 are the counter
  ctx[12] = position
  
  # last 2 are the nonce
  ctx[13 : 16] = struct.unpack('<LLL', nonce)
  
  # apply the 10 rounds to scramble the bytes
  while 1:
    # changes the ctx with x using placeholders or somewthing idk
    x = list(ctx)
    # 10 rounds of rows and diaganols
    for i in range(10):
      quarter_round(x, 0, 4,  8, 12)
      quarter_round(x, 1, 5,  9, 13)
      quarter_round(x, 2, 6, 10, 14)
      quarter_round(x, 3, 7, 11, 15)
      quarter_round(x, 0, 5, 10, 15)
      quarter_round(x, 1, 6, 11, 12)
      quarter_round(x, 2, 7,  8, 13)
      quarter_round(x, 3, 4,  9, 14)
    # add the scrambled bytes to the original bytes (i think, the github copilot ai said that)
    for c in struct.pack('<16L', *(
        (x[i] + ctx[i]) & 0xffffffff for i in range(16))):
      yield c
    ctx[12] = (ctx[12] + 1) & 0xffffffff


def chacha20_encrypt(data, key, nonce=None, position=0):
  # the actual xor function
  return bytes(a ^ b for a, b in
      zip(data,xor_stream(key, nonce, position)))

# variables for encryption only ig
key = os.urandom(32)
nonce = os.urandom(12)

def runchacha20(data, key, nonce):
  #encrypt the data
  ciphertext = chacha20_encrypt(data, key, nonce)
  # print results and stuff
  print('nonce: ', nonce)
  print('key: ', key)
  print('ciphertext: ', ciphertext)
  return ciphertext