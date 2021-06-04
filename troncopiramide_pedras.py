from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from sys import argv
import math 
import png


# Window Name
window_name = "Tronco de Pirâmide de Pedras"

# Rotation vars
left_button = False
alpha = -90.0
beta = 180.0
delta_alpha = 0.5

# Translation vars
right_button = False
delta_x, delta_y, delta_z = 0, 0, 0

down_x, down_y = 0, 0


# Background Color RGBA
background_color = (0.184, 0.211, 0.250, 1)

# Figure vars
raio = 2
N = 5
H = 3
n1 = 50
n2 = 50
r = 2

# Figure functions


# Texture vars
texture = []

# Textures functions
def load_textures():
    global texture
    texture = glGenTextures(2) # Gera 2 IDs para as texturas

    
    reader = png.Reader(filename='pedras.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    


def figure():
    pontosBase = []
    pontosTampa = []
    angulo = (2*math.pi)/N
    glPushMatrix()

    # Translation and Zoom
    glTranslatef(delta_x, delta_y, delta_z)

    # Rotation
    # X axis
    glRotatef(alpha, 0.0, 1.0, 0.0)
    # Y axis
    glRotatef(beta, 0.0, 0.0, 1.0)

    # Figure
    glBindTexture(GL_TEXTURE_2D, texture[0])

    # BASE

    glBegin(GL_POLYGON)
    for i in range(0,N):
        x1 = r * math.cos(i*angulo)
        y1 = r * math.sin(i*angulo)
        pontosBase += [ (x1,y1) ]
        glTexCoord2f(x1,y1)
        glVertex3f(x1,y1,0.0)
    glEnd()

    # TAMPA
    glBegin(GL_POLYGON)
    for i in range(0,N):
        x2 = r/2 * math.cos(i*angulo)
        y2 = r/2 * math.sin(i*angulo)
        pontosTampa += [ (x2,y2) ]
        glTexCoord2f(x2,y2)
        glVertex3f(x2,y2,H)
    glEnd()

    # LATERAL
    glBegin(GL_QUADS)
    for i in range(0,N):
        #glColor3fv(cores[(i+1)%len(cores)])
        glTexCoord2f(0,0)
        glVertex3f(pontosTampa[i][0],pontosTampa[i][1],H)
        glTexCoord2f(0,1)
        glVertex3f(pontosBase[i][0],pontosBase[i][1],0.0)
        glTexCoord2f(1,0)
        glVertex3f(pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],0.0)
        glTexCoord2f(1,1)
        glVertex3f(pontosTampa[(i+1)%N][0],pontosTampa[(i+1)%N][1],H)
    glEnd()

    glPopMatrix()


def draw():
    global alpha, left_button, right_button

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    figure()

    # Auto-Rotation
    alpha = alpha + delta_alpha

    glutSwapBuffers()


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(10, timer, 1)


def special_key_pressed(key, x, y):
    """
    Template.

    Use for Up, Down, Left and Right arrows.
    """
    pass


def key_pressed(key, x, y):
    global delta_alpha

    if key == b"\033":
        glutLeaveMainLoop()

    # Toggles Rotation
    elif key == b" ":
        if delta_alpha == 0:
            delta_alpha = 0.5
        else:
            delta_alpha = 0


def mouse_click(button, state, x, y):
    global down_x, down_y, left_button, right_button, delta_z

    down_x, down_y = x, y

    left_button = button == GLUT_LEFT_BUTTON and state == GLUT_DOWN
    right_button = button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN

    # Zoom
    if button == 3 and state == GLUT_DOWN:
        delta_z += 1
    elif button == 4 and state == GLUT_DOWN:
        delta_z -= 1


def mouse_move(x, y):
    global alpha, beta, down_x, down_y, delta_x, delta_y, delta_alpha

    # Rotate
    if left_button:
        delta_alpha = 0
        # Alpha calculations and bounds
        alpha += ((x - down_x) / 4.0) * -1

        if alpha >= 360:
            alpha -= 360

        if alpha <= 0:
            alpha += 360

        # Beta calculations and bounds
        if alpha >= 180:
            beta -= (y - down_y) / 4.0 * -1
        else:
            beta += (y - down_y) / 4.0 * -1

        if beta >= 360:
            beta -= 360

        if beta <= 0:
            beta += 360

    # Translate
    if right_button:
        delta_x += -1 * (x - down_x) / 100.0
        delta_y += (y - down_y) / 100.0

    down_x, down_y = x, y

    glutPostRedisplay()


def main():    
    glutInit(argv)
    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE
    )

    # Creating a screen with good resolution proportions
    screen_width = glutGet(GLUT_SCREEN_WIDTH)
    screen_height = glutGet(GLUT_SCREEN_HEIGHT)

    window_width = round(2 * screen_width / 3)
    window_height = round(2 * screen_height / 3)

    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(
        round((screen_width - window_width) / 2), round((screen_height - window_height) / 2)
    )
    glutCreateWindow(window_name)

    # Drawing Function
    glutDisplayFunc(draw)

    # Input Functions
    glutSpecialFunc(special_key_pressed)
    glutKeyboardFunc(key_pressed)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_move)

    load_textures()

    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glClearColor(*background_color)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)

    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)

    # Pre-render camera positioning
    gluPerspective(-45, window_width / window_height, 0.1, 100.0)
    glTranslatef(0.0, 0.0, -10)

    glMatrixMode(GL_MODELVIEW)

    glutTimerFunc(10, timer, 1)
    glutMainLoop()

if(__name__ == '__main__'):
    main()
