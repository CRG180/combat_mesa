
from mesa_combat.model import CombatModel
from mesa.experimental import JupyterViz


def agent_portrayal(agent):
  size = 50
  color ="tab:red"
  if agent.agent_side == "Blue":
    size = 50
    color = "tab:blue"
  return {"color": color,"size": size}

if __name__ == '__main__':
  model_params = {}   
  page = JupyterViz(
      CombatModel,
      model_params,
      name="Combat Model",
      agent_portrayal=agent_portrayal)

  page
  
# model = CombatModel()
# for _ in range(25):
#    model.step()