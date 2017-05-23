#-*- coding: utf-8 -*-
size = 30
color = (100, 60, 0)
lvl_texture = [size, color]

print lvl_texture

lvl_texture[0] = 2/3.0 * lvl_texture[0] + 1
lvl_texture[1] = (lvl_texture[1][0], lvl_texture[1][1] + 20, lvl_texture[1][2])

print lvl_texture