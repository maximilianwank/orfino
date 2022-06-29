from setuptools import setup

setup(
    name="orfino",
    version="0.1.0",
    url="https://github.com/maximilianwank/orfino",
    author="Maximilian Wank",
    author_email="orfino@alpenjodel.de",
    description="Send notifications for filled orders on crypto exchanges",
    packages=["orfino"],
    license="MIT",
    install_requires=["ccxt >= 1.88.34"],
)
