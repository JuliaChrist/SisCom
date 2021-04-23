import serial

def toBinary (string):
	return "".join(f"{ord(i):08b}" for i in string)

def toASCII_dec (string):
	return "".join(f"{ord(i)}" for i in string)

def checksum (sum_mensagem,sum_resposta):
	if sum_mensagem == sum_resposta:
		return 1
	else:
		return 0

def sum_bytes(string):
	soma = 0
	for i in range (len(string)):
		soma = soma + int(toASCII_dec(string[i]))
	return soma


USB = serial.Serial('/dev/ttyACM0', 9600)
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
	print("N° de bytes enviados: ", USB.write(mensagem.encode()))

	print("________________________________________\n")

	resposta = USB.readline().decode('ASCII').rstrip()

	print("Resposta: ", resposta)
	print("Resposta em Binário: ", toBinary(resposta))
	print("Soma ASCII: ", sum_bytes(resposta), "\n")

	if (checksum(sum_bytes(mensagem),sum_bytes(resposta))):
		print("Checksum OK\n")
	else:
		print("Checksum NOT OK\n")
	



	USB.flush()

