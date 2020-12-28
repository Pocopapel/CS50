from cs50 import get_int

while True:
    size = get_int("what is the desired size of the pyramid?:")
    if (size > 0 and size < 9):
        break
space = 0
hash = 0
for i in range(size):
    for space in range(0, i - size + 1, -1):
        print(" ", end="")
    for hash in range(0, i + 1):
        print("#", end="")
        hash += 1
    print("  ", end="")
    for hash in range(0, i + 1):
        print("#", end="")
        hash += 1
    print("")

