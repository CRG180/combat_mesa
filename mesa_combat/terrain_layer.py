from mesa import Agent

class TerrainMap:
    
    def __init__(self) -> None:
        pass
    
    def line_of_sight(self,source:Agent,other:Agent) -> bool:
        return True