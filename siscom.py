import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import signal 


import serial

def String_to_Binary (string):
	'''
	Transforma um string de caracteres em uma string contendo seu equivalente em valor binário;
	Recebe: String contendo a mensagem;
	Retorna: string contendo o valor da menságem em binário.
	'''
	return "".join(f"{ord(i):08b}" for i in string)

def String_to_Int_List (string):
	'''
	Converte uma string contendo um valor binário em uma lista de valores inteiros, de tamanho igual ao número de bits da mensagem contina na string;
	Recebe: String com a mensagem em binário;
	Retorna: Lista de inteiros.
	'''
	_list = []
	# str_bin = toBinary(string)
	for i in range (len(string)):
		_list.append(int(string[i]))

	return _list

def Binary_to_Dec(string):
	'''
	Converte uma string contendo uma mensagem em binário em seu valor decimal correspondednte;
	Recebe: String de valores em binário;
	Retorna: Inteiro contendo o valor decimal.
	'''
	global aux
	dec = String_to_Int_List(string)
	exp = 128
	for i in range ((len(dec) - 8), len(dec)):
		aux += dec[i] * exp
		exp = exp / 2
	return int(aux)

def Binary_to_ASCII (string):
	'''
	Converte uma string contendo uma mensagem em binário em uma string com os characteres correspondentes da tabela ASCII;
	Recebe: String com a mensagem em binário;
	Retorna: String com os caracteres ASCII.
	'''
	binary_int = int(string, 2)
	byte_number = binary_int.bit_length() + 7 // 8
	binary_array = binary_int.to_bytes(byte_number, "big")
	return(binary_array.decode())

def String_to_Dec (string):
	'''
	Converte uma string contendo uma mensagem em texto em seu valor decimal correspondente, caractere por caractere;
	Recebe: String contendo mensagem em texto;
	Retorna: String contendo decimais equivalentes
	'''
	return "".join(f"{ord(i)}" for i in string)

def Sum_Bytes (string):
	'''
	Soma os bytes da string de entrada;
	Recebe: string contendo a mensagem;
	Retorna: soma dos bytes da string, em inteiro.

	Obs.: Independentemente da base numérica utilizada, as operações matemáticas aplicadas geram o mesmo resultado, portanto, 
	a soma na base decimal resulta no mesmo valor que a soma na base binária. Nessa aplicação, utilizamos a soma em decimal,
	pois é a base usada pela linguagem Python para as operações matemáticas.

	'''
	soma = 0
	for i in range (len(string)):
		soma = soma + int(String_to_Dec(string[i]))
	return soma

def Insert_Sum(string):
	'''
	Insere o inverso (binário) da soma dos bits da mensagem. Usado no método CheckSum;
	Recebe: string contendo a mensagem
	Retorna: string com a mensagem + soma;
	'''
	char_checksum = String_to_Binary(chr(Sum_Bytes(string)))
	# print("soma binário: ", char_checksum)

	char_checksum_inv = ""
	for i in range (len(char_checksum)):
		if char_checksum[i] == '1':
			char_checksum_inv += '0'
		else:
			char_checksum_inv += '1'

	# print("soma binário invertido: ", char_checksum_inv)
	char_checksum_list = String_to_Int_List(char_checksum_inv)
	exp = 128
	soma_bin = 0
	for i in range (len(char_checksum_list)):
		soma_bin += int(char_checksum_list[i] * exp)
		exp = exp / 2

	string += chr(soma_bin)
	# print("Mensagem com CheckSum ASCII: ", String_to_Dec(string))
	print("Mensagem (c/ CheckSum): ", String_to_Binary(string))

	return(string)

def Checksum (mensagem,soma):
	'''
	Confere se ocorreu algum erro na transmissão da mensagem (método de detecção de erros CheckSum) e 
	imprime na tela uma mensagem com o resultado do teste;
	
	Recebe: mensagem recebida, soma recebida

	'''
	if (((Sum_Bytes(mensagem)) + (Sum_Bytes(soma))) == 255):
		print("\n_ _ _ _ _ CHECKSUM OK! Mensagem recebida sem erro(s) _ _ _ _ _\n")
	else:
		print("\n_ _ _ _ _ CHECKSUM NOK! Mensagem recebida com erro(s) _ _ _ _ _\n")	

def Plot_Graph (_list, sig):
	'''
	Plota o sinal em um gráfico;
	Recebe: Lista com valores inteiros ; tipo de sinal (enviado ou recebido).
	'''
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

#Recebendo mensagem via terminal. O caractere 'q' encerra a aplicação.
mensagem = input("Mensagem: ")

while(mensagem != "q"):
	aux = 0

	# print("Entrada (ASCII): ", mensagem)
	print("Mensagem (Binário): ",String_to_Binary(mensagem))
	# print("Entrada (Decimal): ", String_to_Dec(mensagem))

	mensagem = Insert_Sum(mensagem)

	in_list = String_to_Int_List(String_to_Binary(mensagem))
	Plot_Graph(in_list, "msg")

	#Envia a mensagem para a serial
	USB.write(mensagem.encode())

	print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n")

	#Lê a serial
	batata = USB.readline()#.decode('ASCII').rstrip()
	resposta = str(batata , 'utf-8')
	resposta = resposta.rstrip()

	out_list = String_to_Int_List(String_to_Binary(resposta))
	Plot_Graph(out_list, "rsp")

	soma = resposta[-1::]
	resp_mensagem = resposta[:-1]

	print("Resposta (ASCII): ", resp_mensagem)
	print("Resposta (Binário): ", String_to_Binary(resp_mensagem))
	# print("Resposta (Decimal): ", String_to_Dec(resp_mensagem))
	# print("Resposta Soma: ", soma)

	Checksum(resp_mensagem, soma)

	#mostra o valor em binário (sem salvar em string)
	# print("Soma Binário: ",format(sum_bytes(mensagem),'b'), "\n")
	
	plt.tight_layout()
	plt.show()

	USB.flush()
	mensagem = input("Mensagem: ")

