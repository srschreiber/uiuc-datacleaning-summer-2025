"""
Traverses for __init__.py files to generate .eggs files.
"""
from setuptools import setup, find_packages

setup(
    name='openai_client',
    version='0.1',
    packages=find_packages()
)