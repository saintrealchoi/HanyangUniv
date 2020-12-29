import glfw
from OpenGL.GL import *
import numpy as np

origin = np.array([[1,0,0],[0,1,0],[0,0,1]])

def key_callback(window, key, scancode, action, mods):
    inputvalue = np.array([[1,0,0],[0,1,0],[0,0,1]])
    global origin

    if key == glfw.KEY_Q:
        if action == glfw.PRESS or action==glfw.REPEAT:
            inputvalue = np.array([[1,0,-0.1],[0,1,0],[0,0,1]])
            origin=inputvalue@origin
    elif key == glfw.KEY_E:
        if action == glfw.PRESS or action==glfw.REPEAT:
            inputvalue = np.array([[1,0,0.1],[0,1,0],[0,0,1]])
            origin=inputvalue@origin
    elif key == glfw.KEY_A:
        if action == glfw.PRESS or action==glfw.REPEAT:
            inputvalue = np.array([[np.cos(np.radians(10)),-np.sin(np.radians(10)),0],
                               [np.sin(np.radians(10)),np.cos(np.radians(10)),0],
                               [0,0,1]])
            origin=origin@inputvalue
    elif key == glfw.KEY_D:
        if action == glfw.PRESS or action==glfw.REPEAT:
            inputvalue = np.array([[np.cos(np.radians(-10)),-np.sin(np.radians(-10)),0],
                                   [np.sin(np.radians(-10)),np.cos(np.radians(-10)),0],
                                   [0,0,1]])
            origin=origin@inputvalue
    elif key == glfw.KEY_1:
        if action == glfw.PRESS or action==glfw.REPEAT:
            origin = np.array([[1,0,0],[0,1,0],[0,0,1]])
    elif key == glfw.KEY_W:
        if action == glfw.PRESS or action==glfw.REPEAT:
            inputvalue = np.array([[0.9,0,0],[0,1,0],[0,0,1]])
            origin=inputvalue@origin
    elif key == glfw.KEY_S:
        if action == glfw.PRESS or action == glfw.REPEAT:
            inputvalue = np.array([[np.cos(np.radians(10)),-np.sin(np.radians(10)),0],
                                   [np.sin(np.radians(10)),np.cos(np.radians(10)),0],
                                   [0,0,1]])
            origin=inputvalue@origin

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
        global origin
        render(origin)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
