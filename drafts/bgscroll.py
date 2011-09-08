class Layer(object):
    def __init__(s, game):
        """ single layer containing parts """
        s._game = game
        s.scrollspeed = 0
        s.position = (0,0)
        

    def update(s):
        s.move
