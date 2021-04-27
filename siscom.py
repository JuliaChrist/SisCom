import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import signal 


import serial

def toBinary (string): #transforma a entrada em valores bináros, sinal a ser transmitido. Codificação de linha NRZ Polar
	return "".join(f"{ord(i):08b}" for i in string)

def toBinaryList (string):
	_list = []
	str_bin = toBinary(string)
	for i in range (len(str_bin)):
		_list.append(int(str_bin[i]))

	return _list


def toASCII_dec (string): #transforma a entrada em valores ASCII decimais correspondentes
	return "".join(f"{ord(i)}" for i in string)

def checksum (sum_mensagem,sum_resposta):
	if sum_mensagem == sum_resposta:
		return 1
	else:
		return 0

def sum_bytes (string): #soma o valor dos bytes da entrada
	soma = 0
	for i in range (len(string)):
		soma = soma + int(toASCII_dec(string[i]))
	return soma

def plotar (_list, sig):
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
		i +=1

	if(sig == "msg"):
		plt.subplot(2, 1, 1)
		plt.title("Mensagem Enviada:")
		plt.plot(index, graph)
	else:
		plt.subplot(2, 1, 2)
		plt.title("Mensagem Recebida:")
		plt.plot(index, graph)

#Configura a comunicação com um baudrate de 9600 
USB = serial.Serial('/dev/ttyACM0', 9600)
#Limpa o buffer
USB.flush()

#Recebendo mensagem via terminal
mensagem = input("Mensagem: ")

in_list = toBinaryList(mensagem)
plotar(in_list, "msg")

print("Entrada em binário: ",toBinary(mensagem))
print("Entrada em ASCII: ", toASCII_dec(mensagem))
print("Soma ASCII: ", sum_bytes(mensagem))
#Envia a mensagem para a serial
print("N° de bytes enviados: ", USB.write(mensagem.encode()))

print("________________________________________\n")

#lê a serial
resposta = USB.readline().decode('ASCII').rstrip()

out_list = toBinaryList(resposta)
plotar(out_list, "rsp")

print("Resposta: ", resposta)
print("Resposta em Binário: ", toBinary(resposta))
print("Soma ASCII: ", sum_bytes(resposta), "\n")

#mostra o valor em binário
# print("Soma Binário: ",format(sum_bytes(mensagem),'b'), "\n")

if (checksum(sum_bytes(mensagem),sum_bytes(resposta))):
	print("Checksum OK\n")
else:
	print("Checksum NOT OK\n")
	

USB.flush()
plt.tight_layout()
# plt.show()

