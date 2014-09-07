try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='GogleBot',
    version='0.0.1',
    description=('A Horrible Project based on the Hangups library'),
    long_description=open('README.md').read(),
    url='https://github.com/banduccm/GogleBot',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    package_dir={'GogleBot': ''},
    packages=['GogleBot'],
    install_requires=[
        'hangups == 0.1.3',
        'wikipedia == 1.3.1',
    ],
)
