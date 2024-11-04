from typing import List, Dict

class MotivationAgent:
    def __init__(self):
        self.goals = []

    def set_goal(self, goal: str):
        self.goals.append(goal)

    def get_goals(self) -> List[str]:
        return self.goals

    def track_progress(self) -> Dict:
        return {
            "completed": len(self.goals),
            "total": len(self.goals)
        } 