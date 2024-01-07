import mesa
from  ..utils.trajectory import generate_curved_trajectory
from typing import List, Tuple

# For Mypy
Cord3D = Tuple[float,float,float]

class CommandNode(mesa.Agent):
    '''Provides Tragets to HIMARS'''
    
    def __init__(self, unique_id, model):
        super.__init__(unique_id, model)
        
class SensorNode(mesa.Agent):
    '''Find enemy targets and send information to CommandNode'''
    
    def __init__(self, unique_id, model):
        super.__init__(unique_id, model)

class HIMARS(mesa.Agent):
    '''Vehicle that lanches PrSM'''
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.agent_type = "PRSM"
        self.agent_side = "Blue"
        self.number_munitions = 4
        self.altitude = 0
        self.mission_dict = {}
    
    @property
    def origin(self):
        return self.pos +(self.altitude,)
    
    def get_mission(self):
        pass
    
    def fire_mission(self):
        prsmAgent = PRSM(unique_id=self.model.next_id(), 
                            model=self.model,
                            start_location = self.origin,
                            target_location= (1000,1000,0),
                            speed =250)
        self.model.schedule.add(prsmAgent)
        self.model.grid.place_agent(prsmAgent,self.pos) 
    
    def step(self) -> None:
        if self.model.step_num % 7 == 0:
            self.fire_mission()


class PRSM(mesa.Agent):
    '''Munition From HIMARS'''
    
    def __init__(self, unique_id, model, start_location, target_location, speed)->None:
        super().__init__(unique_id, model)
        self.agent_type = "PRSM"
        self.agent_side = "Blue"
        self.speed = speed  # m/s
        self.start_location = start_location # Initial position (x,y,z)
        self.altitude = start_location[2]
        self.pos = tuple(start_location[:2])  
        self.target_location = target_location  # Example target location
        self.max_altitude = 10000  # Maximum altitude in meters
        self.blast_radius = 100 # meters
        self.trajectory:List[Cord3D] =  generate_curved_trajectory(
                                    origin = self.start_location, 
                                    destination = self.target_location,
                                    peak_z = self.max_altitude,
                                    speed =self.speed,
                                    time_resolution=1.0)
 
    def move(self)->None:
        if self.trajectory:
            new_position = self.trajectory.pop(0)
            self.altitude = new_position[2]
            new_position = tuple(new_position[:2])
            self.model.grid.move_agent(self,new_position)
            print(f"Agent {self.unique_id} is at grid {self.pos} {self.altitude} at time {self.model.step_num} seconds")
        else:
            self.destroy()
            
    def destroy(self)->None:
        print(f"reached traget time to Kill at {self.pos}")
        targets = self.model.grid.get_neighbors(
                                    pos = self.pos,
                                    radius = self.blast_radius, 
                                    include_center = True)
        
        for agent in targets:
            print(f'Killing Agent {agent.unique_id}')
            self.model.grid.remove_agent(agent)
            self.model.schedule.remove(agent)
        
    def step(self):
        self.move()
    

        
    