class Hud(object):
    def __init__(s, game, options):
        """ Container for all the values of interest. """
        pass


class Basic(object):
    def __init__(s, game, options):
        """ Basic object for a single value """
        s.options = options
        s.valin = 0  # total value
        s.valout = 0 # increasing with frames while < valin
        s.max = 0

class Score(Basic):
    def __init__(s, game, options):
        Basic.__init__(s, game, options)
        s.

    def update(s):
        # for frame:
        if s.valout < s.valin:
            s.valout += 1
        elif s.valout > s.valin:
            s.valout -= 1
        
