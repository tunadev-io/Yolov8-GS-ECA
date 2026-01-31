"""
Setup script for GE-YOLOv8 (Gradient Search + ECA modules)
This package extends Ultralytics YOLOv8 with custom architectural components.

Installation:
    pip install -e .

This will install ultralytics along with the custom GE modules.
"""

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess
import sys
import os
import shutil

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # First install ultralytics
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics>=8.0.0"])
        
        # Run the standard develop installation
        develop.run(self)
        
        # Copy custom files to ultralytics installation
        self._copy_custom_files()
    
    def _copy_custom_files(self):
        """Copy custom modules to installed ultralytics package"""
        try:
            import ultralytics
            ultralytics_path = os.path.dirname(ultralytics.__file__)
            
            # Copy custom nn/modules files
            src_modules = os.path.join(os.getcwd(), 'nn', 'modules')
            dst_modules = os.path.join(ultralytics_path, 'nn', 'modules')
            
            if os.path.exists(src_modules):
                for file in ['block.py', 'Attention.py', 'CoordAttention.py', 
                            'C2f_faster.py', 'C2f_SCconv.py', 'RFCAConv.py']:
                    src = os.path.join(src_modules, file)
                    if os.path.exists(src):
                        dst = os.path.join(dst_modules, file)
                        shutil.copy2(src, dst)
                        print(f"Copied {file} to ultralytics")
                
                # Update __init__.py
                src_init = os.path.join(src_modules, '__init__.py')
                dst_init = os.path.join(dst_modules, '__init__.py')
                if os.path.exists(src_init):
                    shutil.copy2(src_init, dst_init)
                    print("Updated ultralytics nn/modules/__init__.py")
            
            print("✓ Custom GE-YOLOv8 modules installed successfully")
        except Exception as e:
            print(f"Warning: Could not copy custom files: {e}")

setup(
    name='ge-yolov8',
    version='1.0.0',
    description='GE-YOLOv8: Ultralytics YOLOv8 with Gradient Search and ECA modules',
    author='Ultralytics (Extended by tunadev-io)',
    url='https://github.com/tunadev-io/Yolov8-GS-ECA',
    python_requires='>=3.8',
    
    # Include the custom modules and model configs as data
    packages=['nn', 'nn.modules', 'models', 'datasets', 'hub', 'tracker', 
              'tracker.trackers', 'tracker.utils', 'vit', 'vit.rtdetr'],
    
    package_data={
        'models': ['v8/*.yaml', 'v5/*.yaml', 'v6/*.yaml', 'v3/*.yaml', 'rt-detr/*.yaml'],
        'nn': ['*.py'],
        'nn.modules': ['*.py'],
    },
    include_package_data=True,
    
    # Install ultralytics as dependency
    install_requires=[
        'ultralytics>=8.0.0',
        'torch>=1.8.0',
        'torchvision>=0.9.0',
        'PyYAML>=5.3.1',
    ],
    
    cmdclass={
        'develop': PostDevelopCommand,
    },
    
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
