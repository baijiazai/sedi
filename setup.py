import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sedi",
    version="0.2.0",
    author="baijiazai",
    author_email="1052065965@qq.com",
    description="Search engines download images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baijiazai/sedi",
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["requests", "tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["sedi = sedi.cmdline:execute"]
    }
)
