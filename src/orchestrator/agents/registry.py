

class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent_id, agent):
        self.agents[agent_id] = agent

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)

    def unregister_agent(self, agent_id):
        if agent_id in self.agents:
            del self.agents[agent_id]