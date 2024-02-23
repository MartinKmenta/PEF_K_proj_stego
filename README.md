# PEF_K_proj_stego

python 3 and pip required

use following command to install dependencies:
`pip install -r requirements.txt`

usage:
`python main.py -h`

```
usage: main.py [-h] [-m MESSAGE] [-e] [-d] [-i IMAGE] [-o OUTPUT] [-t] [-g]

options:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        Message
  -e, --encode          Encode message
  -d, --decode          Decode message
  -i IMAGE, --image IMAGE
                        Image path
  -o OUTPUT, --output OUTPUT
                        Output path
  -t, --test            Run tests
  -g, --gui             Run GUI
```

usage examples:

- show help
  - `python main.py -h`
- run test
  - `python main.py -t`
- open gui
  - `python main.py -g`
- encode text to bytes
  - `python main.py -e -m "Hello, World!"`
- decode text from binary
  - `python main.py -d -m 0011010000110010`
- encode to image
  - `python main.py -e -m "Hello, World!" -i images/dalle_duck.png -o images/script_out.png`
- decode from image
  - `python main.py -d -m "Hello, World!" -i images/encoded_image.png`
