import pygame
import os
import serial
import inputbox
from pygame.locals import *

class Main:
	def __init__(self, puerto, baud):
		pygame.init()
		FPSCLOCK = pygame.time.Clock()		
		
		grafico = Grafico(puerto, baud)
		comunicacion = Comunicacion(puerto, baud)
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
						c = grafico.getIndex(rectClic)
						carro.enviarComando(c);
						if c == 4 or c == 5:
							carro.enviarComando(6);
				elif evento.type == MOUSEBUTTONUP:
						carro.enviarComando(6)
				elif evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_LEFT:
						carro.enviarComando(3);
					elif evento.key == pygame.K_RIGHT:
						carro.enviarComando(1);
					elif evento.key == pygame.K_DOWN:
						carro.enviarComando(2);
					elif evento.key == pygame.K_UP:
						carro.enviarComando(0);
				elif evento.type == pygame.KEYUP:
					carro.enviarComando(6);
			
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
	masVelocidad = None
	menosVelocidad = None
	rect0 = None
	rect1 = None
	rect2 = None
	rect3 = None
	rect4 = None
	rect5 = None
	
	puerto = None
	tbaud = None
	puertorect = None
	tbaudrect = None
	
	sprite = [flechaArr, flechaDer, flechaAba, flechaIzq, masVelocidad, menosVelocidad]
	rect = [rect0, rect1, rect2, rect3, rect4, rect5]
	
	pantalla = None
	
	
	def __init__(self, puerto, baud):
		self.pantalla = pygame.display.set_mode((450, 300))
		pygame.display.set_caption("Carrito")
		
		for i in range(len(self.sprite)):
			self.sprite[i] = pygame.image.load(config["PATHS"][i]).convert()
			self.sprite[i] = pygame.transform.scale(self.sprite[i], (100, 100))
			
		self.rect[0] = Rect(100,   0, 100, 100)
		self.rect[1] = Rect(200, 100, 100, 100)
		self.rect[2] = Rect(100, 100, 100, 100)
		self.rect[3] = Rect(  0, 100, 100, 100)
		self.rect[4] = Rect(325,   0, 100, 100)
		self.rect[5] = Rect(325, 100, 100, 100)
		
		basicfont = pygame.font.SysFont(None, 48)
		self.puerto = basicfont.render('Puerto: ' + puerto, True, (0, 0, 0), (255, 255, 255))
		self.tbaud = basicfont.render('Tasa de bauds: ' + str(baud), True, (0, 0, 0), (255, 255, 255))
		self.puertorect = self.puerto.get_rect()
		self.tbaudrect = self.tbaud.get_rect()
		self.puertorect.x = 0
		self.puertorect.y = 200
		self.tbaudrect.x = 0
		self.tbaudrect.y = 250
			
	def dibujar(self):
		self.pantalla.fill((255,255,255))
		self.pantalla.blit(self.sprite[0], (100,   0))
		self.pantalla.blit(self.sprite[1], (200, 100))
		self.pantalla.blit(self.sprite[2], (100, 100))
		self.pantalla.blit(self.sprite[3], (  0, 100))
		self.pantalla.blit(self.sprite[4], (325,   0))
		self.pantalla.blit(self.sprite[5], (325, 100))
		self.pantalla.blit(self.puerto, self.puertorect)
		self.pantalla.blit(self.tbaud, self.tbaudrect)
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
	def __init__(self, puerto, baud):
		self.ser = serial.Serial(puerto, baud);
	
	def enviar(self, char):
		self.ser.write(char);
		
		
if __name__ == '__main__':
	config = {}
	execfile("settings.config", config)
	ventanaInput = pygame.display.set_mode((320,240))
	puerto = inputbox.ask(ventanaInput, "Puerto del Carro")
	baud = 9600#inputbox.ask(ventanaInput, "Tasa de baudios")
	main = Main(puerto, baud)