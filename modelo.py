#!/usr/bin/python3
import sys
from random import randrange

from time import sleep

import random
import copy
import collections
import numbers

## Clase agente que tiene x e y  y un mapa interno que al empezar es desconocido

class Agente:
	def __init__(self,x_pos,y_pos, mapa_agente):
		self.x = x_pos
		self.y = y_pos
		self.mapa = mapa_agente

## Funcion que comprueba si me puedo mover a las coordenadas indicadas (Si hay una pared o u obstaculo no puedo)
def can_move(mapa, x, y):
	max_x = len(mapa)
	max_y = len(mapa[0])
	if(x<0 or x>=max_x or y<0 or y>=max_y or mapa[x][y]=='X'):
		return False
	return True

## Comprueba si hay suciedad o algo no visto en el mapa (8 es desconocido)
def all_clear(agent):
	limpio = True
	for row in range(5):
		for val in range(5):
			if(agent.mapa[row][val]==8 or agent.mapa[row][val]=='1'):
				limpio = False
	return limpio

## Se mueve aleatoriamente si puede menos si ve un 1 que li limpia, cada vez que se ejeuta compruebo si todo el mapa está limpio para acabar
def actuate(mapa, agent):
	x1=0
	y1=0
	if (mapa[agent.x][agent.y]=='1'):
		mapa[agent.x][agent.y]=0
		print("SUCK")

	else:
		action = randrange(4)
		if(action == 0): #Arriba
			print( "UP")
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
			
	if(can_move(mapa,agent.x+x1,agent.y+y1)):
		agent.x=x1 + agent.x
		agent.y=y1 + agent.y

	if(all_clear(agent)):
		print("Acabado")
		return(1, agent.x, agent.y)
	return (0, agent.x, agent.y)


##Funcion que percive lo que tiene a su alrededor y lo devuelve en el return, si está en el limite del mapa devuelve una X.
## Además actualizo el mapa interno del agente con lo que percive
def percive(mapa, agent):
	x = agent.x
	y = agent.y
	currPos = mapa[x][y]
	agent.mapa[x][y] = mapa[x][y]
	if((x-1)<0):
		izda = "X"
	else:
		izda = mapa[x-1][y]
		agent.mapa[x-1][y] = mapa[x-1][y]
	if((x+1)>4):
		dcha = "X"
	else:
		dcha = mapa[x+1][y]
		agent.mapa[x+1][y] = mapa[x+1][y]
	if((y-1)<0):
		abajo = "X"
	else:
		abajo = mapa[x][y-1]
		agent.mapa[x][y-1] = mapa[x][y-1]
	if((y+1)>4):
		arriba = "X"
	else:
		arriba = mapa[x][y+1]
		agent.mapa[x][y+1] = mapa[x][y+1]
	return(agent.x,agent.y,currPos,izda,arriba,dcha,abajo )


def main():
	## Creo un array de 5x5 que usaré como mapa ( ya que no tengo sensores lo uso para comprobar el estado y la percepcion)
	rows, cols = (5, 5)
	Map = [[0 for i in range(cols)] for j in range(rows)]
	agent_map = [[8 for i in range(cols)] for j in range(rows)] #Creo un mapa con todo a 8 que representa no saber lo que hay, cuando voy percibiendo lo cambio

	i = 0
	j = 4
	file = open(sys.argv[1], 'r')
	for line in file:
		for word in line.split():
			Map[i][j] = word
			if(word == "1"):
				i = i+1
		i = 0
		j= j-1

	## Creo la accion y un agente que tiene una posicion y un mapa, despues imprimo mi  estado actual
	action = 0
	agent = Agente(0,0,agent_map)
	posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, agent)
	print("Initial position: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='')
	while( action != 1):	## Siempre que la accion sea distinto de 1 (No operation) sigo ejecutando el bucle e imprimiendo es mapa del agente
		posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, agent)
		print("State: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='', end = '')
		action, anteriorx,anteriory = actuate(Map,agent)
		for row in range(5):
			for val in range(5):
				print (agent.mapa[val][4-row],end = '')
			print(" ")


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  	main()

