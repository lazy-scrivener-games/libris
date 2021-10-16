# Enki

Enki is a Markdown to PDF conversion tool that collates multiple Markdown files into a single PDF.

## Requirements

* Generally requires a Linux environment (if you want to get WeasyPrint working under Windows, be my guest).
* Install WeasyPrint using `sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
` or your system's equivalent command
    * See [WeasyPrint's documentation](https://doc.courtbouillon.org/weasyprint/v52.5/install.html) for more details.
* Install BeautifulSoup with `sudo apt-get install python3-bs4` or your system's equivalent command.
* Go into the top-level project folder and install the module using pip3 install .

## Usage

* Create your markdown file sources
* Create any CSS you wish to apply to your Markdown output
* Create a configuration file.
    * More documentation will follow, but for now use `example/example-config.json` as an example configuration file, with the full schema documented in `json-schemas/config-schema.json`.
    * If you set the `$schema` property of your configuration object to point to the `config-schema.json` file you will get auto-complete in any IDE or text editor that support JSON Schema validation.
* Run `enki <CONFIG_FILE_PATH>`
* Check the resulting PDF output!

## Usage

```
usage: enki [-h] [-w] [-v] config_file

Builds a PDF from a JSON configuration file that points to various Markdown source files.

positional arguments:
  config_file    A JSON file that specifies how to build the PDF. View the full docs for details.

optional arguments:
  -h, --help     show this help message and exit
  -w, --watch    Watch the source files and re-compile on changes.
  -v, --verbose  Prints additional logging data, including intermediate HTML.
```
