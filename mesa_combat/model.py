import mesa
from .blue_agents.himars_unit import HIMARS
from .red_agents.buildings import EnemyTarget


class CombatModel(mesa.Model):
    
    def __init__(self, width = 10000, height = 10000):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.grid =mesa.space.ContinuousSpace(height, width, False)
        self.step_num = 1
        self.running = True
        self.current_id = 0
        
        # Create agents
        himarsAgent = HIMARS(unique_id=self.next_id(), model = self)
        self.schedule.add(himarsAgent)
        self.grid.place_agent(himarsAgent,(50,50))
        
        targetAgent = EnemyTarget(unique_id=self.next_id(), model =self, pos = (1000, 1000,0))
        self.schedule.add(targetAgent)
        self.grid.place_agent(targetAgent, (1000,1000))
        
        targetAgent2 = EnemyTarget(unique_id=self.next_id(), model =self, pos = (0,0,0))
        self.schedule.add(targetAgent2)
        self.grid.place_agent(targetAgent2, (0,0))
        
        targetAgent3 = EnemyTarget(unique_id=self.next_id(), model =self, pos = (1100, 1100,0))
        self.schedule.add(targetAgent3)
        self.grid.place_agent(targetAgent3, (1100,1100))
        
        #self.current_id = 8
    
    def step(self):
        self.schedule.step()
        self.step_num += 1 


