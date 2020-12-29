import glfw
from OpenGL.GL import *
import numpy as np

inputvalue = 4

def key_callback(window, key, scancode, action, mods):
    global inputvalue
    if key == glfw.KEY_Q:
        if action == glfw.PRESS:
            inputvalue = "Q"
    elif key == glfw.KEY_E:
        if action == glfw.PRESS:
            inputvalue = "E"
    elif key == glfw.KEY_A:
        if action == glfw.PRESS:
            inputvalue = "A"
    elif key == glfw.KEY_D:
        if action == glfw.PRESS:
            inputvalue = "D"
    elif key == glfw.KEY_1:
        if action == glfw.PRESS:
            inputvalue = 1
    elif key == glfw.KEY_W:
        if action == glfw.PRESS:
            inputvalue = "S"
    elif key == glfw.KEY_S:
        if action == glfw.PRESS:
            inputvalue = "S"

def render(T):
 glClear(GL_COLOR_BUFFER_BIT)
 glLoadIdentity()
 # draw cooridnate
 glBegin(GL_LINES)
 glColor3ub(255, 0, 0)
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([1.,0.]))
 glColor3ub(0, 255, 0)
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([0.,1.]))
 glEnd()
 # draw triangle
glBegin(GL_TRIANGLES)
 glColor3ub(255, 255, 255)
 glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
 glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
 glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
 glEnd()


def main():
    alist = [GL_POLYGON, GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP,
             GL_TRIANGLES, GL_TRIANGLE_STRIP,GL_TRIANGLE_FAN,
             GL_QUADS,GL_QUAD_STRIP]
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"CG_weekly_practice_04_2018063218",None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        global inputvalue
        render(alist[inputvalue])
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
