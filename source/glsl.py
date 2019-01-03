

class GLSL_Type_Interface:
    pass



class Struct:
    def __init__(self, **members):
        pass


class Array:
    def __init__(self, *elements, count=-1):
        if count == -1:
            count = len(elements)