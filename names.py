from random import choice, randint

f = open("m-names.txt")
male = f.read().split("\n")
f.close()

f = open("f-names.txt")
female = f.read().split("\n")
f.close()

f = open("last-names.txt")
last_names = f.read().split("\n")
f.close()

def name():
    last_name = choice(last_names)
    if randint(0,1) == 0:
        first_name = choice(male)
        #print("Male")
    else:
        first_name = choice(female)
        #print("Female")
    return first_name + " " + last_name