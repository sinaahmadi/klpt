<p align="center" width="100%">
    <img width="33%" src="https://raw.githubusercontent.com/sinaahmadi/klpt/master/docs/img/KLPT_logo.png"> 
</p>

### **Welcome / *Hûn bi xêr hatin* / بە خێر بێن!** 🙂


### Introduction

[Language technology](https://en.wikipedia.org/wiki/Language_technology) is an increasingly important field in our information era which is dependent on our knowledge of the human language and computational methods to process it. Unlike the latter which undergoes constant progress with new methods and more efficient techniques being invented, the processability of human languages does not evolve with the same pace. This is particularly the case of languages with scarce resources and limited grammars, also known as *less-resourced languages*.

Despite a plethora of performant tools and specific frameworks for [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) (NLP), such as [NLTK](https://www.nltk.org/), [Stanza](https://stanfordnlp.github.io/stanza/) and [spaCy](https://github.com/explosion/spaCy), the progress with respect to less-resourced languages is often hindered by not only the lack of basic tools and resources but also the accessibility of the previous studies under an open-source licence. This is particularly the case of Kurdish.

### Kurdish Language

Kurdish is a less-resourced Indo-European language which is spoken by 20-30 million speakers in the Kurdish regions of Turkey, Iraq, Iran and Syria and also, among the Kurdish diaspora around the world. It is mainly spoken in four dialects (also referred to as languages):

- [Northern Kurdish](https://en.wikipedia.org/wiki/Kurmanji) (or Kurmanji) `kmr`
- [Central Kurdish](https://en.wikipedia.org/wiki/Sorani) (or Sorani) `ckb`
- [Southern Kurdish](https://en.wikipedia.org/wiki/Southern_Kurdish) `sdh`
- [Laki](https://en.wikipedia.org/wiki/Laki_language) `lki`

Kurdish has been historically written in various scripts, namely Cyrillic, Armenian, Latin and Arabic among which the latter two are still widely in use. Efforts in standardization of the Kurdish alphabets and orthographies have not succeeded to be globally followed by all Kurdish speakers in all regions. As such, the Kurmanji dialect is mostly written in the Latin-based script while the Sorani, Southern Kurdish and Laki are mostly written in the Arabic-based script.

### KLPT - The Kurdish Language Processing Toolkit

KLPT - the Kurdish Language Processing Toolkit is an NLP toolkit for the [Kurdish language](https://en.wikipedia.org/wiki/Kurdish_languages). The current version (0.1) comes with four core modules, namely `preprocess`, `stem`, `transliterate` and `tokenize`, and addresses basic language processing tasks such as text preprocessing, stemming, tokenziation, spell error detection and correction, and morphological analysis for the [Sorani](https://en.wikipedia.org/wiki/Sorani) and [Kurmanji](https://en.wikipedia.org/wiki/Kurmanji) dialects of Kurdish. More importantly, **it is an open-source project**!

To find out more about how to use the tool, please check the "User Guide" section of this website. 

### Cite this project

Please consider citing [this paper](https://sinaahmadi.github.io/docs/articles/ahmadi2020klpt.pdf), if you use any part of the data or the tool ([`bib` file](https://sinaahmadi.github.io/bibliography/ahmadi2020klpt.txt)):

	@inproceedings{ahmadi2020klpt,
	    title = "{KLPT} {--} {K}urdish Language Processing Toolkit",
	    author = "Ahmadi, Sina",
	    booktitle = "Proceedings of Second Workshop for NLP Open Source Software (NLP-OSS)",
	    month = nov,
	    year = "2020",
	    address = "Online",
	    publisher = "Association for Computational Linguistics",
	    url = "https://www.aclweb.org/anthology/2020.nlposs-1.11",
	    pages = "72--84"
	}

You can also watch the presentation of this paper at [https://slideslive.com/38939750/klpt-kurdish-language-processing-toolkit](https://slideslive.com/38939750/klpt-kurdish-language-processing-toolkit).

### License 

<span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Kurdish Language Processing Toolkit</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/sinaahmadi/klpt" property="cc:attributionName" rel="cc:attributionURL">Sina Ahmadi</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a> which means:

- **You are free to share**, copy and redistribute the material in any medium or format and also adapt, remix, transform, and build upon the material
for any purpose, **even commercially**. 
- **You must give appropriate credit**, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- If you remix, transform, or build upon the material, **you must distribute your contributions under the same license as the original**. 



