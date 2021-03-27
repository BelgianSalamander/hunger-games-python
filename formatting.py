def represent(l):
    if len(l) == 0:
        return "nothing"
    if len(l) == 1:
        return "a {:}".format(l[0])
    if len(l) == 2:
        return "a {:} and a {:}".format(l[0],l[1])
    if len(l) > 2:
        return "a {:}, a ".format(l[0]) + ", a ".join(l[1:-1]) + " and a {:}".format(l[-1])

def repr_players(l):
    try:
        l = [player.name for player in l]
    except:
        pass
    if len(l) == 0:
        return "noone"
    if len(l) == 1:
        return "{:}".format(l[0])
    if len(l) == 2:
        return "{:} and {:}".format(l[0],l[1])
    if len(l) > 2:
        return "{:}, ".format(l[0]) + ", ".join(l[1:-1]) + " and {:}".format(l[-1])