from setuptools import setup, find_packages

setup(
    name="orfino",
    version="0.0.1",
    url="https://https://github.com/maximilianwank/orfino",
    author="Maximilian Wank",
    author_email="orfino@alpenjodel.de",
    description="Send notifications for filled orders on crypto exchanges",
    packages=["orfino"],
    install_requires=["ccxt >= 1.88.34"],
)
