class VitVDocInfo:
    def __init__(self, width: int, height: int):
        self.dimensions: tuple[int, int] = (width, height)
    @staticmethod
    def blank():
        return VitVDocInfo(
            width=0, 
            height=0
        )