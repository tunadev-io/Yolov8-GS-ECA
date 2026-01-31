"""
Setup script for GE-YOLOv8 (Gradient Search + ECA modules)
This package provides custom YOLOv8 modules to be used with Ultralytics YOLOv8.

Installation:
    pip install ultralytics einops
    pip install -e .

Note: This will install the custom model configurations. Custom modules (CSP, ECAAttention) 
need to be manually copied to ultralytics installation. See train_ge_yolov8_kaggle.ipynb for details.
"""

from setuptools import setup, find_packages

setup(
    name='ge-yolov8',
    version='1.0.0',
    description='GE-YOLOv8: Custom YOLOv8 modules with Gradient Search (CSP) and ECA attention',
    author='tunadev-io',
    url='https://github.com/tunadev-io/Yolov8-GS-ECA',
    python_requires='>=3.8',
    
    # Include custom module source files  
    packages=find_packages(include=['nn', 'nn.*', 'models', 'models.*']),
    
    package_data={
        'models': ['**/*.yaml'],
    },
    include_package_data=True,
    
    # Dependencies
    install_requires=[
        'torch>=1.8.0',
        'torchvision>=0.9.0',
        'PyYAML>=5.3.1',
        'ultralytics>=8.0.0',
        'einops>=0.3.0',  # Required by custom conv modules
    ],
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
)
