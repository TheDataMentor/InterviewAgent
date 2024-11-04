from typing import List, Dict

class NetworkingAgent:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name: str, company: str, position: str):
        self.contacts.append({
            "name": name,
            "company": company,
            "position": position
        })

    def get_contacts(self) -> List[Dict]:
        return self.contacts

    def generate_referral_request(self, contact_name: str) -> str:
        return f"Hi {contact_name}, I hope you're doing well! I'm currently applying for a position at your company and would appreciate any insights you could share." 