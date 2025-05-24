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


clock = pygame.time.Clock()


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
        [-1, 1.5, 0], [-1, -1, 0], [15, 1.5, 0], [15, -1, 0],
        [3, -1, 0], [4, -3, 0], [13, -1, 0], [11, -3, 0],
        [-1, 1.5, 6], [-1, -1, 6], [15, 1.5, 6], [15, -1, 6],
        [3, -1, 6], [4, -3, 6], [13, -1, 6], [11, -3, 6],
        [7, -1.25, 3],
        [1.75, .75, 0],
        [1.75, .75, 6],
        [4.25, .75, 0],
        [4.25, .75, 6],
        [1.75, 1.5, 0],
        [1.75, 1.5, 6],
        [4.25, 1.5, 0],
        [4.25, 1.5, 6],
        [13.25, .75, 0],
        [13.25, .75, 6],
        [10.75, .75, 0],
        [10.75, .75, 6],
        [13.25, 1.5, 0],
        [10.75, 1.5, 0],
        [13.25, 1.5, 6],
        [10.75, 1.5, 6],
        # Wheel vertices (cylinders)
        [2, 1, 0], [2, 3, 0], [4, 1, 0], [4, 3, 0],  # Front left wheel
        [13, 1, 0], [13, 3, 0], [11, 1, 0], [11, 3, 0],  # Front right wheel
        [2, 1, 6], [2, 3, 6], [4, 1, 6], [4, 3, 6],  # Rear left wheel
        [13, 1, 6], [13, 3, 6], [11, 1, 6], [11, 3, 6],  # Rear right wheel
        [2, 1, 0.75], [2, 3, 0.75], [4, 1, 0.75], [4, 3, 0.75],  # Front left wheel
        [13, 1, 0.75], [13, 3, 0.75], [11, 1, 0.75], [11, 3, 0.75],  # Front right wheel
        [2, 1, 5.25], [2, 3, 5.25], [4, 1, 5.25], [4, 3, 5.25],  # Rear left wheel
        [13, 1, 5.25], [13, 3, 5.25], [11, 1, 5.25], [11, 3, 5.25],  # Rear right wheel
        [1.75, .75, 1],
        [1.75, .75, 5],
        [4.25, .75, 1],
        [4.25, .75, 5],
        [1.75, 1.5, 1],
        [1.75, 1.5, 5],
        [4.25, 1.5, 1],
        [4.25, 1.5, 5],
        [13.25, .75, 1],
        [13.25, .75, 5],
        [10.75, .75, 1],
        [10.75, .75, 5],
        [13.25, 1.5, 1],
        [10.75, 1.5, 1],
        [13.25, 1.5, 5],
        [10.75, 1.5, 5]
    ]
    edges: list[list[int]] = [
        [0, 1],
        [0, 21],
        [21, 17],
        [17, 19],
        [19,23],
        [23, 30],
        [30, 27],
        [27, 25],
        [25, 29],
        [29, 2],
        [2, 3],
        [1, 4],
        [4, 5],
        [4, 6],
        [12, 14],
        [3, 6],
        [6, 7],
        [5, 7],
        [8, 9],
        [8, 22],
        [22, 18],
        [18, 20],
        [20,24],
        [24, 32],
        [32, 28],
        [28, 26],
        [26, 31],
        [31, 10],
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
        [33, 34], [34, 36], [36, 35], [35, 33],  # Front left wheel
        [37, 38], [38, 40], [40, 39], [39, 37],  # Front right wheel
        [41, 42], [42, 44], [44, 43], [43, 41],  # Rear left wheel
        [45, 46], [46, 48], [48, 47], [47, 45],  # Rear right wheel
        # Additional edges for wheel cylinders
        [49, 50], [50, 52], [52, 51], [49, 51], [49, 33], [50, 34], [51, 35], [52, 36],  # Front left wheel
        [53, 54], [54, 56], [56, 55], [55, 53], [53, 37], [54, 38], [55, 39], [56, 40],  # Front right wheel
        [57, 58], [58, 60], [60, 59], [59, 57], [57, 41], [58, 42], [59, 43], [60, 44],  # Rear left wheel
        [61, 62], [62, 64], [64, 63], [63, 61], [61, 45], [62, 46], [63, 47], [64, 48],   # Rear right wheel
        [69, 65],
        [65, 67],
        [67, 71],
        [78, 75],
        [75, 73],
        [73, 77],
        [70, 66],
        [66, 68],
        [68, 72],
        [80, 76],
        [76, 74],
        [74, 79],
        [17, 65,],
        [18, 66],
        [19, 67],
        [20, 68],
        [21, 69],
        [22, 70],
        [23, 71],
        [24, 72],
        [25, 73],
        [26, 74],
        [27, 75],
        [28, 76],
        [29, 77],
        [30, 78],
        [31, 79],
        [32, 80],
        [69, 71],
        [70, 72],
        [65, 67],
        [66, 68],
        [73, 75],
        [74, 76],
        [77, 78],
        [79, 80]
    ]
    faces: list[list[int]] = [
        [0, 1, 4, 5, 7, 6, 3, 2, 29, 25, 27, 30, 23, 19, 17, 21], #put stuff here
        [8, 9, 12, 13, 15, 14, 11, 10, 31, 26, 28, 32, 24, 20, 18, 22],#put stuf here
        [29, 30, 32, 31],
        [21, 23, 24, 22],
        [5, 7, 15, 13],
        [0, 1, 9, 8],
        [2, 3, 11, 10],
        [4, 5, 13, 12],
        [6, 7, 15, 14],
        [0, 21, 22, 8],
        [2, 29, 31, 10],
        [32, 24, 23, 30],
        [18, 22, 70, 66],
        [20, 24, 72, 68],
        [19, 23, 71, 67],
        [21, 17, 65, 69],
        [25, 29, 77, 73],
        [27, 30, 78, 75],
        [26, 31, 79, 74],
        [28, 32, 80, 76],
        [29, 25, 27, 30],
        [23, 19, 17, 21],
        [31, 26, 28, 32],
        [24, 20, 18, 22],
        [17, 19, 67, 65],
        [25, 27, 75, 73],
        [26, 28, 76, 74],
        [20, 18, 66, 68],
        [1, 4, 12, 9],
        [3, 6, 14, 11],
        # Wheel faces (cylinders)
        [33, 34, 36, 35],  # Front left wheel
        [37, 38, 40, 39],  # Front right wheel
        [41, 42, 44, 43],  # Rear left wheel
        [45, 46, 48, 47],  # Rear right wheel
        [49, 50, 52, 51],  # Front left wheel
        [53, 54, 56, 55],  # Front right wheel
        [57, 58, 60, 59],  # Rear left wheel
        [61, 62, 64, 63],  # Rear right wheel
        # Additional faces for wheel cylinders
        [33, 49, 50, 34], [35, 51, 52, 36], [33, 51, 49, 35], [34, 50, 52, 36],  # Front left wheel
        [37, 53, 54, 38], [39, 55, 56, 40], [37, 53, 55, 39], [38, 54, 56, 40],  # Front right wheel
        [41, 57, 58, 42], [43, 59, 60, 44], [41, 57, 59, 43], [42, 58, 60, 44],  # Rear left wheel
        [45, 61, 62, 46], [47, 63, 64, 48], [45, 61, 63, 47], [46, 62, 64, 48]  # Rear right wheel
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

        note2 = font.render(f"FPS: {int(round(clock.get_fps(), 0))}", True, (255, 255, 255))
        window.blit(note2, (10, 700))

        pygame.display.update()
        ticks += 1
        clock.tick(30)


    pygame.quit()
    exit()

if __name__ == "__main__":
    main()