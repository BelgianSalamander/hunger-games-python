from random import shuffle

file = open("last_names.txt","r")
names = file.read().split("\n")
print(len(names))
file.close()


f = open("last-names.txt","w")
for name in names:
    f.write(name[0].upper()+name[1:].lower()+"\n")
f.close()
