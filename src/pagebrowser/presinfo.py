class VitVPresInfo:
    def __init__(self, width: int, height: int):
        self.dimensions: tuple[int, int] = (width, height)
    @staticmethod
    def blank():
        return VitVPresInfo(
            width=0, 
            height=0
        )