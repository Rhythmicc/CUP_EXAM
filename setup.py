from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = '2.6.11'

setup(
    name='CUP_EXAM',
    version=VERSION,
    description='Check exam information of China university of petroleum (Beijing)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='Check exam information',
    author='RhythmLian',
    author_mail='RhythmLian@outlook.com',
    url="https://github.com/Rhythmicc/CUP_EXAM",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['xlrd', 'requests', 'jieba'],
    entry_points={
        'console_scripts': [
            'exam = CUP_EXAM.frontend:main'
        ]
    },
)
