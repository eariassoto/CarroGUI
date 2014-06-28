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
		
		while(True):
			for evento in pygame.event.get():
				if evento.type == QUIT or (evento.type == KEYUP and evento.key == K_ESCAPE):
					pygame.quit()
					os._exit(0)
				elif evento.type == MOUSEBUTTONDOWN:
					print "mouse abajo"
				elif evento.type == MOUSEBUTTONUP:
					print "mouse arriba"
			
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
	flecha = [flechaArr, flechaDer, flechaAba, flechaIzq]
	pantalla = None
	
	def __init__(self):
		self.pantalla = pygame.display.set_mode((600, 300))
		pygame.display.set_caption("Carrito")
		
		for i in range(len(self.flecha)):
			self.flecha[i] = pygame.image.load(config["PATHS"][i]).convert()
			self.flecha[i] = pygame.transform.scale(self.flecha[i], (100, 100))

			
	
	def dibujar(self):
		self.pantalla.fill((255,255,255))
		self.pantalla.blit(self.flecha[0], (100, 0))
		self.pantalla.blit(self.flecha[1], (200, 100))
		self.pantalla.blit(self.flecha[2], (100, 200))
		self.pantalla.blit(self.flecha[3], (0, 100))
		pygame.display.flip()



		
################################################ Carro ##################################################
#                                 Maneja la parte grafica del programa                                    # 
###########################################################################################################
class Carro:
	comunicacion = None
	def __init__(self, com):
		self.comunicacion = com



		
################################################ Comunicacion ##################################################
#                                 Maneja la parte grafica del programa                                    # 
###########################################################################################################
class Comunicacion:
	ser = None
	def __init__(self):
		ser = serial.Serial(config["PUERTO"], config["CANAL"]);
	
		
		
if __name__ == '__main__':
	config = {}
	execfile("settings.config", config) 
	main = Main()