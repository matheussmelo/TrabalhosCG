from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math

def f(x,y):
    return x**2 + y**2

M, N = 100, 100
x0, y0 = -2, -2
xf, yf = 2, 2
dx, dy = (xf - x0)/M, (yf - y0)/N
a = 0

def mesh():
    glPushMatrix()
    glRotatef(a,1.0,0.0,0.0)
    
    for i in range(0, N):
        y = y0 + i*dy
        glBegin(GL_QUAD_STRIP)
        for j in range(0,M):
            x = x0 + j*dx
            
            glVertex3f(x,y+dy,f(x,y))
            glVertex3f(x,y,f(x,y+dy))
        glEnd()
    glPopMatrix()


def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    mesh()
    a+=1
    glutSwapBuffers()
  
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(10,timer,1)

# PROGRAMA PRINCIPAL
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(1024,1024)
glutCreateWindow("Paraboloide com equacao implicita")
glutDisplayFunc(desenha)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0,0,0,1)
gluPerspective(45,800.0/600.0,0.1,100.0)
glTranslatef(0.0,0.0,-10)
glutTimerFunc(10,timer,1)
glutMainLoop()
