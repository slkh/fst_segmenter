# A Minimal Morphological Segmenter
This is shallow morphological segmenter that utilized a minimal grammar without a lexicon, hence a delexicalized segmenter.
This is essentially and implementation of the CFG formalism of a delexicalized morphological analyzer. in Table 1 in [Erdmann, Khalifa, et al (2019)](https://aclanthology.org/W19-4214.pdf). In the paper, the analyzer was implemented using pre-compiled tabulars for prefixes, suffixes, stems, and the repsective compatibilities between each one of them resulting in a totale of six tables. 
For this project I opted to reimplement the analyzer using finite state transducers (FSTs) that will mirror the CFG formalism, the main focus of the implementation is to produce surface segmentations for a give word. 
