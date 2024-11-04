import pytest
from motivation_agent import MotivationAgent

@pytest.fixture
def motivation_agent():
    return MotivationAgent()

class TestMotivationAgent:
    def test_set_goal(self, motivation_agent):
        """Test setting a goal"""
        goal = "Apply to 5 jobs this week"
        motivation_agent.set_goal(goal)
        goals = motivation_agent.get_goals()
        assert goal in goals
        
    def test_track_progress(self, motivation_agent):
        """Test tracking progress"""
        motivation_agent.set_goal("Goal 1")
        motivation_agent.set_goal("Goal 2")
        progress = motivation_agent.track_progress()
        assert progress["completed"] == 2
        assert progress["total"] == 2 