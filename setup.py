from setuptools import setup, find_packages

setup(
    name="interview_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'pytest',
        'pytest-asyncio',
        'pytest-mock',
        'openai>=1.0.0',
        'fastapi',
        'uvicorn',
        'jinja2',
        'pydantic'
    ],
) 