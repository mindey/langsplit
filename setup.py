from setuptools import find_packages, setup

setup(
    name='langsplit',
    version='0.1.9',
    description='Splits text by separator, and limited length language names, combines split text chunks into OrderedDict, or combines back to text. Supposed for extending markdown with tags for human languages.',
    url='https://github.com/mindey/langsplit',
    author='Mindey',
    author_email='mindey@qq.com',
    license='UNLICENSE',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=["langdetect"],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
