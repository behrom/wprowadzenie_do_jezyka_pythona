import os.path
CACHE = "cache/"

if not os.path.exists(CACHE):
    os.mkdir(CACHE)

print os.path.exists(CACHE + "1834.png")