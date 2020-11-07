#!/usr/bin/python3
import sys
from random import randrange

from time import sleep

import random
import copy
import collections
import numbers


class Position:
	def __init__(self,x_pos,y_pos):
		self.x = x_pos
		self.y = y_pos

def can_move(mapa, x, y):
	max_x = len(mapa)
	max_y = len(mapa[0])
	if(x<0 or x>=max_x or y<0 or y>=max_y or mapa[x][y]=='X'):
		return False
	return True


def actuate(mapa, posi, to_clean):
	x1=0
	y1=0
	if (mapa[posi.x][posi.y]=='1'):
			mapa[posi.x][posi.y]=0
			to_clean-=1
			print("suck")
	else:
		if((posi.x==0 and posi.y==4) or (posi.x==1 and (posi.y==3 or posi.y==4))):
			print("Esquina 1")
			x1+=1
		elif((posi.x==4 and (posi.y==4 or posi.y==3)) or (posi.x==3 and posi.y==3)):
			y1-=1
			print("Esquina 2")
		elif(((posi.x==4 or posi.x==3) and posi.y==0) or (posi.x==3 and posi.y==1)):
			x1-=1
			print("Esquina 3")
		elif((posi.x==1 and (posi.y==0 or posi.y==1)) or (posi.x==1 and posi.y==1)):
			y1+=1
			print("Esquina 4")

		elif(posi.x==0 or posi.x==1 ):
			y1+=1
			print( "^")
		elif(posi.y==4 or posi.y==3):
			x1+=1
			print(">")
		elif(posi.x==4 or posi.x==3):
			y1-=1
			print("v")
		elif(posi.y==0 or posi.y==1):
			x1-=1
			print("<")
		
		if not (can_move(mapa,posi.x+x1,posi.y+y1)):
			print("NO PUEDORL")
			x1=0
			y1=0

			action = randrange(4)
			if(action==0): #Arriba
				print( "^")
				y1+=1
				x1+=1
			elif(action==1):#Abajo
				print("v")
				x1+=1
				y1-=1
			elif(action==2):#Derecha
				print(">")
				x1-=1
				y1+=1
			elif(action==3):#Izquierda
				print("<")
				x1-=1
				y1-=1

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
	posi = Position(0,0)
	print("Initial position: <",sep='',end = '')
	percive(Map, posi)
	while( to_clean >0):
		print("To clean: ", to_clean)
		print("State: <",sep='',end = '')
		percive(Map, posi)
		to_clean = actuate(Map,posi, to_clean)
		sleep(0.5)

	print()

	


	

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  	main()

