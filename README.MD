# Libris

Libris is a Markdown to PDF conversion tool that collates multiple Markdown files into a single PDF.

## Requirements

-   Linux or Windows with [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install)
-   If anyone figures out how to get Weasyprint working with Windows, that'd be great. Otherwise, the answer is WSL.
-   Python 3.6+

## Debian/Linux Setup

-   Run `sudo apt update`
-   Run `sudo apt install python3-pip`
-   Run `sudo apt install libpangocairo-1.0-0
-   Install the module using `pip install libris`

## Basic Usage

-   Create your markdown file sources
-   Create any CSS you wish to apply to your Markdown output
-   Create a configuration file.
    -   See [config documentation](./config-docs.MD) for details.
    -   If you set the `$schema` property of your configuration object to point to `https://github.com/lazy-scrivener-games/libris/json-schemas/config-schema.json`, you will get auto-complete in any IDE or text editor that supports JSON Schema validation.
-   Run `libris <CONFIG_FILE_PATH>`
-   Check the resulting PDF output!

## Detailed Documentation

-   For full config documentation see [config documentation](./config-docs.MD).

## Docker Setup

-   Have Docker installed
-   Run `docker build -t libris .`
-   Run `docker run -it --name libris libris`

## Known Issues

-   The watch feature will not work on WSL due to how WSL interacts with the mounted Windows file system (it can't access low-level Windows file event hooks). To get a similar effect on Windows, I suggest using [watchmedo](https://github.com/gorakhargosh/watchdog) and writing a batch file for your specific use case that runs the libris command in WSL.

## Command Options

```
usage: libris [-h] [-w] [-v] config_file

Builds a PDF from a JSON configuration file that points to various Markdown source files.

positional arguments:
  config_file    A JSON file that specifies how to build the PDF. View the full docs for details.

optional arguments:
  -h, --help          show this help message and exit
  -w, --watch         Watch the source files and re-compile on changes.
  -v, --verbose       Prints additional logging data, including intermediate HTML.
  -n, --no-validation Skips JSON validation. Use this if you are getting URL resolution errors.
```

## Folder Structure

| Path                | Description                                   |
| ------------------- | --------------------------------------------- |
| libris              | Libris program package folder                 |
| libris/json-schemas | JSON schemas to validate configuration files  |
| libris/lib          | Supporting functions and classes              |
| libris/example      | Example markdown, CSS, and configuration file |
| libris/scripts      | Shell script installed on running pip install |

### Folder Structure With Files

| Path                                      | Description                                              |
| ----------------------------------------- | -------------------------------------------------------- |
| .gitattributes                            | Git attributes file                                      |
| .gitignore                                | Git ignore file                                          |
| .pylintrc                                 | Linting rules                                            |
| config-docs.MD                            | Documentation for config files                           |
| README.MD                                 | Main project README                                      |
| requirements.txt                          | Python requirements list                                 |
| setup.py                                  | Package setup file for pip                               |
| libris (folder)                           | Libris program package folder                            |
| libris/\_\_init\_\_.py                    | Module init file                                         |
| libris/\_\_main\_\_.py                    | Main program entry point                                 |
| libris/json-schemas (folder)              | JSON schemas to validate configuration files             |
| libris/json-schemas/config-schema.json    | JSON schema for overall configuration file               |
| libris/json-schemas/decorator-schema.json | JSON schema for decorator data                           |
| libris/json-schemas/source-schema.json    | JSON schema for individual markdown source data          |
| libris/json-schemas/sources-schema.json   | JSON schema for markdown sources list                    |
| libris/json-schemas/style-schema.json     | JSON schema for individual CSS style                     |
| libris/json-schemas/styles-schema.json    | JSON schema for CSS styles list                          |
| libris/lib (folder)                       | Supporting functions and classes                         |
| libris/lib/constants.py                   | Program constants                                        |
| libris/lib/data_extractors.py             | Functions that extract data from files                   |
| libris/lib/pdf_builder.py                 | Functions that construct the PDF output                  |
| libris/lib/watch.py                       | Functions that support the file watch feature            |
| libris/lib/\_\_init\_\_.py                | Module init file                                         |
| example (folder)                          | Example markdown, CSS, and configuration file            |
| example/advanced-style.css                | Example CSS stylesheet                                   |
| example/basic-style.css                   | Example CSS stylesheet                                   |
| example/chapter1.md                       | Example markdown                                         |
| example/chapter2.md                       | Example markdown                                         |
| example/chapter3.md                       | Example markdown                                         |
| example/example-config.json               | Example libris configuration file                        |
| scripts (folder)                          | Folder for shell script installed on running pip install |
| scripts/libris                            | Shell script installed on running pip install            |

## Releasing

-   `python3 -m build`
-   `python3 -m twine upload dist/*`
