*_This is the project for [LIN637: Computational Linguistics 2](https://github.com/Compling2-Spring2023-SBU) class._*

# A Minimal Morphological Segmenter for Arabic

This is shallow morphological segmenter that utilized a minimal grammar without a lexicon, hence, a delexicalized segmenter.
This is essentially an implementation of the CFG formalism of a delexicalized morphological analyzer in Table 1 in [Erdmann, Khalifa, et al (2019)](https://aclanthology.org/W19-4214.pdf). In the paper, the analyzer was implemented using pre-compiled tabulars for prefixes, suffixes, stems, and the repsective compatibilities between each one of them resulting in a total of six tables. 
```
WORD   → CONJ? (NOM | VERB | PART)
PART   → PART_0 PRON_n
NOM    → PART_n? (ART? NOM_0 | NOM_0 PRON_n?)
VERB   → NEG? VERB_1 NEG_PART?
VERB_1 → PART_v? (VERB_0.iv | VERB_0.pv | VERB_0.cv) PRON_v? IOBJ?
```
For this project I opted to reimplement the analyzer using FSTs that will based on the CFG formalism, the main focus of the implementation is to produce surface segmentations for a given word. 


## Approach

The core task is to generate all possible segmentations for an input word. All the affixes and clitics are specefied as part of the grammar, both the lexical and the POS information. 
To create the FST(s), [Pyfoma](https://github.com/mhulden/pyfoma) was used. Pyfoma suports different approaches to create FSTs, in this work however, I opted to create FSTs through compiling python/peal like regular expressions. Even though Pyfoma provides scafolding for creating a morphological analyzer/generator, it is however strictly through right-linear grammar formalisms which is not usable in this case since Arabic concatnative morphology utilizes both prefixes and suffixes.

Since this is a delexicalized segmenter, the output is expected to have all possible segmentations across all possible POS. The original work in [Erdmann, Khalifa, et al (2019)](https://aclanthology.org/W19-4214.pdf) describes different approaches to selecting the most plausible segmentation given the context of the word, this is not addressed in this work. However, an option to filter the segmentations based on a given core POS is added, the available core POS are:
- `NOM` all nominals. This can be expanded to the different types of nouns and adjectives, but it is not cruicial to this specific work.
- `PART` all standalone particles. Essentially these are all closed-class lexical items, but here we assume that we know very little about the given language.
- `PV` perfective verbs.
- `IV` imperfective verbs.
- `CV` command verbs. Also known as imperative, howevern in most Arabic NLP work, they are interpreted as a feature of aspect.

Additionally, there are two modes of segmentations:
- `baseword` a scheme that segments clitics only, this is equvilant to the D3 segmentation described in Habash (2010).
-  `stem` a more verbose segmentation that segments both clitics _and_ affixes. This is similar to the segmentation used in the Buckwalter POS tag (Buckwalter, 2004).

## Assumptions

- The grammar used describes that of Egyptian Arabic in particular, it should work for closely related dialects.
- Undiacritized orthography (in [Buckwalter transilitration scheme](https://en.wikipedia.org/wiki/Buckwalter_transliteration)) is assumed to be the representation of the input. This is the main reason why many affix morphemes have the same form (there are few cases where the morphemes are actually identical).
- The output is always sorted by the most greedy segmentation.

---

## Contents

- `segmenter.py` main segmentation script.
- `requirements.txt` necessary dependencies needed to run the scripts, in this case, only Pyfoma.
- `README.md` this document.

## Requirements

- Python 3.8 and above.

To use, you need to first install the necessary dependencies by running the following command:

```bash
pip install -r requirements.txt
```

---
## Usage

```text
usage: segmenter.py [-h] [-m MODE] [-f FILTER] -w WORD

optional arguments:
  -h,        --help            show this help message and exit
  -m MODE,   --mode MODE  "baseword" for baseword segmentation only, stemming will be assumed otherwise ("stem").
  -f FILTER, --filter FILTER
                        return segmentations with matching core POS "PV,CV,IV,NOM,PART", otherwise all segmentations will be returned
  -w WORD,   --word WORD  word to be segmented
```
---
## Example

### Input
wmktbhA$ /wi-ma-katab-ha:-ʃ/ 'and he did not write it'

``` bash
python segmenter.py -m stem -f PV -w wmktbhA$
```

### Output
In this case the first one (the most greedy) is the correct segmentation
```text
w_CONJ+_m_m-NEG+_ktb_PV_+_PV3MS_+hA_3FS_+$_NEG-PART
w_CONJ+_m_m-NEG+_ktbhA_PV_+_PV3MS_+$_NEG-PART
w_CONJ+_mktbhA$_PV_+_PV3MS
wmktbhA$_PV_+_PV3MS
```

