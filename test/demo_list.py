# coding=utf-8

data = {'id': 1, 'userName': 'admin', 'token': '1654847651706B270B147B9EC41869AE76FC9E1614D33', 'walletJson': '{"address":"juc1dqy4nt8x9qzzg92zqazv6ds8q8vk2s7k22ma5k","id":"63af7fb8-215b-437a-9308-ccdea7f08011","version":3,"crypto":{"cipher":"aes-128-ctr","ciphertext":"8a5dc0ceb747661e36a2f082492e915328027b9a22e87752be1d40cfde65aa93","cipherparams":{"iv":"bd1e1b0dd70c509c590ed4ae437b896e"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":16384,"p":1,"r":8,"salt":"75d024d77ce283bbe4421cbb53e689552faaf389da7ebf109488a9775cf1a00d"},"mac":"f73dec7af3bdd625c1657732e93e323956b5122afc22d9549e775a864c5b3267"}}'}
print("walletJson:{0}".format(data["walletJson"]))
walletJson = eval(data["walletJson"])
print("walletJson的数据类型：{0}".format(type(walletJson)))
print(walletJson["address"])

