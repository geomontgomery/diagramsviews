# diagramsviews

diagramsviews is a python script that will append views to a DIAGRAMS Configuration.xml based on info from a P&ID Database.tbl.

## Installation

Clone the repo,
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Usage

Replace Configuration.xml and Database.tbl with your files in the same directory as main.py

```cmd
python main.py
```
The Configuration.xml will be enhanced and sent to .\output\Configuration.xml, take this and copy it to your Diagrams support directory.

## License
[MIT](https://choosealicense.com/licenses/mit/)