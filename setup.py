from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='ecosim',
      version='0.1',
      install_requires=requirements,
      description='Natural selection simulation',
      url='https://github.com/herstky/eco-sim',
      author='Kyle Herstad',
      author_email='herstky@gmail.com',
      license='MIT',
      packages=['ecosim'],
      zip_safe=False)