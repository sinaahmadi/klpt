# Kurdish Language Processing Toolkit

<p align="center" width="100%">
    <img width="33%" src="https://raw.githubusercontent.com/sinaahmadi/klpt/master/docs/img/KLPT_logo.png"> 
</p>

<p align="center">
    <a href="">
        <img alt="Build" src="https://badges.frapsoft.com/os/v1/open-source.png?v=103">
    </a>
    <a href="https://github.com/sinaahmadi/KLPT/blob/master/license">
        <img alt="GitHub" src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-blue">
    </a>
    <a href="">
        <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/klpt">
    </a>
    <a href="https://sinaahmadi.github.io/klpt/">
        <img alt="Documentation" src="https://img.shields.io/website?down_color=green&down_message=online&up_color=orange&url=https%3A%2F%2Fsinaahmadi.github.io%2FKLPT%2F">
    </a>
    <a href="https://gitter.im/KurdishNLP/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge">
      <img alt="Documentation" src="https://badges.gitter.im/KurdishNLP/community.svg">
    </a>
    <a href="https://badge.fury.io/py/klpt">
        <img src="https://badge.fury.io/py/klpt.svg" alt="PyPI version" height="18">
    </a>
</p>


### Welcome / *Hûn bi xêr hatin* / بە خێر بێن! 🙂

Kurdish Language Processing Toolkit--KLPT is a [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) (NLP) toolkit in Python for the [Kurdish language](https://en.wikipedia.org/wiki/Kurdish_languages). The current version comes with four core modules, namely `preprocess`, `stem`, `transliterate` and `tokenize` and addresses basic language processing tasks such as text preprocessing, stemming, tokenization, spell-checking and morphological analysis for the [Sorani](https://en.wikipedia.org/wiki/Sorani) and the [Kurmanji](https://en.wikipedia.org/wiki/Kurmanji) dialects of Kurdish.

---
#### Latest update on January 6th, 2022 🎉

In the latest version, the followings are done:

- It is possible to **stem** and **lemmatize** words of all part-of-speech. Up to version 0.1.4, stemming was only possible for verbs.
- For stemming unknown words, a rule-based approach is provided.
- When using the morphological analyzer (in [stem module](https://github.com/sinaahmadi/klpt/blob/master/klpt/stem.py)), prefixes and suffixes are returned separately. These used to be previously merged.
- Stopwords are now available for both Sorani and Kurmanji.

---

## Install KLPT

<!--For detailed installation instructions, see the [documentation]().-->

- **Operating system**: macOS / OS X · Linux · Windows (Cygwin, MinGW, Visual
  Studio)
- **Python version**: Python 3.5+ 
- **Package managers**: [pip](https://pypi.org/project/klpt/)

[pip]: https://pypi.org/project/spacy/
[conda]: https://anaconda.org/conda-forge/spacy

### pip

Using pip, KLPT releases are available as source packages and binary wheels. Please make sure that a compatible Python version is installed:

```bash
pip install klpt
```

All the data files including lexicons and morphological rules are also installed with the package. 

Although KLPT is not dependent on any NLP toolkit, there is one important requirement, particularly for the `stem` module. That is [`cyhunspell`](https://pypi.org/project/cyhunspell/) which should be installed with a version >= 2.0.1.

### About this version

Please note that KLPT is under development and some of the functionalities will appear in the future versions. You can find out regarding the progress of each task at the [Projects](https://github.com/sinaahmadi/KLPT/projects) section. In the current version, the following tasks are included:

<table>
<thead>
  <tr>
    <th>Modules<br></th>
    <th>Tasks</th>
    <th>Sorani (ckb)</th>
    <th>Kurmanji (kmr)</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4"><code>preprocess</code></td>
    <td>normalization</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>standardization</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>unification of numerals</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>stopwords</td>
    <td>&#10003; (v0.1.4)</td>
    <td>&#10003; (v0.1.4)</td>
  </tr>
  <tr>
    <td rowspan="4"><code>tokenize</code></td>
    <td>word tokenization<br></td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>MWE tokenization<br></td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>sentence tokenization</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>part-of-speech tagging</td>
    <td>&#x2717;</td>
    <td>&#x2717;</td>
  </tr>
  <tr>
    <td rowspan="4"><code>transliterate</code></td>
    <td>Arabic to Latin</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>Latin to Arabic</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>Detection of u/w and î/y</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.0)</td>
  </tr>
  <tr>
    <td>Detection of Bizroke ( <i>i</i> )</td>
    <td>&#x2717;</td>
    <td>&#x2717;</td>
  </tr>
  <tr>
    <td rowspan="5"><code>stem</code></td>
    <td>morphological analysis</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#10003; (v0.1.1)</td>
  </tr>
  <tr>
    <td>morphological generation</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#x2717;</td>
  </tr>
  <tr>
    <td>stemming</td>
    <td>&#10003; (v.0.1.5) 🆕</td>
    <td>&#x2717;</td>
  </tr>
  <tr>
    <td>lemmatization</td>
    <td>&#10003; (v.0.1.5) 🆕</td>
    <td>&#x2717;</td>
  </tr>
  <tr>
    <td>spell error detection and correction</td>
    <td>&#10003; (v0.1.0)</td>
    <td>&#x2717;</td>
  </tr>
</tbody>
</table>


## Basic usage

Once the package is installed, you can import the toolkit as follows:

```python
import klpt
```

In the following, a few examples are provided to work with various modules. Almost all the classes have three arguments in common:

- `dialect`: the name of the dialect as `Sorani` or `Kurmanji` (ISO 639-3 code will be also added)
- `script`: the script of your input text as "Arabic" or "Latin"
- `numeral`: the type of the numerals as
	- Arabic [١٢٣٤٥٦٧٨٩٠]
	- Farsi [۱۲۳۴۵۶۷۸۹۰]
	- Latin [1234567890]

### Preprocess

This module deals with normalizing scripts and orthographies by using writing conventions based on dialects and scripts. The goal is not to correct the orthography but to normalize the text in terms of the encoding and common writing rules. The input encoding should be in UTF-8 only. To this end, three functions are provided as follows:

- `normalize`: deals with different encodings and unifies characters based on dialects and scripts
- `standardize`: given a normalized text, it returns standardized text based on the Kurdish orthographies following recommendations for [Kurmanji](https://books.google.ie/books?id=Z7lDnwEACAAJ) and [Sorani](http://yageyziman.com/Renusi_Kurdi.htm)
- `unify_numerals`: conversion of the various types of numerals used in Kurdish texts

It is recommended that the output of this module be used as the input of subsequent tasks in an NLP pipeline.

```python
>>> from klpt.preprocess import Preprocess

>>> preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")
>>> preprocessor_ckb.normalize("لە ســـاڵەکانی ١٩٥٠دا")
'لە ساڵەکانی 1950دا'
>>> preprocessor_ckb.standardize("راستە لەو ووڵاتەدا")
'ڕاستە لەو وڵاتەدا'
>>> preprocessor_ckb.unify_numerals("٢٠٢٠")
'2020'

>>> preprocessor_kmr = Preprocess("Kurmanji", "Latin")
>>> preprocessor_kmr.standardize("di sala 2018-an")
'di sala 2018an'
>>> preprocessor_kmr.standardize("hêviya")
'hêvîya'
```

In addition, it is possible to remove Kurdish [stopwords](https://en.wikipedia.org/wiki/Stop_word) using the `stopwords` variable. You can define a function like the following to do so:

```python
from klpt.preprocess import Preprocess

def remove_stopwords(text, dialect, script):
    p = Preprocess(dialect, script)
    return [token for token in text.split() if token not in p.stopwords]
```

### Tokenization

This module focuses on the tokenization of both Kurmanji and Sorani dialects of Kurdish with the following functions:

- `word_tokenize`: tokenization of texts into tokens (both [multi-word expressions](https://aclweb.org/aclwiki/Multiword_Expressions) and single-word tokens).
- `mwe_tokenize`: tokenization of texts by only taking compound forms into account
- `sent_tokenize`: tokenization of texts into sentences

This module is based on the [Kurdish tokenization project](https://github.com/sinaahmadi/KurdishTokenization). It is recommended that the output of this module be used as the input of the `Stem` module. 

```python
>>> from klpt.tokenize import Tokenize

>>> tokenizer = Tokenize("Kurmanji", "Latin")
>>> tokenizer.word_tokenize("ji bo fortê xwe avêtin")
['▁ji▁', 'bo', '▁▁fortê‒xwe‒avêtin▁▁']
>>> tokenizer.mwe_tokenize("bi serokê hukûmeta herêma Kurdistanê Prof. Salih re saz kir.")
'bi serokê hukûmeta herêma Kurdistanê Prof . Salih re saz kir .'

>>> tokenizer_ckb = Tokenize("Sorani", "Arabic")
>>> tokenizer_ckb.word_tokenize("بە هەموو هەمووانەوە ڕێک کەوتن")
['▁بە▁', '▁هەموو▁', 'هەمووانەوە', '▁▁ڕێک‒کەوتن▁▁']
```

### Transliteration

This module aims at transliterating one script of Kurdish into another one. Currently, only the Latin-based and the Arabic-based scripts of Sorani and Kurmanji are supported. The main function in this module is `transliterate()` which also takes care of detecting the correct form of double-usage graphemes, namely و ↔ w/u and ی ↔ î/y. In some specific occasions, it can also predict the placement of the missing *i* (also known as *Bizroke/بزرۆکە*).

The module is based on the [Kurdish transliteration project](https://github.com/sinaahmadi/wergor).

```python
>>> from klpt.transliterate import Transliterate
>>> transliterate = Transliterate("Kurmanji", "Latin", target_script="Arabic")
>>> transliterate.transliterate("rojhilata navîn")
'رۆژهلاتا ناڤین'

>>> transliterate_ckb = Transliterate("Sorani", "Arabic", target_script="Latin")
>>> transliterate_ckb.transliterate("لە وڵاتەکانی دیکەدا")
'le wiłatekanî dîkeda'
```

### Stem

The Stem module deals with various tasks, mainly through the following functions:
- `check_spelling`: spell error detection
- `correct_spelling`: spell error correction
- `analyze`: morphological analysis
- `stem`: stemming, e.g. "بڕ" → "بڕاوە"
- `lemmatize`: lemmatization, e.g. "بردن" → "بردمنەوە"

The module is based on the [Kurdish Hunspell project](https://github.com/sinaahmadi/KurdishHunspell) for Sorani and the [Apertium project](https://github.com/apertium/apertium-kmr) for Kurmanji. Please note that this module is currently getting further completed and we are aware of its current shortcomings.

```python
>>> from klpt.stem import Stem
>>> stemmer = Stem("Sorani", "Arabic")
>>> stemmer.check_spelling("سوتاندبووت")
False
>>> stemmer.correct_spelling("سوتاندبووت")
(False, ['ستاندبووت', 'سووتاندبووت', 'سووڕاندبووت', 'ڕووتاندبووت', 'فەوتاندبووت', 'بووژاندبووت'])
>>> stemmer.analyze("دیتبامن")
[{'pos': ['verb'], 'description': 'past_stem_transitive_active', 'stem': 'دی', 'lemma': ['دیتن'], 'base': 'دیت', 'prefixes': '', 'suffixes': 'بامن'}]
>>> stemmer.stem("دەچینەوە")
['چ']
>>> stemmer.stem("گورەکە", mark_unknown=True) # گوڵەکە in Hewlêrî dialect
['_گور_']
>>> stemmer.lemmatize("گوڵەکانم"))
['گوڵ', 'گوڵە']

>>> stemmer = Stem("Kurmanji", "Latin")
>>> stemmer.analyze("dibêjim")
[{'base': 'gotin', 'description': 'vblex_tv_pri_p1_sg', 'pos': '', 'terminal_suffix': '', 'formation': ''}]
```

📖 **Please note that a more complete documentation of the toolkit is available at [https://sinaahmadi.github.io/klpt/](https://sinaahmadi.github.io/klpt/)**.

## Become a sponsor 

Please consider donating to the project. Data annotation and resource creation requires tremendous amount of time and linguistic expertise. Even a trivial donation will make a difference. You can do so by [becoming a sponsor](https://github.com/sponsors/sinaahmadi) to accompany me in this journey and help the Kurdish language have a better place within other natural languages on the Web. Depending on your support,

- You can be an official sponsor
- You will get a GitHub sponsor badge on your profile
- If you have any questions, I will focus on it
- If you want, I will add your name or company logo on the front page of your preferred project
- Your contribution will be acknowledged in one of my future papers in a field of your choice

*And, thanks for those who have already sponsored this project. More significant achievements will be made thanks to you!*

## Contribute

Are you interested in this project? Each task is addressed individually. Please check the following repositories to find which one you are more interested in:

- [Kurdish tokenization](https://github.com/sinaahmadi/KurdishTokenization)
- [Kurdish Hunspell](https://github.com/sinaahmadi/KurdishHunspell)
- [Kurdish transliteration](https://github.com/sinaahmadi/wergor)

In addition, our main objective is to extend the current toolkit to include more tasks, particularly part-of-speech tagging, named-entity recognition and syntactic analysis. Further instructions are provided at [https://sinaahmadi.github.io/klpt/about/contributing/](https://sinaahmadi.github.io/klpt/about/contributing/). You can also join us on [Gitter](https://gitter.im/KurdishNLP/community).

Don't forget, **open-source is fun!** 😊

## Requirements
- Python >=3.6
- [`cyhunspell`](https://pypi.org/project/cyhunspell/) >= 2.0.1

## Cite this project
Please consider citing [this paper](https://sinaahmadi.github.io/docs/articles/ahmadi2020klpt.pdf), if you use any part of the data or the tool ([`bib` file](https://sinaahmadi.github.io/bibliography/ahmadi2020klpt.txt)):

	@inproceedings{ahmadi2020klpt,
	    title = "{KLPT--Kurdish Language Processing Toolkit}",
	    author = "Ahmadi, Sina",
	    booktitle = "Proceedings of the second Workshop for {NLP} Open Source Software ({NLP}-{OSS})",
	    month = nov,
	    year = "2020",
	    publisher = "Association for Computational Linguistics"
	}


## License 
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Kurdish Language Processing Toolkit</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/sinaahmadi/klpt" property="cc:attributionName" rel="cc:attributionURL">Sina Ahmadi</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a> which means:

- **You are free to share**, copy and redistribute the material in any medium or format and also adapt, remix, transform, and build upon the material
for any purpose, **even commercially**. 
- **You must give appropriate credit**, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- If you remix, transform, or build upon the material, **you must distribute your contributions under the same license as the original**. 



