import serial

def toBinary (string):
	return "".join(f"{ord(i):08b}" for i in string)

com = serial.Serial('/dev/ttyACM0', 9600)
com.flush()
a = "abc"
while 1 :
	# com.write(a.encode())
	# print (a.encode())
	_in = input("Mensagem: ")

	print("Entrada em bytes: ", _in.encode())
	print("Entrada em binário: ", toBinary(_in))
	print("N° de bytes enviados: ", com.write(_in.encode()))



	string = com.readline().decode('ASCII').rstrip()

	print("Resposta: ",string)
	print("Resposta em Binário: ",toBinary(string))

	com.flush()

