#!/usr/bin/python3
import sys
from random import randrange

from time import sleep

import random
import copy
import collections
import numbers
import math

## Clase agente que tiene x e y  y un mapa interno que al empezar es desconocido
class Agente:
	def __init__(self,x_pos,y_pos, mapa_agente):
		self.x = x_pos
		self.y = y_pos
		self.mapa = mapa_agente

## Funcion que comprueba si me uedo mover a las coordenadas indicadas (Si hay una pared o u obstaculo no puedo)
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

## Busca el la suciedad o lo desconocido más cercano para moverse hacia ello y ser más eficiente
## calcula la distancia a todos y elije el mas cercano
def buscar(agente):
	i = 0
	j = 4
	distancia = 10
	for line in range(5):
		for word in range(5):
			word = agente.mapa[i][j]
			if (word=='1' or word == 8):
				temporal = math.sqrt(abs(i-agente.x)+ abs(j-agente.y))  
				if( temporal < distancia):
					distancia = temporal
					X = i
					Y = j
			i = i+1
		i = 0
		j = j-1
	return(X,Y)

## Comprueba si estoy atascado (Si lleva 3 iteraciones en el mismo sitio) leyendo las posiciones anteriores
def stuck(anteriores):
	if(anteriores[1][4]==anteriores[1][3]==anteriores[1][2] and anteriores[0][4]==anteriores[0][3]==anteriores[0][2]):
		return True
	return False
	
## Se mueve hacia un 1 si lo detecta y si no busca un 1 o algo desconocido cerca, y va hacia ello, si se cruza con un bstaculo se mueve para evitarlo.
def actuate(mapa, agent, anteriores, energia):

	if(all_clear(agent)):
		print("Acabado")
		return(1, agent.x, agent.y, energia)
	x1=0
	y1=0
	energia_devolver = energia -1
	if (mapa[agent.x][agent.y]=='1'):
			mapa[agent.x][agent.y]=0
			print("SUCK")
			energia_devolver = energia +100
	elif(agent.x+1<=4 and mapa[agent.x+1][agent.y]=='1'):
		x1+=1
		print("RIGHT")
	elif(agent.x-1>=0 and mapa[agent.x-1][agent.y]=='1'):
		x1-=1
		print("LEFT")
	elif(agent.y+1<=4 and mapa[agent.x][agent.y+1]=='1'):
		y1+=1
		print("UP")
	elif(agent.y-1>=0 and mapa[agent.x][agent.y-1]=='1'):
		y1-=1
		print("DOWN")
	else:
		X, Y = buscar(agent)
		## Primero se mueve para estar en la misma x que el objetivo y luego va a la y evitando obstaculos si se los encuentra
		if(X!=agent.x):
			if( X > agent.x):
				x1 +=1
				print("RIGHT")
			elif( X < agent.x):
				x1 -=1
				print("LEFT")
			if(not can_move(mapa,agent.x+x1,agent.y)):
				x1 = 0
				if(can_move(mapa,agent.x+x1,agent.y+1)):
					y1+=1
					print("UP")
				else:
					y1-=1
					print("DOWN")
		else:
			#print("Entro en lo de Y")
			if( Y > agent.y):
				print("UP")
				y1 +=1
			elif( Y < agent.y):
				y1 -=1
				print("DOWN")
			if(not can_move(mapa,agent.x,agent.y+y1)):
				y1 = 0
				if(can_move(mapa,agent.x+1,agent.y+y1)):
					x1+=1
					print("RIGHT")
				else:
					x1-=1
					print("LEFT")
	if(can_move(mapa,agent.x+x1,agent.y+y1)):
		agent.x=x1 + agent.x
		agent.y=y1 + agent.y
	
	return (0, agent.x, agent.y, energia_devolver)

##Funcion que percive lo que tiene a su alrededor y lo devuelve en el return, si está en el limite del mapa devuelve una X.
## Ademś actualizo el mapa interno del agente con lo que percive
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

## Le paso un array doble con posiciones y mete la nueva posicion x e y
def move(anteriores, anteriorx, anteriory):
	for i in range(4):
		anteriores[1][i] = anteriores[1][i+1]
		anteriores[0][i] = anteriores[0][i+1]
	anteriores[1][4]= anteriorx
	anteriores[0][4]= anteriory
	

def main():
	## Creo un array de 5x5 que usaré como mapa ( ya que no tengo sensores lo uso para comprobar el estado y la percepcion)
	rows, cols = (5, 5)
	Map = [[0 for i in range(cols)] for j in range(rows)]
	agent_map = [[8 for i in range(cols)] for j in range(rows)] #lo pongo todo a 8 porque no sé cual es el mapa, se irá cambiando cuando se descubra
	i = 0
	j = 4
	file = open(sys.argv[1], 'r')
	for line in file:

		for word in line.split():
			Map[i][j] = word
			i = i+1
		i = 0
		j = j-1
	## Creo la accion y un agente que tiene una posicion y un mapa, despues imprimo mi  estado actual  y creo un array doble lleno de 9 (caracter que no puede aparecer en el mapa) que uso para comprobar si estoy atascado.
	action = 0
	print(Map[2][0])
	agent = Agente(2,4,agent_map)
	posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, agent)
	print("Initial position: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='')
	anteriores = [[0,9,8,7,6],[9,8,7,6,0]]
	print("anteriores es x:", anteriores[1][4], " e y: " ,anteriores[0][4])
	energia = 0
	## Mido la energía, cada vez que me muevo le resto 1 y cada vez que limpio le sumo 100
	while( action != 1):## Siempre que la accion sea distinto de 1 (No operation) sigo ejecutando el bucle e imprimiendo es mapa del agente
		print("Energia: ", energia)
		posix,posiy,currPos,izda,arriba,dcha,abajo = percive(Map, agent)
		print("State: <",posix,",", posiy,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='', end = '')
		action, anteriorx,anteriory,energia = actuate(Map,agent, anteriores, energia)
		move(anteriores, anteriorx, anteriory)## Meto la nueva posicion en el array 
		for row in range(5):
			for val in range(5):
				print (agent.mapa[val][4-row],end = '')
			print(" ")
		


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  	main()

