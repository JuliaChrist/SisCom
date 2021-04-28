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

def Binary_to_Dec(string):
	dec = String_to_Int_List(string)
	exp = 1
	for i in range (8,0):
		aux += dec[i] * exp
		exp = exp * 2
	return aux




def Binary_to_ASCII (string):
	binary_int = int(string, 2)
	byte_number = binary_int.bit_length() + 7 // 8
	binary_array = binary_int.to_bytes(byte_number, "big")
	return(binary_array.decode())



def String_to_ASCII_Dec (string): #transforma a entrada em valores ASCII decimais correspondentes
	return "".join(f"{ord(i)}" for i in string)

def checksum (sum_mensagem,sum_resposta):
	# Independentemente da base numérica utilizada, as operações matemáticas aplicadas geram o mesmo resultado, portanto, a soma na base decimal resulta no mesmo 
	# valor que a soma na base binária.
	# Nessa aplicação, utilizamos a soma em decimal, pois é a base usada pela linguagem Python para as operações matemáticas.
	if sum_mensagem == sum_resposta:
		return 1
	else:
		return 0

def Sum_Bytes (string): #soma o valor dos bytes da entrada
# Independentemente da base numérica utilizada, as operações matemáticas aplicadas geram o mesmo resultado, portanto, a soma na base decimal resulta no mesmo 
# valor que a soma na base binária.
# Nessa aplicação, utilizamos a soma em decimal, pois é a base usada pela linguagem Python para as operações matemáticas.
	soma = 0
	for i in range (len(string)):
		soma = soma + int(String_to_ASCII_Dec(string[i]))
	return soma

def Insert_Checksum(String):
	mensagem = str(Sum_Bytes(mensagem))



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

	print("Entrada (ASCII): ", mensagem)
	print("Entrada (Binário): ",String_to_Binary(mensagem))
	print("Entrada (Decimal): ", String_to_ASCII_Dec(mensagem))



#checksum
	char_checksum = String_to_Binary(chr(Sum_Bytes(mensagem)))
	print("soma bináriooooo: ", char_checksum)

	char_checksum_inv = ""
	for i in range (len(char_checksum)):
		if char_checksum[i] == '1':
			char_checksum_inv += '0'
		else:
			char_checksum_inv += '1'

	print("soma binário invertidoooooo: ", char_checksum_inv)
	char_checksum_list = String_to_Int_List(char_checksum_inv)
	exp = 128
	soma_bin = 0
	for i in range (len(char_checksum_list)):
		soma_bin += int(char_checksum_list[i] * exp)
		exp = exp / 2

	mensagem += chr(soma_bin)
	print("Mensagem com CheckSum ASCII: ", String_to_ASCII_Dec(mensagem))
	print("Mensagem com CheckSum: ", String_to_Binary(mensagem))
#end checksum




	in_list = String_to_Int_List(String_to_Binary(mensagem))
	Plot_Graph(in_list, "msg")

	#Envia a mensagem para a serial
	USB.write(mensagem.encode())

	print("________________________________________\n")

	#lê a serial

	batata = USB.readline()#.decode('ASCII').rstrip()
	resposta = str(batata , 'utf-8')
	resposta = resposta.rstrip()
	print(resposta)

	out_list = String_to_Int_List(String_to_Binary(resposta))
	Plot_Graph(out_list, "rsp")

	print("Resposta (ASCII): ", resposta)
	print("Resposta (Binário): ", String_to_Binary(resposta))
	print("Resposta (Decimal): ", String_to_ASCII_Dec(resposta))

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

