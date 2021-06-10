from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'scoping',
    version = '0.1.0',
    author = 'l74d',
    author_email = 'l.d.code@outlook.com',
    description = 'Probably the best way to simulate block scopes in Python.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/l74d/scoping',
    project_urls = {
        "Bug Tracker" : "https://github.com/l74d/scoping/issues"
    },
    classifiers =[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "."},
    packages = {},
    python_requires=">=3.6",
)    


