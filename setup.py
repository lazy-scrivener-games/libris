from setuptools import setup
setup(
    name='enki',
    version='1.0.0',
    description='PDF generator that uses Markdown sources.',
    url='https://github.com/lazy-scrivener-games/enki-dnd-style',
    author='Chris Muller',
    author_email='chris@lazyscrivenergames.com',
    license='MIT',
    packages=['enki'],
    install_requires=[
        'beautifulsoup4 == 4.10.0',
        'Jinja2 == 3.0.2',
        'jsonschema == 4.0.0',
        'markdown2 == 2.4.1',
        'watchdog == 2.1.6',
        'weasyprint == 52.5'
    ]
)
