from setuptools import setup, find_packages

setup(
    name='clld-phylogeny-plugin',
    version='1.4.0',
    description='clld-phylogeny-plugin',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Robert Forkel',
    author_email='forkel@shh.mpg.de',
    url='https://github.com/clld/clld-phylogeny-plugin',
    keywords='web pyramid pylons',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'attrs>=18.1',
        'clld>=4.0.3',
        'sqlalchemy',
        'zope.interface',
        'ete3',
    ],
    extras_require={
        'dev': [
            'flake8',
            'wheel',
            'twine'],
        'test': [
            'pytest-clld',
            'pytest>=3.6',
            'pytest-mock',
            'mock',
            'coverage>=4.2',
            'pytest-cov',
            'webtest',
        ],
    },
    license="Apache 2.0",
)
