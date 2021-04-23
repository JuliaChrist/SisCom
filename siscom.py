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


#Configura a comunicação com um baudrate de 9600 
USB = serial.Serial('/dev/ttyACM0', 9600)
#Limpa o buffer
USB.flush()

while 1 :
	# com.write(a.encode())
	# print (a.encode())
	mensagem = input("Mensagem: ")

	# print(_in[1])
	# print(toASCII_dec(_in[1]))

	# print("Entrada em bytes: ", _in.encode())
	print("Entrada em binário: ", toBinary(mensagem))
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

