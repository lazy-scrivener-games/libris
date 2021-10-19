# Enki

Enki is a Markdown to PDF conversion tool that collates multiple Markdown files into a single PDF.

## Requirements

* Linux or Windows with [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install)
* If anyone figures out how to get Weasyprint working with Windows, that'd be great. Otherwise, the answer is WSL.

## Setup

* Run `sudo apt update`
* Install WeasyPrint
    * On Debian/Ubuntu, run `sudo apt install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`.
    * For other platforms, see [WeasyPrint's documentation](https://doc.courtbouillon.org/weasyprint/v52.5/install.html) for more details.
* Install BeautifulSoup
    * On Debian/Ubuntu, run `sudo apt install python3-bs4`.
* Go into the top-level project folder and install the module using pip3 install .

## Basic Usage

* Create your markdown file sources
* Create any CSS you wish to apply to your Markdown output
* Create a configuration file.
    * See [config documentation](./config-docs.MD) for details.
    * If you set the `$schema` property of your configuration object to point to the `enki/json-schemas/config-schema.json` file you will get auto-complete in any IDE or text editor that supports JSON Schema validation.
* Run `enki <CONFIG_FILE_PATH>`
* Check the resulting PDF output!

## Detailed Documentation

* For full config documentation see [config documentation](./config-docs.MD).

## Known Issues

* The watch feature will not work on WSL due to how WSL interacts with the mounted Windows file system (it can't access low-level Windows file event hooks). To get a similar effect on Windows, I suggest using [watchmedo](https://github.com/gorakhargosh/watchdog) and writing a batch file for your specific use case that runs the enki command in WSL.

## Command Options

```
usage: enki [-h] [-w] [-v] config_file

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

| Path              | Description                                   |
| ----------------- | --------------------------------------------- |
| enki              | Enki program package folder                   |
| enki/json-schemas | JSON schemas to validate configuration files  |
| enki/lib          | Supporting functions and classes              |
| enki/example      | Example markdown, CSS, and configuration file |
| enki/scripts      | Shell script installed on running pip install |

### Folder Structure With Files

| Path                                      | Description                                               |
| ----------------------------------------- | --------------------------------------------------------- |
| .gitattributes                            | Git attributes file                                       |
| .gitignore                                | Git ignore file                                           |
| .pylintrc                                 | Linting rules                                             |
| config-docs.MD                            | Documentation for config files                            |
| README.MD                                 | Main project README                                       |
| requirements.txt                          | Python requirements list                                  |
| setup.py                                  | Package setup file for pip                                |
| enki (folder)                             | Enki program package folder                               |
| enki/\_\_init\_\_.py                      | Module init file                                          |
| enki/\_\_main\_\_.py                      | Main program entry point                                  |
| enki/json-schemas (folder)                | JSON schemas to validate configuration files              |
| enki/json-schemas/config-schema.json      | JSON schema for overall configuration file                |
| enki/json-schemas/decorator-schema.json   | JSON schema for decorator data                            |
| enki/json-schemas/source-schema.json      | JSON schema for individual markdown source data           |
| enki/json-schemas/sources-schema.json     | JSON schema for markdown sources list                     |
| enki/json-schemas/style-schema.json       | JSON schema for individual CSS style                      |
| enki/json-schemas/styles-schema.json      | JSON schema for CSS styles list                           |
| enki/lib (folder)                         | Supporting functions and classes                          |
| enki/lib/constants.py                     | Program constants                                         |
| enki/lib/data_extractors.py               | Functions that extract data from files                    |
| enki/lib/pdf_builder.py                   | Functions that construct the PDF output                   |
| enki/lib/watch.py                         | Functions that support the file watch feature             |
| enki/lib/\_\_init\_\_.py                  | Module init file                                          |
| example (folder)                          | Example markdown, CSS, and configuration file             |
| example/advanced-style.css                | Example CSS stylesheet                                    |
| example/basic-style.css                   | Example CSS stylesheet                                    |
| example/chapter1.md                       | Example markdown                                          |
| example/chapter2.md                       | Example markdown                                          |
| example/chapter3.md                       | Example markdown                                          |
| example/example-config.json               | Example enki configuration file                           |
| scripts (folder)                          | Folder for shell script installed on running pip install  |
| scripts/enki                              | Shell script installed on running pip install             |
