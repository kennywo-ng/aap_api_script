from setuptools import setup, find_packages

setup(
    name="aap_api_script",
    version="0.1.4",
    description="API Automation for AAP (using Python Requests)",
    author="Kenny Wong",
    packages=find_packages(),
    python_requires=">=3.10,<3.13",
    install_requires=[
        "requests",
        "python-dotenv",
    ],
)
