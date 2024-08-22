# Static Site Generator

Purely educational, rudimentary [static site generator](https://en.wikipedia.org/wiki/Static_site_generator) written in [Python](https://www.python.org/). It uses:

* [shutil](https://docs.python.org/3/library/shutil.html) and [pathlib](https://docs.python.org/3/library/pathlib.html) for filesystem operations
* [re](https://docs.python.org/3/library/re.html) (Regex) for Markdown to HTML processing

## Basic usage

To build the site, `cd` into your project directory and run:

```bash
./main.sh
```

The script will build your site and serve it using a minimal HTTP server. The site is build from the `/static` and `/content` directories and files are published into the `/public` directory.

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

It cannot handle nested inline syntax yet:

* Bold and Italic
* Nested Blockquotes
* ... and probably way more I don't know about, yet


