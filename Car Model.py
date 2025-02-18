#credit to Leet Unova (https://github.com/LeetUnova/Pygame-3D-Graphics?source=post_page-----c36ec2e03a33---------------------------------------) for the main code (all i did was add some of the movement parts)
import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    install("pygame_menu")
except:
    pass
try:
    install("pygame")
except:
    pass

import pygame
import pygame_menu
from math import sin, cos, pi, sqrt, radians

def show_controls():
    controls = [
        "W: Move forward",
        "S: Move backward",
        "A: Move left",
        "D: Move right",
        "Q: Rotate left",
        "E: Rotate right",
        "Z: Rotate x-axis",
        "X: Rotate x-axis (opposite)",
        "C: Rotate z-axis",
        "V: Rotate z-axis (opposite)",
        "R: Move up",
        "F: Move down",
        "ESC: Reset position and rotation"
    ]
    return "\n".join(controls)

def rotate(point, vertice, centre, angle, axis):
    cntx = centre[0]
    cnty = centre[1]
    cntz = centre[2]
    theta = angle
    ptz = vertice[2] - cntz
    pty = vertice[1] - cnty
    ptx = vertice[0] - cntx

    p2z = ptz * cos(radians(theta[0])) - ptx * sin(radians(theta[0]))
    p2x = ptx * cos(radians(theta[0])) + ptz * sin(radians(theta[0]))

    ptz = p2z

    p2z = ptz * cos(radians(theta[1])) + pty * sin(radians(theta[1]))
    p2y = pty * cos(radians(theta[1])) - ptz * sin(radians(theta[1]))

    ptx = p2x
    pty = p2y

    p2x = ptx* cos(radians(theta[2])) - pty * sin(radians(theta[2]))
    p2y = pty * cos(radians(theta[2])) + ptx * sin(radians(theta[2]))
    
    

    p2x += cntx
    p2y += cnty
    p2z += cntz

    if axis == 0:
        point = p2x

    elif axis == 1:
        point = p2y

    elif axis == 2:
        point = p2z
        

    return point

class Object3d:
    def __init__(self,
                    vertices: list[list[float]],
                    edges: list[list[int]],
                    faces: list[list[int]],
                    position: list[float],
                    rotation: list[float],
                    textures: list[str]) -> None:
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.position = position
        self.rotation = rotation
        self.textures = [pygame.image.load(texture) for texture in textures]  # Load textures for each face
        self.default_texture = pygame.Surface((1, 1))  # Default texture for faces not found
        self.default_texture.fill((255, 255, 255))  # Fill default texture with white color

        # Calculate the midpoint
        self.midpoint = [
            sum(vertex[i] for vertex in self.vertices) / len(self.vertices) for i in range(3)
        ]

    def draw(self, surface: pygame.Surface) -> None:
        halfWidth = surface.get_width() / 2
        halfHeight = surface.get_height() / 2
        verts = [
            [
                rotate(o[u], o, self.midpoint, self.rotation, u) * 50 + self.position[u] for u in range(3)
            ] for o in self.vertices]
        
        # Calculate the average depth of each face
        face_depths = []
        for face in self.faces:
            avg_depth = sum(verts[vertex][2] for vertex in face) / len(face)
            face_depths.append((avg_depth, face))
        
        # Sort faces by depth (farthest to nearest)
        face_depths.sort(reverse=True, key=lambda x: x[0])
        
        for _, face in face_depths:
            points = []
            for vertex in face:
                pointDiv = verts[vertex][2] / 400
                if pointDiv <= 0:
                    pointDiv = 1/400
                point = [
                    verts[vertex][0] / pointDiv + halfWidth,
                    verts[vertex][1] / pointDiv + halfHeight
                ]
                points.append(point)
            if len(points) == len(face):
                
                # Calculate texture coordinates
                min_x = min(p[0] for p in points)
                min_y = min(p[1] for p in points)
                texture_coords = [(p[0] - min_x, p[1] - min_y) for p in points]
                texture_width = max(p[0] for p in points) - min_x
                texture_height = max(p[1] for p in points) - min_y
                
                # Get the texture for the face or use the default texture
                try:
                    texture_surface = pygame.transform.scale(self.textures[self.faces.index(face)], (int(texture_width), int(texture_height)))
                except:
                    texture_surface = pygame.transform.scale(self.default_texture, (int(texture_width), int(texture_height)))
                
                # Create a mask surface
                mask_surface = pygame.Surface((int(texture_width), int(texture_height)), pygame.SRCALPHA)
                pygame.draw.polygon(mask_surface, (255, 255, 255, 255), texture_coords)
                # Blit the texture onto the mask surface
                texture_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                # Blit the masked texture onto the main surface
                surface.blit(texture_surface, (min_x, min_y))

        for edge in self.edges:
            point1Div = verts[edge[0]][2] / 400
            if point1Div <= 0:
                point1Div = 1/400
            point2Div = verts[edge[1]][2] / 400
            if point2Div <= 0:
                point2Div = 1/400
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
        [-1, 1.5, 0],
        [-1, -1, 0],
        [15, 1.5, 0],
        [15, -1, 0],
        [3, -1, 0],
        [4, -3, 0],
        [13, -1, 0],
        [11, -3, 0],
        [-1, 1.5, 6],
        [-1, -1, 6],
        [15, 1.5, 6],
        [15, -1, 6],
        [3, -1, 6],
        [4, -3, 6],
        [13, -1, 6],
        [11, -3, 6],
        [7, -1.25, 3],
        # Wheel vertices (cylinders)
        [2, 1.5, 0], [2, 3.5, 0], [4, 1.5, 0], [4, 3.5, 0],  # Front left wheel
        [13, 1.5, 0], [13, 3.5, 0], [11, 1.5, 0], [11, 3.5, 0],  # Front right wheel
        [2, 1.5, 6], [2, 3.5, 6], [4, 1.5, 6], [4, 3.5, 6],  # Rear left wheel
        [13, 1.5, 6], [13, 3.5, 6], [11, 1.5, 6], [11, 3.5, 6],  # Rear right wheel
        [2, 1.5, 0.5], [2, 3.5, 0.5], [4, 1.5, 0.5], [4, 3.5, 0.5],  # Front left wheel
        [13, 1.5, 0.5], [13, 3.5, 0.5], [11, 1.5, 0.5], [11, 3.5, 0.5],  # Front right wheel
        [2, 1.5, 5.5], [2, 3.5, 5.5], [4, 1.5, 5.5], [4, 3.5, 5.5],  # Rear left wheel
        [13, 1.5, 5.5], [13, 3.5, 5.5], [11, 1.5, 5.5], [11, 3.5, 5.5]  # Rear right wheel
    ]
    edges: list[list[int]] = [
        [0, 1],
        [0, 2],
        [2, 3],
        [1, 4],
        [4, 5],
        [4, 6],
        [12, 14],
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
        [7, 15],
        # Wheel edges (cylinders)
        [17, 18], [18, 20], [20, 19], [19, 17],  # Front left wheel
        [21, 22], [22, 24], [24, 23], [23, 21],  # Front right wheel
        [25, 26], [26, 28], [28, 27], [27, 25],  # Rear left wheel
        [29, 30], [30, 32], [32, 31], [31, 29],  # Rear right wheel
        # Additional edges for wheel cylinders
        [33, 34], [34, 36], [36, 35], [33, 35], [33, 17], [34, 18], [35, 19], [36, 20],  # Front left wheel
        [37, 38], [38, 40], [40, 39], [39, 37], [37, 21], [38, 22], [39, 23], [40, 24],  # Front right wheel
        [41, 42], [42, 44], [44, 43], [43, 41], [41, 25], [42, 26], [43, 27], [44, 28],  # Rear left wheel
        [45, 46], [46, 48], [48, 47], [47, 45], [45, 29], [46, 30], [47, 31], [48, 32]   # Rear right wheel
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
        [3, 6, 14, 11],
        # Wheel faces (cylinders)
        [17, 18, 20, 19],  # Front left wheel
        [21, 22, 24, 23],  # Front right wheel
        [25, 26, 28, 27],  # Rear left wheel
        [29, 30, 32, 31],  # Rear right wheel
        [33, 34, 36, 35],  # Front left wheel
        [37, 38, 40, 39],  # Front right wheel
        [41, 42, 44, 43],  # Rear left wheel
        [45, 46, 48, 47],  # Rear right wheel
        # Additional faces for wheel cylinders
        [17, 33, 34, 18], [19, 35, 36, 20], [17, 35, 33, 19], [18, 34, 36, 20],  # Front left wheel
        [21, 37, 38, 22], [23, 39, 40, 24], [21, 37, 39, 23], [22, 38, 40, 24],  # Front right wheel
        [25, 41, 42, 26], [27, 43, 44, 28], [25, 41, 43, 27], [26, 42, 44, 28],  # Rear left wheel
        [29, 45, 46, 30], [31, 47, 48, 32], [29, 45, 47, 31], [30, 46, 48, 32]  # Rear right wheel
    ]
    textures: list[str] = [
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',
        'ahndureh.png',  # Front left wheel
        'ahndureh.png',  # Front right wheel
        'ahndureh.png',  # Rear left wheel
        'ahndureh.png'  # Rear right wheel
    ]
    def __init__(self, position: list[float], rotation: list[float]) -> None:
        super().__init__(Car.vertices, Car.edges, Car.faces, position, rotation, Car.textures)

def main():
    pygame.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("3D Graphics")

    menu = pygame_menu.Menu('Controls', 400, 300, theme=pygame_menu.themes.THEME_DARK, position=(0, 0))
    menu.add.label(show_controls(), max_char=-1, font_size=20, font_color=(255, 255, 255), align=pygame_menu.locals.ALIGN_LEFT)
    menu.add.button('Close (TAB)', pygame_menu.events.BACK)

    car = Car([0, 0, 500], [0, 0, 0])

    ticks = 0
    temp_pos = 0
    draging = False
    offset_x = 0
    offset_y = 0
    temp_pos_y = 0
    blank = 0
    rotx = 0
    rotz = 0

    show_menu = False

    font = pygame.font.SysFont(None, 24)

    done = False
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    show_menu = not show_menu

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            car.position[2] -= 1
        if keys[pygame.K_s]:
            car.position[2] += 1
        if keys[pygame.K_a]:
            temp_pos += 1
        if keys[pygame.K_d]:
            temp_pos -= 1 
        if keys[pygame.K_q]:
            blank += .5
        if keys[pygame.K_e]:
            blank -= .5
        if keys[pygame.K_r]:
            temp_pos_y += 1
        if keys[pygame.K_f]:
            temp_pos_y -= 1
        if keys[pygame.K_z]:
            rotx += .5
        if keys[pygame.K_x]:
            rotx -= .5
        if keys[pygame.K_c]:
            rotz += .5
        if keys[pygame.K_v]:
            rotz -= .5
        if keys[pygame.K_ESCAPE]:
            blank = 0
            rotx = 0
            rotz = 0
            temp_pos = 0
            temp_pos_y = 0
            car.position[2] =  500

        pygame.draw.rect(window, (135, 206, 235), (0, 0, 1280, 720))
        car.position[0] =  temp_pos
        car.position[1] =  temp_pos_y
        car.rotation[0] = blank
        car.rotation[1] = rotx
        car.rotation[2] = rotz
        car.draw(window)

        if show_menu:
            menu.update(events)
            menu.draw(window)
        else:
            note = font.render("Press TAB to open Controls", True, (255, 255, 255))
            window.blit(note, (10, 10))

        pygame.display.update()
        ticks += 1

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()