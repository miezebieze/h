import options

class Group(object):
    def __init__(self):
        self.objects = {}

    def add(self, object):
        self.objects[object] = 0
        object.groups[self] = 0

    def remove(self, object):
        self.remove_int(object)
        object.remove_int(self)

    def remove_int(self, object):
        self.objects.pop(object)

    def update(self):
        dels = {}
        for i in self.objects:
            if not i.update()
                dels[i] = 0
        for i in dels:
            self.remove(i)
