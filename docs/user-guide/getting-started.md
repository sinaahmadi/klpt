
## Install KLPT

KLPT is implemented in Python and requires basic knowledge on programming and particularly the Python language. Find out more about Python at [https://www.python.org/](https://www.python.org/).

### Requirements

- **Operating system**: macOS / OS X · Linux · Windows (Cygwin, MinGW, Visual
  Studio)
- **Python version**: Python 3.5+ 
- **Package managers**: [pip](https://pypi.org/project/klpt/)
- [`cyhunspell`](https://pypi.org/project/cyhunspell/) >= 2.0.1


### pip

Using pip, KLPT releases are available as source packages and binary wheels. Please make sure that a compatible Python version is installed:

```bash
pip install klpt
```

All the data files including lexicons and morphological rules are also installed with the package. 

Although KLPT is not dependent on any NLP toolkit, there is one important requirement, particularly for the `stem` module. That is [`cyhunspell`](https://pypi.org/project/cyhunspell/) which should be installed with a version >= 2.0.1.


### Import `klpt`
Once the package is installed, you can import the toolkit as follows:

```python
import klpt
```

As a principle, the following parameters are widely used in the toolkit:

- `dialect`: the name of the dialect as `Sorani` or `Kurmanji` (ISO 639-3 code will be also added)
- `script`: the script of your input text as "Arabic" or "Latin"
- `numeral`: the type of the numerals as
	- Arabic [١٢٣٤٥٦٧٨٩٠]
	- Farsi [۱۲۳۴۵۶۷۸۹۰]
	- Latin [1234567890]