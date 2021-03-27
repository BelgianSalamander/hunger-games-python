from random import randint
import traceback

def tester(func):
    def f(*args,**kwargs):
        try:
            func(*args,**kwargs)
            return True
        except Exception as e:
            #print(traceback.format_exc())
            return False
    return f

class GameEnded(Exception):
    pass


#functions = []

#for a in range(5):
#    @tester
#    def f():
#        if randint(1,3)==3:
#            raise
#        print(a)
#    functions.append(f)

def execute(count, *functions, before = lambda : 0, names = None):
    #print(f"Attempting execution of {count} functions!")
    functions = list(functions)
    orig = [f[0] for f in functions]

    total = sum(f[1] for f in functions)
    executions = 0

    while executions <= count and total > 0:
        try:
            before()
        except GameEnded:
            return
        n = randint(1,total)
        index = 0
        for function in functions:
            n -= function[1]
            if n <= 0:
                break
            index += 1
        success = function[0]()
        if success:
            executions += 1
            function[2] -= 1
            if not function[2]:
                total -= function[1]
                del functions[index]
        else:
            #if(names != None):
            #    print(names[orig.index(function[0])] + " Failed")
            total -= function[1]
            del functions[index]

#execute(14,*[[function,1,2] for function in functions])
