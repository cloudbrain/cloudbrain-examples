from setuptools import find_packages, setup



def findRequirements():
  """
  Read the requirements.txt file and parse into requirements for setup's
  install_requirements option.
  """
  return [line.strip()
          for line in open("requirements.txt").readlines()
          if not line.startswith("#")]


setup(name="cloudbrain_examples",
      version="0.0.1",
      description="CloudBrain Examples",
      author="Marion Le Borgne",
      url="https://github.com/cloudbrain/cloudbrain-examples",
      packages=find_packages(),
      install_requires=findRequirements(),
      license=open('LICENSE.txt').read(),
      long_description=open('README.md').read()
      )
