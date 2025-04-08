"""
SDESA Python库 - 安装和配置文件
"""

from setuptools import setup, find_packages

setup(
    name="sdesa",
    version="0.1.0",
    author="SDESA开发团队",
    author_email="sdesa@example.com",
    description="基于SDESA的离散事件模拟Python库",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sdesa/sdesa-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "networkx",
        "plotly",
    ],
)
