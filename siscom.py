import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import signal 


import serial

def String_to_Binary (string): #transforma a entrada em valores bináros, sinal a ser transmitido. Codificação de linha NRZ Polar
	return "".join(f"{ord(i):08b}" for i in string)

def String_to_Int_List (string):
	_list = []
	# str_bin = toBinary(string)
	for i in range (len(string)):
		_list.append(int(string[i]))

	return _list

def Binary_to_ASCII (string):
	binary_int = int(string, 2)
	byte_number = binary_int.bit_length() + 7 // 8
	binary_array = binary_int.to_bytes(byte_number, "big")
	return(binary_array.decode())

def String_to_ASCII_Dec (string): #transforma a entrada em valores ASCII decimais correspondentes
	return "".join(f"{ord(i)}" for i in string)

def checksum (sum_mensagem,sum_resposta):
	if sum_mensagem == sum_resposta:
		return 1
	else:
		return 0

def Sum_Bytes (string): #soma o valor dos bytes da entrada
	soma = 0
	for i in range (len(string)):
		soma = soma + int(String_to_ASCII_Dec(string[i]))
	return soma

def Plot_Graph (_list, sig):
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

while(mensagem != "q"):

	in_list = String_to_Int_List(String_to_Binary(mensagem))
	Plot_Graph(in_list, "msg")

	print("Entrada: ", mensagem)
	print("Entrada em Binário: ",String_to_Binary(mensagem))
	# print("Entrada em ASCII: ", String_to_ASCII_Dec(mensagem))
	# print("Soma ASCII: ", Sum_Bytes(mensagem))
	#Envia a mensagem para a serial

	USB.write(mensagem.encode())
	# print("N° de bytes enviados: ", USB.write(mensagem.encode()))

	print("________________________________________\n")

	#lê a serial
	resposta = USB.readline().decode('ASCII').rstrip()

	out_list = String_to_Int_List(resposta)
	Plot_Graph(out_list, "rsp")

	print("Resposta: ", Binary_to_ASCII(resposta))
	print("Resposta em Binário: ", resposta)
	# print("Resposta em ASCII: ", String_to_ASCII_Dec(Binary_to_ASCII(resposta)))
	# print("Soma ASCII: ", Sum_Bytes(Binary_to_ASCII(resposta)), "\n")

	#mostra o valor em binário
	# print("Soma Binário: ",format(sum_bytes(mensagem),'b'), "\n")

	# if (checksum(Sum_Bytes(mensagem),Sum_Bytes(resposta))):
	# 	print("Checksum OK\n")
	# else:
	# 	print("Checksum NOT OK\n")
		
	USB.flush()
	plt.tight_layout()
	plt.show()

	mensagem = input("Mensagem: ")

