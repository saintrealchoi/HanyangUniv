import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0.
gCamHeight = 1.
a=0
b=0
c=0

def render(ang):
    global a,b,c
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5 * np.sin(gCamAng), gCamHeight, 5 * np.cos(gCamAng), 0, 0, 0, 0, 1, 0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_RESCALE_NORMAL)  # rescale normal vectors after transformation and before lighting to have unit length

    # set light properties
    lightPos = (1., 2., 3., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    ambientLightColor = (.1, .1, .1, 1.)
    diffuseLightColor = (1., 1., 1., 1.)
    specularLightColor = (1., 1., 1., 1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor)

    # ZYX Euler angles
    xang = np.radians(a)
    yang = np.radians(b)
    zang = np.radians(c)
    M = np.identity(4)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(yang), -np.sin(yang)],
                   [0, np.sin(yang), np.cos(yang)]])
    Ry = np.array([[np.cos(zang), -np.sin(zang),0],
                   [np.sin(zang), np.cos(zang), 0],
                   [0,0,1]])
    Rz = np.array([[np.cos(xang), -np.sin(xang), 0],
                   [np.sin(xang), np.cos(xang), 0],
                   [0, 0, 1]])
    M[:3, :3] = Rz @ Rx @ Ry
    glMultMatrixf(M.T)

    # # The same ZYX Euler angles with OpenGL functions
    # glRotate(30, 0,0,1)
    # glRotate(30, 0,1,0)
    # glRotate(ang, 1,0,0)

    glScalef(.25, .25, .25)

    # draw cubes
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (.5, .5, .5, 1.))
    drawCube_glDrawArray()

    glTranslatef(3, 0, 0)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1., 0., 0., 1.))
    drawCube_glDrawArray()

    glTranslatef(-3, 3, 0)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0., 1., 0., 1.))
    drawCube_glDrawArray()

    glTranslatef(0, -3, 3)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0., 0., 1., 1.))
    drawCube_glDrawArray()

    glDisable(GL_LIGHTING)


def drawCube_glVertex():
    glBegin(GL_TRIANGLES)

    glNormal3f(0, 0, 1)  # v0, v2, v1, v0, v3, v2 normal
    glVertex3f(-1, 1, 1)  # v0 position
    glVertex3f(1, -1, 1)  # v2 position
    glVertex3f(1, 1, 1)  # v1 position

    glVertex3f(-1, 1, 1)  # v0 position
    glVertex3f(-1, -1, 1)  # v3 position
    glVertex3f(1, -1, 1)  # v2 position

    glNormal3f(0, 0, -1)
    glVertex3f(-1, 1, -1)  # v4
    glVertex3f(1, 1, -1)  # v5
    glVertex3f(1, -1, -1)  # v6

    glVertex3f(-1, 1, -1)  # v4
    glVertex3f(1, -1, -1)  # v6
    glVertex3f(-1, -1, -1)  # v7

    glNormal3f(0, 1, 0)
    glVertex3f(-1, 1, 1)  # v0
    glVertex3f(1, 1, 1)  # v1
    glVertex3f(1, 1, -1)  # v5

    glVertex3f(-1, 1, 1)  # v0
    glVertex3f(1, 1, -1)  # v5
    glVertex3f(-1, 1, -1)  # v4

    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1, 1)  # v3
    glVertex3f(1, -1, -1)  # v6
    glVertex3f(1, -1, 1)  # v2

    glVertex3f(-1, -1, 1)  # v3
    glVertex3f(-1, -1, -1)  # v7
    glVertex3f(1, -1, -1)  # v6

    glNormal3f(1, 0, 0)
    glVertex3f(1, 1, 1)  # v1
    glVertex3f(1, -1, 1)  # v2
    glVertex3f(1, -1, -1)  # v6

    glVertex3f(1, 1, 1)  # v1
    glVertex3f(1, -1, -1)  # v6
    glVertex3f(1, 1, -1)  # v5

    glNormal3f(-1, 0, 0)
    glVertex3f(-1, 1, 1)  # v0
    glVertex3f(-1, -1, -1)  # v7
    glVertex3f(-1, -1, 1)  # v3

    glVertex3f(-1, 1, 1)  # v0
    glVertex3f(-1, 1, -1)  # v4
    glVertex3f(-1, -1, -1)  # v7
    glEnd()


def createVertexArraySeparate():
    varr = np.array([
        (0, 0, 1),  # v0 normal
        (-1, 1, 1),  # v0 position
        (0, 0, 1),  # v2 normal
        (1, -1, 1),  # v2 position
        (0, 0, 1),  # v1 normal
        (1, 1, 1),  # v1 position

        (0, 0, 1),  # v0 normal
        (-1, 1, 1),  # v0 position
        (0, 0, 1),  # v3 normal
        (-1, -1, 1),  # v3 position
        (0, 0, 1),  # v2 normal
        (1, -1, 1),  # v2 position

        (0, 0, -1),
        (-1, 1, -1),  # v4
        (0, 0, -1),
        (1, 1, -1),  # v5
        (0, 0, -1),
        (1, -1, -1),  # v6

        (0, 0, -1),
        (-1, 1, -1),  # v4
        (0, 0, -1),
        (1, -1, -1),  # v6
        (0, 0, -1),
        (-1, -1, -1),  # v7

        (0, 1, 0),
        (-1, 1, 1),  # v0
        (0, 1, 0),
        (1, 1, 1),  # v1
        (0, 1, 0),
        (1, 1, -1),  # v5

        (0, 1, 0),
        (-1, 1, 1),  # v0
        (0, 1, 0),
        (1, 1, -1),  # v5
        (0, 1, 0),
        (-1, 1, -1),  # v4

        (0, -1, 0),
        (-1, -1, 1),  # v3
        (0, -1, 0),
        (1, -1, -1),  # v6
        (0, -1, 0),
        (1, -1, 1),  # v2

        (0, -1, 0),
        (-1, -1, 1),  # v3
        (0, -1, 0),
        (-1, -1, -1),  # v7
        (0, -1, 0),
        (1, -1, -1),  # v6

        (1, 0, 0),
        (1, 1, 1),  # v1
        (1, 0, 0),
        (1, -1, 1),  # v2
        (1, 0, 0),
        (1, -1, -1),  # v6

        (1, 0, 0),
        (1, 1, 1),  # v1
        (1, 0, 0),
        (1, -1, -1),  # v6
        (1, 0, 0),
        (1, 1, -1),  # v5

        (-1, 0, 0),
        (-1, 1, 1),  # v0
        (-1, 0, 0),
        (-1, -1, -1),  # v7
        (-1, 0, 0),
        (-1, -1, 1),  # v3

        (-1, 0, 0),
        (-1, 1, 1),  # v0
        (-1, 0, 0),
        (-1, 1, -1),  # v4
        (-1, 0, 0),
        (-1, -1, -1),  # v7
    ], 'float32')
    return varr


def drawCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 6))


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    global a,b,c
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key == glfw.KEY_2:
            gCamHeight += .1
        elif key == glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_A:
            a = a+10
        elif key==glfw.KEY_Z:
            a = a-10
        elif key==glfw.KEY_S:
            b = b+10
        elif key==glfw.KEY_X:
            b = b-10
        elif key==glfw.KEY_D:
            c = c+10
        elif key==glfw.KEY_C:
            c = c-10
        elif key==glfw.KEY_V:
            a=0
            b=0
            c=0


gVertexArraySeparate = None


def main():
    global gVertexArraySeparate

    if not glfw.init():
        return
    window = glfw.create_window(480, 480, 'CG_weekly_practice_08_2018063218', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArraySeparate = createVertexArraySeparate()

    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        ang = count % 360
        render(ang)
        count += 1
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()




