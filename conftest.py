import pytest
import asyncio

def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as asyncio test")

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function", autouse=True)
async def setup_test():
    """Setup and cleanup for each test."""
    # Setup
    yield
    # Cleanup
    await asyncio.sleep(0)  # Allow pending tasks to complete

@pytest.fixture(scope="function")
async def event_loop_policy():
    """Override the default event loop policy for the test session."""
    policy = asyncio.get_event_loop_policy()
    return policy