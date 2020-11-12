
def actuate(mapa, posi, to_clean):
	x1=0
	y1=0
	Suck = 0
	action = randrange(6)
	if(action == 0): #Arriba
		print( "^")
		y1+=1
	elif(action == 1):#Abajo
		print("v")
		y1-=1
	elif(action == 2):#Derecha
		print(">")
		x1+=1
	elif(action == 3):#Izquierda
		print("<")
		x1-=1
	elif(action == 4):#Chupar
		if (mapa[posi.x][posi.y]=='1'):
			mapa[posi.x][posi.y]=0
			to_clean-=1
	elif(action == 5): #Nada
		print(" ")

	if(can_move(mapa,posi.x+x1,posi.y+y1)):
		posi.x=x1 + posi.x
		posi.y=y1 + posi.y
	return to_clean
	


def percive(mapa, posi):
	x = posi.x
	y = posi.y
	currPos = mapa[x][y]
	if((x-1)<0):
		izda = "M"
	else:
		izda = mapa[x-1][y]
	
	if((x+1)>4):
		dcha = "M"
	else:
		dcha = mapa[x+1][y]

	if((y-1)<0):
		abajo = "M"
	else:
		abajo = mapa[x][y-1]
	
	if((y+1)>4):
		arriba = "M"
	else:
		arriba = mapa[x][y+1]
		# llamar a accion, creo un num aletorio y devuelve la posicion modificada (si se ha modificado) y la accion aleatoria que se ha hecho
		# 
	print(posi.x,",", posi.y,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='', end = '')
	return(posi.x,posi.y, )


def main():
	rows, cols = (5, 5) 
	
	Map = [[0 for i in range(cols)] for j in range(rows)] 
	
	i = 0
	j = 4
	to_clean = 0
	file = open(sys.argv[1], 'r')
	for line in file:
		for word in line.split():
			Map[i][j] = word 
			if(word == "1"):
				to_clean = to_clean +1
			i = i+1
		i = 0
		j= j-1
		
	
	print(Map[2][0])
	print("To clean: ", to_clean)
	posi = Position(2,3)
	print("Initial position: <",sep='',end = '')
	percive(Map, posi)
	a =0
	iteraciones = 0;



	#creo la tabla
	tabla = {}
	cosas = [0,1,'X']

	for a in cosas:
		for b in cosas:
			for c in cosas:
				for d in cosas:
					for e in cosas:
						if (e == 'X'):
							print("eso no se puede")
						elif (e == 1):
							tabla[a,b,c,d,e] = Suck
						elif (a == 1):
							tabla[a,b,c,d,e] = izquierda
						elif (b == 1):
							tabla[a,b,c,d,e] = arriba
						elif (c == 1):
							tabla[a,b,c,d,e] = derecha
						elif (d == 1):
							tabla[a,b,c,d,e] = abajo

						elif (a == 0 or a == 'X'):
							tabla[a,b,c,d,e] = derecha
						elif (b == 0 or b == 'X'):
							tabla[a,b,c,d,e] = arriba
						elif (c == 0 or c == 'X'):
							tabla[a,b,c,d,e] = derecha
						elif (d == 0 or d == 'X'):
							tabla[a,b,c,d,e] = abajo
						

	while( iteraciones < 15):
		print("To clean: ", to_clean)
		print("State: <",sep='',end = '')
		percive(Map, posi)
		left = actuate(Map,posi, to_clean)
		to_clean = left	
		iteraciones+=1	 ##Lo ejecuto 15 veces, si quiero hacerlo hasta que acabe uso el toclean en el while
	print()



	


	

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  	main()

