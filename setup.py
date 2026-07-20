## This enables making ML project as a package like any other package like pandas, seaborn, etc.

from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements
setup(
    name="MLProject",
    version='0.0.1',
    author='Taha',
    author_email="tahatariqf@gmail.com",
    packages=find_packages(),    # finds all the packages for ML app in the directory
    install_requires=get_requirements('requirements.txt')
)