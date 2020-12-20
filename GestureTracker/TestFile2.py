# possible_directions = [0,1,2,3]
# print(possible_directions[3])

def test():
    print("test")
    return (1,5,55,5), (2,4)

images = test()
mask, img = images[0],images[1]
print(mask, img)