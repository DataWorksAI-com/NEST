#!/usr/bin/env python3
"""
Setup script for Streamlined NANDA Adapter
"""

from setuptools import setup, find_packages
import os


def read_requirements():
    """Read requirements from file"""
    requirements = [
        "anthropic>=0.18.0",
        "a2a-sdk>=0.2.0",  # Official A2A SDK (replaced python-a2a)
        "httpx>=0.27.0",  # For async HTTP (replaces requests)
        "uvicorn>=0.30.0",  # ASGI server for A2A
        "starlette>=0.37.0",  # For A2A server (included with a2a-sdk)
        "python-dotenv>=1.0.0",
        "psutil>=5.9.0",  # For system monitoring
    ]
    return requirements


def read_readme():
    """Read README file for long description"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "NEST - NANDA Sandbox and Testbed"


setup(
    name="nest",
    version="2.0.0",
    description="NEST - NANDA Sandbox and Testbed for intelligent agent deployment and coordination",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="NANDA Team",
    author_email="support@nanda.ai",
    url="https://github.com/projnanda/NEST.git",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "black", "flake8"],
        "monitoring": ["prometheus-client", "grafana-api"],
    },
    entry_points={
        "console_scripts": [
            "streamlined-adapter=nanda_core.core.adapter:main",
            "nanda-discover=nanda_core.discovery.agent_discovery:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="nanda ai agent framework streamlined discovery telemetry",
    include_package_data=True,
    zip_safe=False,
)