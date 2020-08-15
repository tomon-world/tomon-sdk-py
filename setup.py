import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tomon_sdk",  # Replace with your own username
    version="0.1.5",
    author="Tomon Team",
    author_email="qiang.l.x@gmail.com",
    description="A simple development kit for Tomon bot.",
    url="https://github.com/tomon-world/tomon-sdk-py",
    packages=setuptools.find_packages(),
    keywords=['TOMON'],
    install_requires=[            # I get to this in a second
        'aiohttp',
        'node-events',
        'ws4py'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
