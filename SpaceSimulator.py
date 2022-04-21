import pygame
import math
pygame.init() #inicia o módulo do pygame

WIDTH, HEIGHT = 800,800 #constante do tamanho da janela
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #cria a janela com os tamanhos das variáveis
pygame.display.set_caption("Space Simulation") #nome da janela

WHITE=(255,255,255)
YELLOW = (255,255,0) #VALOR RGB PARA AMARELO
BLUE = (100,149,237)
RED = (188,39,50)
DARK_GREY=(80,78,81)

FONT = pygame.font.SysFont("comicsans",16)

class Planet:
    AU = 149.6e6 * 1000 #unidades astronomicas - distancia aproximada da terra e do sol
    #está multiplicado por 1000 para transformar em KM para M
    G = 6.67428e-11 #gravidade e sua força de atração entre os objetos
    SCALE = 200/AU #escala para facilitar a visualização -> uma unidade astronomica será equivalente
                    #a 100 pixels no programa
    TIMESTEP = 3600*24 #quanto tempo será simulado - Um dia (3600 segundos * 24 = 24hrs)

    def __init__(self, x, y, radius, color, mass): #variáveis que serão necessárias para os planetas
        self.x=x #distancia do sol em metros
        self.y=y #distancia do sol em metros
        self.radius=radius
        self.color=color
        self.mass=mass

        self.orbit=[]
        self.sun=False #o sol será completamente diferente dos planetas, e não terá órbita
        #portanto o que for descrito aqui não deve ser aplicado a ele
        self.distance_to_sun=0

        self.x_vel=0 #velocidade no eixo X
        self.y_vel=0 #velocidade no eixo Y
        #para ser capaz de mover o objeto em várias direções, deve-se ter velocidade vindo de várias
        #direções (X e Y)

    def draw(self,win):
        x = self.x*self.SCALE + WIDTH/2 #localização em metros aplicado à escalae desenhado no meio
        y = self.y*self.SCALE + HEIGHT/2

        if len(self.orbit)>2:
            updated_points=[]
            for point in self.orbit:
                x,y=point
                x = x*self.SCALE + WIDTH/2
                y=y*self.SCALE+HEIGHT/2
                updated_points.append((x,y))

            pygame.draw.lines(win,self.color,False,updated_points,2) #desenha linhas entre os pontos

        pygame.draw.circle(win,self.color,(x,y), self.radius) #quando a função draw for chamada, um circulo será desenhado

        if not self.sun:
            distance_text=FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1,WHITE) #objeto de texto
            win.blit(distance_text,(x-distance_text.get_width()/2,y-distance_text.get_width()/2)) #para que o texto apareça diretamente
                                                                                                #no centro dos planetas

    def attraction(self,other):
        other_x, other_y=other.x,other.y
        distance_x=other_x-self.x
        distance_y = other_y-self.y
        distance=math.sqrt(distance_x**2+distance_y**2) #calcula a distância entre os objetos

        if other.sun: #se o outro objeto for o sol
            self.distance_to_sun=distance #a distancia será guardada em uma variável própria

        force=self.G*self.mass*other.mass/distance**2 #força de atração entre os objetos
        theta=math.atan2(distance_y,distance_x) #para descobrir o ângulo do triângulo distancia - lado x - lado y
        force_x=math.cos(theta)*force #força sobre o lado x
        force_y=math.sin(theta)*force #força sobre o lado y
        return force_x,force_y

    def update_position(self,planets):
        total_fx=total_fy=0
        for planet in planets:
            if self==planet:
                continue #pois a distancia entre um planeta e ele mesmo é 0

            fx,fy=self.attraction(planet)
            total_fx+=fx
            total_fy+=fy

        self.x_vel+=total_fx/self.mass*self.TIMESTEP #velocidade está aumentando de acordo com a aceleração * TIMESTEP (um dia)
        #aceleração = força / massa (força = massa / aceleração)
        self.y_vel+=total_fy/self.mass*self.TIMESTEP

        self.x+= self.x_vel *self.TIMESTEP
        self.y+= self.y_vel*self.TIMESTEP
        self.orbit.append((self.x,self.y))


def main():
    run = True
    clock = pygame.time.Clock() #impede o framerate de ultrapassar determinado valor
    #sem a função Clock, o programa rodaria na velocidade suportada pelo PC
    #framerates altos em pcs potentes, e baixos em pcs pouco potentes
    #isso faria com que o programa rodasse diferentemente dependendo da máquina

    sun=Planet(0,0,30,YELLOW, 1.98892*10**30) #variáveis necessárias da função init
    sun.sun=True #iniciar o sun que foi cancelado na função Planet

    earth = Planet(-1*Planet.AU, 0, 16, BLUE,5.9742*10**24) #O x equivale à distância do sol (está a 1 AU do sol)
                                                            #multiplicado por -1 para ir para a esquerda do eixo X
    earth.y_vel=29.783*1000 #km/s convertido para m/s (por isso multiplicado por 1000)

    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_vel=24.077*1000 #se a posição é negativa, a velocidade precisa ser positiva para que o planeta gire em sentido horário
                            #se a posição por positiva, a velocidade deve ser negativa

    mercury = Planet(-0.387*Planet.AU,0,8,DARK_GREY,3.30*10**23)
    mercury.y_vel=47.4*1000

    venus=Planet(-0.723*Planet.AU, 0,14,WHITE,4.8685*10**24)
    venus.y_vel=35.02*1000

    planets=[sun, earth, mars,mercury,venus]

    while run:
        clock.tick(60) #60fps será o máximo que o programa poderá rodar
        '''WIN.fill(WHITE)
        pygame.display.update() #atualiza a tela - em todo loop irá atualizar a tela e aplicará a cor
                                #branca no fundo'''
        WIN.fill((0,0,0)) #toda vez que a tela for "update", o preto irá apagar a posição antiga dos planetas, mostrando apenas
                            #a posição atual, dando a impressão de que eles estão se movendo

        for event in pygame.event.get():
            if event.type==pygame.QUIT: #evento de sair da janela (apertar o botão X da janela)
                run=False #causa o término do programa
            #com esse loop, a janela não mais fecha automaticamente. Ela roda até que o X seja apertado

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN) #será desenhado na tela

        pygame.display.update()

    pygame.quit()

main()