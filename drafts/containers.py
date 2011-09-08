class Basic(object):
    def __init__(s, options):
        pass
    def update(s):
        pass

class Money(Basic):
    ''' Make the class for Objects also the container
        for all objects of the same type. '''
    instances = []

    def __init__(s, options):
        Basic.__init__(options)
        s.occurence.append(s)


class Game(object):
    def __init__(s):
        s.objectqueue = [Money, Othertypeofobjects]

    def update(s):
        for j in range(len(s.objectqueue)):
            for i in range(len(i.instances)):
                i.update()
