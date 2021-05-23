# sedi

Search engines download images

Compatibility
-------------

only supports Python 3.6 and above.

Basic Usage
-----------

Install with pip:

```bash
pip install sedi
```

Usage:

```bash
# Help
> sedi --help

Usage: sedi [OPTIONS] KEYWORD

Options:
  -s, --save_path TEXT  Picture save path (relative path or absolute path)
                        [./img].
  -e, --engine TEXT     Search engine ([baidu], sogou, 360).
  --help                Show this message and exit.

# Example
> sedi cat img

Searching: 1594it [00:08, 177.96it/s]
[baidu] Downloading: 100%|██████████████████████████████| 1594/1594 [00:22<00:00, 71.08it/s]

# Switch engine
> sedi cat -e sogou

# Change save path
> sedi cat -s ./baidu
```

License
-------

insure is released under the MIT License. See the bundled `LICENSE` file for details.