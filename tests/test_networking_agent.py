import pytest
from networking_agent import NetworkingAgent

@pytest.fixture
def network_agent():
    return NetworkingAgent()

class TestNetworkingAgent:
    def test_add_contact(self, network_agent):
        """Test adding a contact"""
        network_agent.add_contact(
            name="John Doe",
            company="TestCorp",
            position="Data Scientist"
        )
        contacts = network_agent.get_contacts()
        assert len(contacts) == 1
        assert contacts[0]["name"] == "John Doe"
        
    def test_generate_referral_request(self, network_agent):
        """Test generating referral request"""
        request = network_agent.generate_referral_request("John")
        assert isinstance(request, str)
        assert "John" in request 