# Modified by the tkmacos fork; see NOTICE for details.
import ast
from pathlib import Path

from setuptools import setup, find_packages


def get_package_metadata():
    """Read package metadata without importing the package (or tkinter)."""
    init_path = Path(__file__).parent / 'tkmacos' / '__init__.py'
    module = ast.parse(init_path.read_text(encoding='utf-8'))
    metadata = {}
    for node in module.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id in ('__version__', '__author__'):
                metadata[target.id] = ast.literal_eval(node.value)
    return metadata


PACKAGE_METADATA = get_package_metadata()


def get_long_description(path):
    """Opens and fetches text of long description file."""
    with open(path, 'r') as f:
        text = f.read()
    return text


attrs = dict(
    name='tkmacos',
    version=PACKAGE_METADATA['__version__'],
    packages=find_packages(exclude=('test', 'test.*')),
    long_description=get_long_description('README.md'),
    description='TkMacos is a Python library extension to Tkinter with customizable widgets.',
    long_description_content_type='text/markdown',
    author=PACKAGE_METADATA['__author__'],
    license='Apache',
    license_files=['LICENSE', 'NOTICE'],
    python_requires='>=3',
    install_requires=[
        'colour',
    ],
    keywords=[
        'tkinter',
        'macos',
        'variable',
        'widgets',
        'colorscale',
        'tk',
        'color',
        'button',
        'circlebutton',
        'marquee',
        'tkinter-widgets',
        'tkinter-scrollableframe',
        'scrollableframe',
    ],
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'License :: OSI Approved :: Apache Software License',
    ],
    include_package_data=True,
)

setup(**attrs)
