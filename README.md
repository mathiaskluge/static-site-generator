# Static Site Generator

Purely educational, rudimentary [static site generator](https://en.wikipedia.org/wiki/Static_site_generator) written in [Python](https://www.python.org/).

* Shell and filesystem -> [shutil](https://docs.python.org/3/library/shutil.html) and [pathlib](https://docs.python.org/3/library/pathlib.html)
* Regex -> [re](https://docs.python.org/3/library/re.html)
* Resiliance -> md to HTML...

## Basic usage

To build the site, `cd` into your project directory and run:

```bash
# within top-level project directory
./main.sh
```

The script will build your site and serve it using a minimal HTTP server. The site is build from the `static` and `content` directories and files are published into the `public` directory.

## Capabilities & Limitations

It can handle following block markdown syntaxt:

* Headings (`#` - `######`)
* Paragraphs (blank line)
* Code Blocks (```)
* Quote (`>`)
* Unordered List (`*` or `-`)
* Ordered Lists (`1.` - `n.`)

And following inline markdown syntax:

* Bold  (`**`)
* Italic (`*`)
* Code (`)
* Links (`[label](url)`)
* Images (`![alt](src)`)

It cannot yet handle nested inline syntax yet:

* Bold and Italic
* Nested Blockquotes
* ... and probably way more I don't know about


