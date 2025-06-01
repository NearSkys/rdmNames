from setuptools import setup, find_packages

setup(
    name="rdmNames",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        'rdmNames': ['data/*.first', 'data/*.last'],
    },
    python_requires='>=3.7',
    install_requires=[],
    author="Seu Nome",
    author_email="seu.email@example.com",
    description="Uma biblioteca otimizada para geração de nomes aleatórios",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/seu-usuario/rdmNames",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
