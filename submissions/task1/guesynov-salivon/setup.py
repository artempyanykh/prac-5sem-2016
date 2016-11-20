from setuptools import setup, find_packages

setup(name='Nash Equilibrium',
      version='0.1',
      description='Ridiculous Nash equilibrium',
      url='http://github.com/doesnt/matter',
      author='IO team',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'nose',
        'nose-parameterized',
        'numpy',
        'scipy'
      ],
      zip_safe=False)
