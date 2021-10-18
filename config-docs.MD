# Enki Configuration File Documentation

## <a name="overview">Overview</a>

Enki uses a JSON configuration file to allow it to accept a variety of inputs and collate them together into a single PDF document. Configuration files are validated using [JSON Schema](https://json-schema.org/) and must match the schema file found at enki/json-schemas/config-schema.json.

Styles are defined and attached to strings so that they can be easily referenced. This is because a style might encompass multiple CSS stylesheets, and/or might use the templating option we call "decorators."

Decorators are additional HTML files that are rendered as PDF overlays and appended to each generated page of the PDF. They can be assigned their own styling, and we recommend you give them `position: absolute` and use them for things like headers, footers, page numbers, etc. Decorators can interpolate variables (useful for things like chapter names) and have access to the current page number as a built-in variable. More on [decorators](#decorator) below.

## Schema Details

All properties are optional unless otherwise specified.

### <a name="overall-config">Overall Configuration Object</a>

| Property Name | Type | Description |
| --- | --- | --- |
| output | string | REQUIRED. File path to which to write PDF output. |
| sources | array of [source](#source) | REQUIRED. List of markdown files to be included in PDF output. Each source will have an added page break after it. |
| styles | object with values of type [style](#style) | List of style definitions for PDF. |
| defaultStyle | string | Default style to use when a style is not defined for a source. |
| documentWrapperClass | string | If each document needs to be wrapped in a div of a particular CSS class, specify the class name(s) in a string here. If multiple, separate them by spaces. |
| markdownPipe | string | Pipe to run all markdown through. Markdown will be passed to the command given here as stdin and stdout will be sent to the PDF generation code. |

### <a name="source">Source Configuration Object</a>

You can give a source either as a simple string that is the path to the markdown file, or you can use the advanced object format, detailed below. You must include either the source property, the sources property, or the sourceDirectory property.

| Property Name | Type | Description |
| --- | --- | --- |
| source | string | Path to the markdown file to be included. |
| sources | array of strings | Array of markdown file paths to be included. Files will be collated into a single document with no added page breaks and then rendered into the PDF. |
| sourceDirectory | string | Directory of markdown files to be included. Files will be sorted alphabetically and collated together in that order with no added page breaks. |
| style | string | Style to be used for this source object, as defined in the style property of the overall configuration object. If no style is given, the default style will be used. |
| variables | string | Template variables to use for document interpolation. See [decorator](#decorator) for details. |

### <a name="style">Style Configuration Object</a>

You can give a style as a simple string that is the path to the CSS file to use, you can pass an array of strings that are CSS paths, or you can use the advanced object format, detailed below. If you use the advanced object format, you must include either the stylesheet or stylesheets properties and you must also include either the decorator or decorators properties.

| Property Name | Type | Description |
| --- | --- | --- |
| stylesheet | string | Path to CSS stylesheet to be used. |
| stylesheets | array of strings | Paths to CSS stylesheets to be used. |
| decorator | [decorator](#decorator) | Decorator definition for this style. |
| decorators | array of [decorator](#decorator) objects | Decorator definitions for this style. |

### <a name="decorator">Decorator Configuration Object</a>

Decorators, as described in the [Overview](#overview), are additional content applied to each page of a document source individually. You can specify variables in the [variables](#source) property of the source configuration object. Variable are interpolated using double curly brace syntax, i.e. `{{ variableName }}`. There is also a built-in variable for page numbers, which can be interpolated using `{{ pageNumber }}`.

Variables are likely unnecessary in many cases, but one use case for variables is to apply a similar footer for many sections of the document, but put a chapter title in that footer that is specific to each section defined by a source object.

| Property Name | Type | Description |
| --- | --- | --- |
| template | string | REQUIRED. Path to the HTML template for the decorator. |
| stylesheet | string | REQUIRED. Path to the CSS stylesheet for the decorator. |
| evenStylesheet | string | Path to an added CSS stylesheet to be applied only to even pages. |
| oddStylesheet | string | Path to an added CSS stylesheet to be applied only to odd pages. |
