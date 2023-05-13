# pyline

Python one liner generator.

## Usage

Input can be stdin or a file, output can be stdout or a file.

```bash
$ echo "print('Hello, world')" | python3 pyline.py 2>/dev/null
import base64;exec(base64.b64decode("cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg=="))
```

```bash
$ echo "print('Hello, world')" | python3 pyline.py 2>/dev/null | python3
Hello, world
```
