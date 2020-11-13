#!/usr/bin/python3
import sys
from random import randrange

from time import sleep

import random
import copy
import collections
import numbers

## Clase posicion que tiene x e y para usar el mapa
class Position:
	def __init__(self,x_pos,y_pos):
		self.x = x_pos
		self.y = y_pos

## Funcion que comprueba si me puedo mover a las coordenadas indicadas (Si hay una pared o un obstaculo no puedo)
def can_move(mapa, x, y):
	max_x = len(mapa)
	max_y = len(mapa[0])
	if(x<0 or x>=max_x or y<0 or y>=max_y or mapa[x][y]=='X'):
		return False
	return True

## Miro la situacion en la tabla y respondo acorde, me muevo si puedo imprimo la accion para completar el mensaje
def actuate(mapa, posi,tabla):
	x1 = 0
	y1=0
	posix,posiy,currPos,izda,arriba,dcha,abajo = percive(mapa, posi)
	respuesta = tabla[izda,arriba,dcha,abajo,currPos]

	if(respuesta== 'suck'):
		print("SUCK")
		mapa[posi.x][posi.y]=0
	elif(respuesta== 'izquierda'):
		print("LEFT")
		x1-=1
	elif(respuesta== 'arriba'):
		print("UP")
		y1+=1
	elif(respuesta== 'abajo'):
		print("DOWN")
		y1-=1
	elif(respuesta== 'derecha'):
		print("RIGHT")
		x1+=1
	elif(respuesta== 'error'):
		print("Por favor elija una posicion valida")
		exit()
	
	if(can_move(mapa,posi.x+x1,posi.y+y1)):
		posi.x=x1 + posi.x
		posi.y=y1 + posi.y	

## Funcion que percive lo que tiene a su alrededor y lo devuelve en el return, si está en el limite del mapa devuelve una X.
def percive(mapa, posi):
	x = posi.x
	y = posi.y
	currPos = mapa[x][y]
	if((x-1)<0):
		izda = "X"
	else:
		izda = mapa[x-1][y]
	
	if((x+1)>4):
		dcha = "X"
	else:
		dcha = mapa[x+1][y]

	if((y-1)<0):
		abajo = "X"
	else:
		abajo = mapa[x][y-1]
	
	if((y+1)>4):
		arriba = "X"
	else:
		arriba = mapa[x][y+1]
	return(posi.x,posi.y,currPos,izda,arriba,dcha,abajo )



## Creo la tabla usando 5 bucles para comprobar todas las percepciones que puede tener el robot, y en  cada caso hace una cosa, si está en un 1 limpia.

def make_table():
	tabla = {}
	cosas = ['0','1','X']

	for a in cosas:
		for b in cosas:
			for c in cosas:
				for d in cosas:
					for e in cosas:
						if (e == 'X'):
							#situacion imposible, si pasa es que las coordenadas iniciales no son validas, asi que paso error y salgo en actuate
							tabla[a,b,c,d,e] = 'error'
						elif (e == 1):
							tabla[a,b,c,d,e] = 'suck'
						elif (a == 1):
							tabla[a,b,c,d,e] = 'suck'
						elif (b == 1):
							tabla[a,b,c,d,e] = 'suck'
						elif (c == 1):
							tabla[a,b,c,d,e] = 'suck'
						elif (d == 1):
							tabla[a,b,c,d,e] = 'suck'

						elif (a == 0 or a == 'X'):
							tabla[a,b,c,d,e] = 'derecha'
						elif (b == 0 or b == 'X'):
							tabla[a,b,c,d,e] = 'abajo'
						elif (c == 0 or c == 'X'):
							tabla[a,b,c,d,e] = 'izquierda'
						elif (d == 0 or d == 'X'):
							tabla[a,b,c,d,e] = 'arriba'

	return tabla

def main():
	## Creo un array de 5x5 que usaré como mapa ( ya que no tengo sensores lo uso para comprobar el estado y la percepcion)
	rows, cols = (5, 5) 
	Map = [[0 for i in range(cols)] for j in range(rows)] 
	
	i = 0
	j = 4
	file = open(sys.argv[1], 'r')
	for line in file:
		for word in line.split():
			Map[i][j] = word 
			i = i+1
		i = 0
		j= j-1
		
	
	posi = Position(2,3)
	posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, posi)
	print("Initial position: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='', end = '')
	a = 0
	iteraciones = 0

	tabla = make_table()
						
	#print("lo de la tbala en ", tabla['1','0','0','0','0'])
	while( iteraciones < 15):
		posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, posi)
		print("State: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='', end = '')
		actuate(Map,posi, tabla)
		iteraciones+=1	 ##Lo ejecuto 15 veces, si quiero hacerlo hasta que acabe uso el toclean en el while



	


	

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  	main()

