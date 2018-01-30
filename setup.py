from setuptools import setup, find_packages

with open('requirements.txt') as fin:
  requirements = fin.read()

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
	name='corna',
    version='0.1.46',
    description='Natural Abundance Correction Toolbox',
    long_description=readme(),
    packages = find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Scientists',
        'Natural Language :: English',
        'Topic :: Scientific :: Metabolomics',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        requirements,
    ],
    package_data={
        '': ['*.bngl', '*.json']
    },

)
