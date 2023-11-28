from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='elec_price_pred',
      version="0.0.12",
      description="Electricity Price Prediction",
      license="MIT",
      author="Nepomuk11",
      author_email="mylius.nepomuk11@gmail.co",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
