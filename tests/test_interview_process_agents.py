import pytest
from interview_process_agents import InterviewProcessManager
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
class TestInterviewProcessManager:
    async def test_get_completion(self):
        """Test OpenAI completion"""
        manager = InterviewProcessManager(openai_api_key="test_key")
        messages = [{"role": "user", "content": "test"}]
        
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        
        mock_create = AsyncMock(return_value=mock_response)
        
        with patch.object(manager.client.chat.completions, 'create', new=mock_create):
            response = await manager.get_completion(messages)
            assert response == "Test response"
            
    async def test_get_completion_error(self):
        """Test OpenAI completion error handling"""
        manager = InterviewProcessManager(openai_api_key="test_key")
        messages = [{"role": "user", "content": "test"}]
        
        mock_create = AsyncMock(side_effect=Exception("API Error"))
        
        with patch.object(manager.client.chat.completions, 'create', new=mock_create):
            with pytest.raises(Exception) as exc_info:
                await manager.get_completion(messages)
            assert "OpenAI API error" in str(exc_info.value) 