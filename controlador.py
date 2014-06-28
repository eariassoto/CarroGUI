import pygame
import os
import serial
from pygame.locals import *

class Main:
	def __init__(self):
		pygame.init()
		FPSCLOCK = pygame.time.Clock()		
		
		grafico = Grafico()
		comunicacion = Comunicacion()
		carro = Carro(comunicacion)
		
		mousex, mousey = 0, 0
		
		while(True):
			for evento in pygame.event.get():
				if evento.type == QUIT or (evento.type == KEYUP and evento.key == K_ESCAPE):
					pygame.quit()
					os._exit(0)
				elif evento.type == MOUSEMOTION:
					mousex, mousey = evento.pos 
				elif evento.type == MOUSEBUTTONDOWN:
					rectClic = grafico.collide(mousex, mousey)
					if rectClic:
						carro.enviarComando(grafico.getIndex(rectClic))
				elif evento.type == MOUSEBUTTONUP:
						carro.enviarComando(4)
			
			grafico.dibujar()
			pygame.display.update()	
			FPSCLOCK.tick(114)

		
		
			
################################################ Grafico ##################################################
#                                 Maneja la parte grafica del programa                                    # 
###########################################################################################################
class Grafico:
	flechaArr = None
	flechaDer = None
	flechaAba = None
	flechaIzq = None
	stop = None
	rect0 = None
	rect1 = None
	rect2 = None
	rect3 = None
	rect4 = None
	
	sprite = [flechaArr, flechaDer, flechaAba, flechaIzq, stop]
	rect = [rect0, rect1, rect2, rect3, rect4]
	
	pantalla = None
	
	
	def __init__(self):
		self.pantalla = pygame.display.set_mode((600, 300))
		pygame.display.set_caption("Carrito")
		
		for i in range(len(self.sprite)):
			self.sprite[i] = pygame.image.load(config["PATHS"][i]).convert()
			self.sprite[i] = pygame.transform.scale(self.sprite[i], (100, 100))
			
		self.rect[0] = Rect(100,   0, 100, 100)
		self.rect[1] = Rect(200, 100, 100, 100)
		self.rect[2] = Rect(100, 200, 100, 100)
		self.rect[3] = Rect(  0, 100, 100, 100)
		self.rect[4] = Rect(100, 100, 100, 100)

			
	def dibujar(self):
		self.pantalla.fill((255,255,255))
		pygame.draw.rect (self.pantalla, (0,0,0), self.rect[0])
		self.pantalla.blit(self.sprite[0], (100,   0))
		self.pantalla.blit(self.sprite[1], (200, 100))
		self.pantalla.blit(self.sprite[2], (100, 200))
		self.pantalla.blit(self.sprite[3], (  0, 100))
		self.pantalla.blit(self.sprite[4], (100, 100))
		pygame.display.flip()

	
	def collide(self, x, y):
		for i in range(len(self.rect)):
			if self.rect[i].collidepoint(x,y):
				return self.rect[i]
				
	
	def getIndex(self, rect):
		return self.rect.index(rect)


		
################################################ Carro ##################################################
#                                 Maneja la parte grafica del programa                                    # 
###########################################################################################################
class Carro:
	comunicacion = None
	def __init__(self, com):
		self.comunicacion = com
		
	def enviarComando(self, n):
		self.comunicacion.enviar(config["COMANDO"][n])



		
################################################ Comunicacion ##################################################
#                                 Maneja la parte grafica del programa                                    # 
###########################################################################################################
class Comunicacion:
	ser = None
	def __init__(self):
		self.ser = serial.Serial(config["PUERTO"], config["CANAL"]);
	
	def enviar(self, char):
		self.ser.write(char);
		
		
if __name__ == '__main__':
	config = {}
	execfile("settings.config", config) 
	main = Main()