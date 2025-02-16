#credit to Leet Unova (https://github.com/LeetUnova/Pygame-3D-Graphics?source=post_page-----c36ec2e03a33---------------------------------------) for the main code (all i did was add some of the movement parts)

import pygame
from math import sin, cos, pi, sqrt

class Object3d:
    def __init__(self,
                    vertices: list[list[float]],
                    edges: list[list[int]],
                    faces: list[list[int]],
                    position: list[float]) -> None:
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.position = position
    def draw(self, surface: pygame.Surface) -> None:
        halfWidth = surface.get_width() / 2
        halfHeight = surface.get_height() / 2
        verts = [
            [
                o[u] * 50 + self.position[u] for u in range(3)
            ] for o in self.vertices]
        
        for face in self.faces:
            points = []
            for vertex in face:
                pointDiv = verts[vertex][2] / 400
                if pointDiv == 0:
                    break
                point = [
                    verts[vertex][0] / pointDiv + halfWidth,
                    verts[vertex][1] / pointDiv + halfHeight
                ]
                points.append(point)
            if len(points) == len(face):
                pygame.draw.polygon(surface, (255, 255, 255), points)

        for edge in self.edges:
            point1Div = verts[edge[0]][2] / 400
            if point1Div == 0:
                continue
            point2Div = verts[edge[1]][2] / 400
            if point2Div == 0:
                continue
            point1 = [
                verts[edge[0]][0] / point1Div + halfWidth,
                verts[edge[0]][1] / point1Div + halfHeight
            ]
            point2 = [
                verts[edge[1]][0] / point2Div + halfWidth,
                verts[edge[1]][1] / point2Div + halfHeight
            ]
            pygame.draw.line(surface, (0, 0, 0), point1, point2)

class Car(Object3d):
    vertices: list[list[float]] = [
        [-1, 1.5, -1],
        [-1, -1, -1],
        [15, 1.5, -1],
        [15, -1, -1],
        [3, -1, -1],
        [4, -3, -1],
        [13, -1, -1],
        [11, -3, -1],
        [-1, 1.5, 5],
        [-1, -1, 5],
        [15, 1.5, 5],
        [15, -1, 5],
        [3, -1, 5],
        [4, -3, 5],
        [13, -1, 5],
        [11, -3, 5],
    ]
    edges: list[list[int]] = [
        [0, 1],
        [0, 2],
        [2, 3],
        [1, 4],
        [4, 5],
        [3, 6],
        [6, 7],
        [5, 7],
        [8, 9],
        [8, 10],
        [10, 11],
        [9, 12],
        [12, 13],
        [11, 14],
        [14, 15],
        [13, 15],
        [0, 8],
        [1, 9],
        [2, 10],
        [3, 11],
        [4, 12],
        [5, 13],
        [6, 14],
        [7, 15]
    ]
    faces: list[list[int]] = [
        [0, 1, 4, 5, 7, 6, 3, 2],
        [8, 9, 12, 13, 15, 14, 11, 10],
        [0, 1, 9, 8],
        [2, 3, 11, 10],
        [4, 5, 13, 12],
        [6, 7, 15, 14],
        [0, 2, 10, 8],
        [1, 4, 12, 9],
        [3, 6, 14, 11]
    ]
    def __init__(self, position: list[float]) -> None:
        super().__init__(Car.vertices, Car.edges, Car.faces, position)

window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("3d Graphics")
done = False

car = Car([0, 0, 150])

ticks = 0
temp_pos = 0
draging = False
offset_x = 0
offset_y = 0
temp_pos_y = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                    draging = True
                    offset_x, offset_y = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                draging = False

        if event.type == pygame.MOUSEMOTION:
            if draging:
                mouse_x, mouse_y = event.pos
                blank = mouse_x - offset_x
                temp_pos_y = mouse_y - offset_y


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        car.position[2] -= 1
    if keys[pygame.K_s]:
        car.position[2] += 1
    if keys[pygame.K_a]:
        temp_pos += 1
    if keys[pygame.K_d]:
        temp_pos -= 1 
    pygame.draw.rect(window, (135, 206, 235), (0, 0, 1280, 720))
    car.position[0] =  temp_pos
    car.position[1] =  temp_pos_y
    car.draw(window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    

    pygame.display.update()
    print(temp_pos_y, car.position[1])
    ticks += 1

exit()