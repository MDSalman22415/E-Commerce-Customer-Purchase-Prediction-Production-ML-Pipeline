from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    '''
    This function return list of function 
    '''
    requirements_list:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            ## 
            lines = file.readlines()
            for line in lines:
                requirements = line.strip()
                
                if requirements and requirements != '-e .':
                    requirements_list.append(requirements)
    except FileNotFoundError:
        print("Requirements.txt file required")
    
    return requirements_list

setup(
    name='E-Commerce Customer Purchase Prediction — Production ML Pipeline',
    version='0.0.1',
    author='Md Salman',
    author_email='mdsalmankhan41868@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)