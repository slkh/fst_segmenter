import re
import sys
import argparse
from pyfoma import FST

def create_grammar(mode):
    Grammar = {}
    #### Terminals ####
    # delexicalized segmenter, so stems can theoretically be anything
    Grammar['PART_0'] = FST.re("'':''[a-z A-Z $\*]+'':'_PART'")
    if mode == 'baseword':
        Grammar['NOM_0'] = FST.re("'':''[a-z A-Z $\*]+'':'_NOM'")
        Grammar['VERB_0_iv'] = FST.re("'':''[a-z A-Z $\*]+'':'_IV'")
        Grammar['VERB_0_pv'] = FST.re("'':''[a-z A-Z $\*]+'':'_PV'")
        Grammar['VERB_0_cv'] = FST.re("'':''[a-z A-Z $\*]+'':'_CV'")
    else:
        # nominal suffixes
        Grammar['NOM_SUFF'] = FST.re("'':'\_\+''':'_MS'|\
                                      '':'\_\+'p'':'_FS'|\
                                      '':'\_\+'yn'':'_MD'|\
                                      '':'\_\+'tyn'':'_FD'|\
                                      '':'\_\+'yn'':'_MP'|\
                                      '':'\_\+'At'':'_FP'")
        # verbal suffixes
        Grammar['IV_SUFF'] = FST.re("'':'\_\+'y'':'_IV2FS'|\
                                     '':'\_\+'wA'':('_IV2UP'|'_IV3UP')")

        Grammar['PV_SUFF'] = FST.re("'':'\_\+'t'':('_PV1US'|'_PV2MS'|'_PV3FS')|\
                                     '':'\_\+'nA'':'_PV1UP'|\
                                     '':'\_\+'ty'':'_PV2FS'|\
                                     '':'\_\+'twA'':'_PV2UP'|\
                                     '':'\_\+''':'_PV3MS'|\
                                     '':'\_\+'wA'':'_PV3UP'")

        Grammar['CV_SUFF'] = FST.re("'':'\_\+''':'_CV2MS'|\
                                     '':'\_\+'y'':'_CV2FS'|\
                                     '':'\_\+'wA'':'_CV2UP'")
        # verbal prefixes
        Grammar['IV_PREF'] = FST.re("'':''A'':'_IV1US\+\_'|\
                                     '':''n'':'_IV1UP\+\_'|\
                                     '':''t'':(('_IV2MS'|'_IV2FS'|'_IV2UP'|'_IV3FS')'\+\_')|\
                                     '':''y'':(('_IV3MS'|'_IV3UP')'\+\_')")


        Grammar['NOM_0'] = FST.re("'':''[a-z A-Z $\*]+'':'_NOM' $NOM_SUFF?", Grammar)
        Grammar['VERB_0_iv'] = FST.re("$IV_PREF '':''[a-z A-Z $\*]+'':'_IV' $IV_SUFF?", Grammar)
        Grammar['VERB_0_pv'] = FST.re("'':''[a-z A-Z $\*]+'':'_PV' $PV_SUFF", Grammar)
        Grammar['VERB_0_cv'] = FST.re("'':''[a-z A-Z $\*]+'':'_CV' $CV_SUFF", Grammar)


    ### Enclitics ###
    # pronominal clitics shared with NOM and VERB
    Grammar['PRON_nv'] = FST.re("'':'\_\+'(kw|km)'':'_2UP'|\
                                '':'\_\+'(ky|k)'':'_2FS'|\
                                '':'\_\+'k'':'_2MS'|\
                                '':'\_\+'h'':'_3MS'|\
                                '':'\_\+'hA'':'_3FS'|\
                                '':'\_\+'hm'':'_3UP'|\
                                '':'\_\+'h'':'_3MS'|\
                                '':'\_\+'nA'':'_1UP'")
    # NOM only PRON
    Grammar['PRON_n'] = FST.re("'':'\_\+'y'':'_1US'| $PRON_nv", Grammar)
    
    # VERB only PRON
    Grammar['PRON_v'] = FST.re("'':'\_\+'ny'':'_1US'| $PRON_nv", Grammar)

    # indirect object: perposition:l + PRON_n
    Grammar['IOBJ'] = FST.re("'':'\_\+'l'':'_PREP'$PRON_n", Grammar)

    # negation particle
    Grammar['NEG_PART'] = FST.re("'':'\_\+'\$'':'_NEG-PART'")

    ### Proclitics ###
    
    # Conjuctions
    Grammar['CONJ'] = FST.re("'':''(f|w)'':'_CONJ\+\_'")
    
    # definite article
    Grammar['ART'] = FST.re("'':''Al'':'_DET\+\_'")

    # negation particle, in EGY it is a circumfix m_NEG+VERB+NEG_PART
    Grammar['m_NEG'] = FST.re("'':''(m|mA)'':'_m-NEG\+\_'")

    # Prepositions, vocatives, ... etc
    Grammar['PART_n'] = FST.re("'':''(E|b|f|w|l)'':'_PREP_\+\_'\
                                '':''yA'':'_VOC-PART_\+\_'")

    # Progressive and Future particles
    Grammar['PART_v'] = FST.re("'':''(H|h)'':'_FUT-PART\+\_'|\
                                '':''b'':'_PROG-PART\+\_'|\
                                '':''l'':'_JUS-PART\+\_'")

    #### Non-Terminals ####
    Grammar['VERB_1'] = FST.re("$VERB_0_cv $PRON_v? $IOBJ?", Grammar)
    Grammar['VERB_2'] = FST.re("(($PART_v? $VERB_0_iv) | $VERB_0_pv) $PRON_v?\
                            $IOBJ?", Grammar)

    Grammar['PART'] = FST.re('$PART_0 $PRON_n?', Grammar)
    Grammar['NOM'] = FST.re("$PART_n? ($ART? $NOM_0|$NOM_0 $PRON_n?)", Grammar)
    Grammar['VERB'] = FST.re("$VERB_1 | ($m_NEG? $VERB_2 $NEG_PART?)", Grammar)

    return Grammar

def create_segmenter(Grammar):
    return FST.re('$CONJ? ($PART|$NOM|$VERB)', Grammar)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help='"baseword" for baseword \
                        segmentation only, stemming will be assumed otherwise')
    parser.add_argument('--filter', type=str, help='return segmentations with \
                        matching core POS "PV,CV,IV,NOM,PART", otherwise all \
                        segmentations will be returned')
    parser.add_argument('--word', type=str, help='word to be segmented')
    args = parser.parse_args()

    mode = args.mode.lower()
    filtering = args.filter.upper()
    word = args.word

    Grammer = create_grammar(mode)
    segmenter = create_segmenter(Grammer)


    if filtering in ['PV', 'CV', 'IV', 'NOM', 'PART']:
        segmentations = [x for x in list(segmenter.generate(word)) if f'_{filtering}' in x]
    else:
        segmentations = list(segmenter.generate(word))

    gr_segs = sorted(segmentations, key=lambda x: len(re.split("\+_|_\+", x)), reverse=True)
    print('\n'.join(gr_segs))
