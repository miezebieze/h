class main:
    def __init__(s):
        s.fps = 30
        s.frame = 0
        s.objects = []

    def tick(s):
        for obj in s.objects:
            obj.tick()

    def run(s):
        while True:
            do_stuff()
            self.tick()        

    def start(s):
        new = object(s)
        s.objects.append(new)
        s.run()

class object:
    def __init__(s, main):
        s.fps = 10
        s.frame = 0
        s.partframe = 0
        s.main = main
        s.partfps = 0

    def tick(s):
        s.partfps = 1.0 * s.main.fps / s.fps
        s.partframe += 1
        if s.partframe >= s.partfps:
            s.frame += 1
