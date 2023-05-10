from pyfoma import FST
Grammar = {}
Grammar['PART_0'] = FST.re('[a-z A-Z $\*]+')
Grammar['NOM_0'] = FST.re('[a-z A-Z $\*]+')
Grammar['VERB_0_iv'] = FST.re('[a-z A-Z $\*]+')
Grammar['VERB_0_pv'] = FST.re('[a-z A-Z $\*]+')
Grammar['VERB_0_cv'] = FST.re('[a-z A-Z $\*]+')


Grammar['PRON_n'] = FST.re("'':'\_\+'(kw|ky|km|h|w|hA|hm|hn|n|j|k|kn|nA|y)")
Grammar['PRON_v'] = FST.re("'':'\_\+'(kw|ky|km|h|w|hA|hm|hn|n|j|k|kn|nA|y|ny)")
Grammar['IOBJ'] = FST.re("'':'\_\+'l'':'\_\+'(h|w|hA|hm|hn|n|j|k|km|kn|nA|y)")
Grammar['NEG_PART'] = FST.re("'':'\_\+'(\$)")

Grammar['ART'] = FST.re("'':''Al'':'\+\_'")
Grammar['m_NEG'] = FST.re("'':''(m|mA)'':'\+\_'")
Grammar['PART_n'] = FST.re("'':''(\$|E|b|d|f|k|w|yA|A|l)'':'\+\_'")
Grammar['PART_v'] = FST.re("'':''(H|b|m|g|h|k|t|l)'':'\+\_'")
Grammar['VERB_1'] = FST.re("$PART_v? ($VERB_0_iv|$VERB_0_pv|$VERB_0_cv) $PRON_v?\
                           $IOBJ?", Grammar)

Grammar['PART'] = FST.re('$PART_0 $PRON_n?', Grammar)
Grammar['NOM'] = FST.re("$PART_n? ($ART? $NOM_0|$NOM_0 $PRON_n?)", Grammar)
Grammar['VERB'] = FST.re("$m_NEG? $VERB_1 $NEG_PART?", Grammar)

Grammar['CONJ'] = FST.re("'':''(f|t|w)'':'\+\_'")

words = FST.re('$CONJ? ($PART|$NOM|$VERB)', Grammar)
words.view()
list(words.analyze('wmbyqwllk$'))

if __name__ == "__main__":
    print("hi")