import mesa


class EnemyTarget(mesa.Agent):
    '''Something to be shot at'''
    
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id,model)
        self.damage = 100
        #self.pos = pos
        self.agent_type = "Building"
        self.agent_side = "Red"