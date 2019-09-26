import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
#

version = __import__("startmicro").__version__

setuptools.setup(
    name="microstarter",
    version=version,
    author="Munis Isazade",
    author_email="munisisazade@gmail.com",
    description="Microservice simple Starter Flask example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/munisisazade/startmicro",
    scripts=['startmicro/script/start_micro.py'],
    install_requires=["PyInquirer", "virtualenv"],
    extras_require={
        "prompt_toolkit": ["prompt_toolkit == 1.0.14"]
    },
    entry_points={'console_scripts': [
        'microstarter = startmicro.core.management:execute_from_command_line',
    ]},
    platforms=['any'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
