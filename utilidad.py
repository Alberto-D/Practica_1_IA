#!/usr/bin/python3
import sys
from random import randrange

from time import sleep

import random
import copy
import collections
import numbers
import math

class Agente:
	def __init__(self,x_pos,y_pos, mapa_agente):
		self.x = x_pos
		self.y = y_pos
		self.mapa = mapa_agente



def can_move(mapa, x, y):
	max_x = len(mapa)
	max_y = len(mapa[0])
	if(x<0 or x>=max_x or y<0 or y>=max_y or mapa[x][y]=='X'):
		return False
	return True

def all_clear(agent):
	limpio = True
	for row in range(5):
		for val in range(5):
			if(agent.mapa[row][val]==8 or agent.mapa[row][val]=='1'):
				limpio = False
	return limpio


def buscar(agente):
	i = 0
	j = 4
	distancia = 10
	for line in range(5):
		for word in range(5):
			word = agente.mapa[i][j]
			if (word=='1' or word == 8):
				temporal = math.sqrt(abs(i-agente.x)+ abs(j-agente.y))  
				#print("La i vale ", i, " la X vale ",agente.x, "la diferencia es es ",abs(i-agente.x),"La j vale ", j, " la Y vale ",agente.y, "la diferencia es es ",abs(j-agente.y))
				print("LA diferencia es :",temporal)
				if( temporal < distancia):
					distancia = temporal
					print("Cambio distancia ahora es :",distancia)
					X = i
					Y = j
			i = i+1
		i = 0
		j = j-1
	return(X,Y)

def stuck(anteriores):
	if(anteriores[1][4]==anteriores[1][3]==anteriores[1][2] and anteriores[0][4]==anteriores[0][3]==anteriores[0][2]):
		return True
	return False
	
def actuate(mapa, agent, anteriores, energia):

	if(all_clear(agent)):
		print("Acabado")
		return(1, agent.x, agent.y, energia)

	x1=0
	y1=0
	energia_devolver = energia -1
	if (mapa[agent.x][agent.y]=='1'):
		mapa[agent.x][agent.y]=0
		print("suck")
		energia_devolver = energia +100
	elif(agent.x+1<=4 and agent.mapa[agent.x+1][agent.y]=='1'):
		x1+=1
	elif(agent.x-1>=0 and agent.mapa[agent.x-1][agent.y]=='1'):
		x1-=1
	elif(agent.y+1<=4 and agent.mapa[agent.x][agent.y+1]=='1'):
		y1+=1
	elif(agent.y-1>=0 and agent.mapa[agent.x][agent.y-1]=='1'):
		y1-=1
	
	else:
		X, Y = buscar(agent)
		#print("X e y son ",X,Y)
		if(X!=agent.x):
			#print("Entro en lo de X")
			if( X > agent.x):
				x1 +=1
			elif( X < agent.x):
				x1 -=1
			if(not can_move(mapa,agent.x+x1,agent.y)):
				x1 = 0
				if(can_move(mapa,agent.x+x1,agent.y+1)):
					y1+=1
				else:
					y1-=1
		else:
			#print("Entro en lo de Y")
			if( Y > agent.y):
				y1 +=1
			elif( Y < agent.y):
				y1 -=1
			if(not can_move(mapa,agent.x,agent.y+y1)):
				y1 = 0
				if(can_move(mapa,agent.x+1,agent.y+y1)):
					x1+=1
				else:
					x1-=1
	if(can_move(mapa,agent.x+x1,agent.y+y1)):
		agent.x=x1 + agent.x
		agent.y=y1 + agent.y
	
	return (0, agent.x, agent.y, energia_devolver)

def percive(mapa, agent):
	x = agent.x
	y = agent.y
	currPos = mapa[x][y]
	agent.mapa[x][y] = mapa[x][y]
	if((x-1)<0):
		izda = "M"
	else:
		izda = mapa[x-1][y]
		agent.mapa[x-1][y] = mapa[x-1][y]
	if((x+1)>4):
		dcha = "M"
	else:
		dcha = mapa[x+1][y]
		agent.mapa[x+1][y] = mapa[x+1][y]
	if((y-1)<0):
		abajo = "M"
	else:
		abajo = mapa[x][y-1]
		agent.mapa[x][y-1] = mapa[x][y-1]
	if((y+1)>4):
		arriba = "M"
	else:
		arriba = mapa[x][y+1]
		agent.mapa[x][y+1] = mapa[x][y+1]
	print(agent.x,",", agent.y,">  Perception : <",currPos,",",izda,",",arriba,",",dcha,",",abajo,">","Action: ", sep='', end = '')


def move(anteriores, anteriorx, anteriory):
	for i in range(4):
		anteriores[1][i] = anteriores[1][i+1]
		anteriores[0][i] = anteriores[0][i+1]
	anteriores[1][4]= anteriorx
	anteriores[0][4]= anteriory
	

def main():
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

	action = 0
	print(Map[2][0])
	agent = Agente(2,4,agent_map)
	print("Initial agenttion: <",sep='',end = '')
	percive(Map, agent)
	anteriores = [[0,9,8,7,6],[9,8,7,6,0]]
	print("anteriores es x:", anteriores[1][4], " e y: " ,anteriores[0][4])
	energia = 0
	while( action != 1):
		print("Energia: ", energia)
		print("State: <",sep='',end = '')
		percive(Map, agent)
		action, anteriorx,anteriory,energia = actuate(Map,agent, anteriores, energia)
		move(anteriores, anteriorx, anteriory)
		for row in range(5):
			for val in range(5):
				print (agent.mapa[val][4-row],end = '')
			print(" ")
		sleep(0.5)
	print()






# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  	main()

