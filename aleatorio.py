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

## En este caso actuate escoje un numero aleatorio del 1 al 6 y, si puede realiza esa accion la realiza y la imprime.
def actuate(mapa, posi):
	x1=0
	y1=0
	Suck = 0
	action = randrange(6)
	if(action == 0): #Arriba
		print("UP")
		y1+=1
	elif(action == 1):#Abajo
		print("DOWN")
		y1-=1
	elif(action == 2):#Derecha
		print("RIGHT")
		x1+=1
	elif(action == 3):#Izquierda
		print("LEFT")
		x1-=1
	elif(action == 4):#Chupar
		print("SUCK")
		if (mapa[posi.x][posi.y]=='1'):
			mapa[posi.x][posi.y]=0
	elif(action == 5): #Nada
		print("NOOP")

	if(can_move(mapa,posi.x+x1,posi.y+y1)):
		posi.x=x1 + posi.x
		posi.y=y1 + posi.y
	


##Funcion que percive lo que tiene a su alrededor y lo devuelve en el return, si está en el limite del mapa devuelve una X.
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
		
	return(posi.x,posi.y,currPos,izda,arriba,dcha,abajo)




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

	## Creo una posicion  e imprimo el mensaje, tras eso me muevo e imprimo un mensaje 15 veces ( menos la accion, que la imprime actuate)
	posi = Position(2,3)
	posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, posi)
	print("Initial position: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='')
	a =0
	iteraciones = 0
	while( iteraciones < 15):
		posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, posi)
		print("State: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='', end = '')
		actuate(Map,posi)
		iteraciones+=1




# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  	main()

