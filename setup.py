# KSYLO by Alexander Abraham
# licensed under the MIT license
from setuptools import setup, find_packages
import pathlib
import os
from ksylo.page import version
from Cython.Build import cythonize
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.markdown').read_text(encoding='utf-8')
EXCLUDE_FILES = []
def get_ext_paths(root_dir, exclude_files):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if os.path.splitext(filename)[1] != '.py':
                continue
            file_path = os.path.join(root, filename)
            if file_path in exclude_files:
                continue
            paths.append(file_path)
    return paths
setup(
    name='Ksylo',
    version=version(),
    description='A compiler for the Hex language. Hex by Alexander Abraham',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RealAAbraham/HexLang',
    author='Alexander Abraham',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=['pip', 'setuptools', 'wheel', 'colorama', 'cython', 'requests'],
    ext_modules=cythonize(
        get_ext_paths('ksylo', EXCLUDE_FILES),
        compiler_directives={'language_level': 3}
    ),
    entry_points={
        'console_scripts': [
            'ksite=ksylo.ksite:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/RealAAbraham/Ksylo/issues',
        'Source': 'https://github.com/RealAAbraham/Ksylo',
    },
)
