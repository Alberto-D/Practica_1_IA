#!/usr/bin/python3
import sys
from random import randrange

from time import sleep

import random
import copy
import collections
import numbers


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
			if(agent.mapa[row][val]==8):
				limpio = False
	return limpio

def stuck(anteriores):
	if(anteriores[1][4]==anteriores[1][3]==anteriores[1][2] and anteriores[0][4]==anteriores[0][3]==anteriores[0][2]):
		return True
	return False
	
def in_line(agent):

	for i in range(4):
		devolverx = 0
		devolvery = 0
		if(agent.mapa[agent.x][i]==8):
			if(i> agent.y):
				devolvery = -1
			else:
				devolvery = 1
		if(agent.mapa[i][agent.y]==8):
			if(i> agent.x):
				devolverx = -1
			else:
				devolverx = 1

def actuate(mapa, agent, anteriores):
	x1=0
	y1=0
	if (mapa[agent.x][agent.y]=='1'):
		mapa[agent.x][agent.y]=0
		print("suck")
	elif(agent.x+1<=4 and agent.mapa[agent.x+1][agent.y]=='1'):
		x1+=1
	elif(agent.x-1>=0 and agent.mapa[agent.x-1][agent.y]=='1'):
		x1-=1
	elif(agent.y+1<=4 and agent.mapa[agent.x][agent.y+1]=='1'):
		y1+=1
	elif(agent.y-1>=0 and agent.mapa[agent.x][agent.y-1]=='1'):
		y1-=1
	else:
		if(((agent.x+1 < 4) and (agent.mapa[agent.x+2][agent.y]==8)) and (agent.mapa[agent.x+1][agent.y]!='X')):
			x1+=1
		elif(((agent.y+1 < 4) and (agent.mapa[agent.x][agent.y+2]==8)) and (agent.mapa[agent.x][agent.y+1]!='X')):
			y1+=1
		elif(((agent.x-1 >= 0) and (agent.mapa[agent.x-2][agent.y]==8)) and (agent.mapa[agent.x-1][agent.y]!='X')):
			x1-=1
		elif(((agent.y-1 >= 0) and (agent.mapa[agent.x][agent.y-2]==8)) and (agent.mapa[agent.x][agent.y-1]!='X')):
			y1-=1

	if (stuck(anteriores)):
		action = randrange(4)
		if(action == 0): #Arriba
			print( "aleatorio^")
			y1+=1
		elif(action == 1):#Abajo
			print("aleatoriov")
			y1-=1
		elif(action == 2):#Derecha
			print("aleatorio>")
			x1+=1
		elif(action == 3):#Izquierda
			print("aleatorio<")
			x1-=1
			

	if(can_move(mapa,agent.x+x1,agent.y+y1)):
		print(" puedo",x1, y1 )
		agent.x=x1 + agent.x
		agent.y=y1 + agent.y

	if(all_clear(agent)):
		print("Acabado")
		return(1, agent.x, agent.y)

	
	
		
	return (0, agent.x, agent.y)



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

	action = 0
	print(Map[2][0])
	agent = Agente(0,0,agent_map)
	print("Initial agenttion: <",sep='',end = '')
	percive(Map, agent)
	anteriores = [[0,9,8,7,6],[9,8,7,6,0]]
	print("anteriores es x:", anteriores[1][4], " e y: " ,anteriores[0][4])
	while( action != 1):
		print("To clean: ", to_clean)
		print("State: <",sep='',end = '')
		percive(Map, agent)
		action, anteriorx,anteriory = actuate(Map,agent, anteriores)
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

