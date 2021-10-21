from setuptools import setup
setup(
    name='libris',
    version='1.1.0',
    description='PDF generator that uses Markdown sources.',
    url='https://github.com/lazy-scrivener-games/libris',
    download_url='https://github.com/lazy-scrivener-games/libris/archive/refs/tags/v1.1.tar.gz',
    author='Chris Muller',
    author_email='chris@lazyscrivenergames.com',
    keywords=[
        'utility',
        'pdf',
        'html',
        'css',
        'markdown',
        'conversion',
        'assembly',
        'book'
    ],
    license='MIT',
    packages=[
        'libris',
        'libris.lib'
    ],
    package_data={
        'libris': ['json-schemas/*'],
    },
    scripts=[
        'scripts/libris'
    ],
    install_requires=[
        'beautifulsoup4 == 4.10.0',
        'idna == 2.6',
        'Jinja2 == 3.0.2',
        'jsonpointer == 1.10',
        'jsonschema == 4.0.0',
        'markdown2 == 2.4.1',
        'watchdog == 2.1.6',
        'weasyprint == 52.5'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Text Processing :: Markup :: Markdown',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
