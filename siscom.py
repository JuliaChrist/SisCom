import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import signal 


import serial

def toBinary (string): #transforma a entrada em valores bináros, sinal a ser transmitido. Codificação de linha NRZ Polar
	return "".join(f"{ord(i):08b}" for i in string)

def toASCII_dec (string): #transforma a entrada em valores ASCII decimais correspondentes
	return "".join(f"{ord(i)}" for i in string)

def checksum (sum_mensagem,sum_resposta):
	if sum_mensagem == sum_resposta:
		return 1
	else:
		return 0

def sum_bytes(string): #soma o valor dos bytes da entrada
	soma = 0
	for i in range (len(string)):
		soma = soma + int(toASCII_dec(string[i]))
	return soma






def plotar(_list):
	# _bin = []
	# for num in _list:
	# 	if num == 0:
	# 		_bin.extend((0,0))
	# 	else:
	# 		_bin.extend((1,1))

	prev = 0
	graph = [] 
	index = [0]
	i = 1
	for num in _list:
		if (num == 0):
			if prev == 0 :
				graph.extend((0,0))
				prev = 0
		else:
			graph.extend((1,1))

		if i != len(_list):
			index.extend((i,i))
		else:
			index.append(i)


		# index.extend((i,i)) if i != len(_list) else index.append(i)
		i +=1

	plt.plot(index, graph)
	plt.show()

#Configura a comunicação com um baudrate de 9600 
USB = serial.Serial('/dev/ttyACM0', 9600)
#Limpa o buffer
USB.flush()

in_list = []

# while 1 :

mensagem = input("Mensagem: ")


#Transformando mensagem (binária) em lista de números inteiros para plotar.
in_bin = toBinary(mensagem)
print(type(in_bin))
for i in range (len(in_bin)):
	in_list.append(int(in_bin[i]))
# print("deu? ",in_list)
plotar(in_list)

print("Entrada em binário: ",in_bin)
print("Entrada em ASCII: ", toASCII_dec(mensagem))
print("Soma ASCII: ", sum_bytes(mensagem))

	#Envia a mensagem para a serial
print("N° de bytes enviados: ", USB.write(mensagem.encode()))

print("________________________________________\n")

	#lê a serial
resposta = USB.readline().decode('ASCII').rstrip()

print("Resposta: ", resposta)
print("Resposta em Binário: ", toBinary(resposta))
print("Soma ASCII: ", sum_bytes(resposta), "\n")

	#mostra o valor em binário
print("Soma Binário: ",format(sum_bytes(mensagem),'b'), "\n")

if (checksum(sum_bytes(mensagem),sum_bytes(resposta))):
	print("Checksum OK\n")
else:
	print("Checksum NOT OK\n")
	

USB.flush()

