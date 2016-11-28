from distutils.core import setup
from setuptools import find_packages

setup(
    name='PyTexturePacker',
    packages=find_packages(exclude=['docs', 'tests', 'test_image']),
    version='0.0.1',
    description='an package to create sprite sheets or sprite atlases',
    author='Quanyong Huang',
    author_email='quanyongh@foxmail.com',
    url='https://github.com/wo1fsea/PyTexturePacker',
    download_url='https://github.com/wo1fsea/PyTexturePacker',
    keywords=['TexturePacker', 'cocos2d'],
    classifiers=[],
    license='MIT',
    install_requires=['Pillow'],
)
