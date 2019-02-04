TAGS = {
    'NO': {
        'acronym': 'fork',
        'adjective': 'adj',
        'adverb': 'adv',
        'common_gender': 'm/f',
        'common_noun': 'appell',
        'comparative': 'komp',
        'conjunction': 'konj',
        'definite': 'be',
        'feminine': 'fem',
        'imperative': 'imp',
        'infinitive': 'inf',
        'indefinite': 'ub',
        'intransitive': 'intrans',
        'interjection': 'interj',
        'masculine': 'mask',
        'neuter_gender': 'nøyt',
        'noun': 'subst',
        'ordinal': 'ordenstall',
        'past_tense': 'pret',
        'passive': 'pass',
        'perfect_participle': 'perf-part',
        'present_participle': 'pres-part',
        'plural': 'fl',
        'positive': 'pos',
        'proper_noun': 'prop',
        'present_tense': 'pres',
        'prefix': 'pref',
        'roman_num': 'romertall',
        'superlative': 'sup',
        'singular': 'ent',
        'transitive': 'trans',
        'verb': 'verb'
    },
    'DE': {
        'acronym': 'fork',
        'adjective': 'ADJ',
        'adverb': 'ADV',
        'common_gender': 'noGender',
        'common_noun': 'appell',
        'comparative': 'comp',
        'conjunction': 'CONJ',
        'definite': '<def>',
        'feminine': 'fem',
        'imperative': 'imp',
        'infinitive': 'inf',
        'indefinite': '<indef>',
        'masculine': 'masc',
        'neuter_gender': 'neut',
        'noun': 'NN',
        'ordinal': 'ORD',
        'past_tense': 'past',
        'passive': 'pass',
        'perfect_participle': 'ppast',
        'plural': 'plu',
        'positive': 'pos',
        'proper_noun': 'NNP',
        'present_tense': 'ppres',
        'prefix': 'pref',
        'superlative': 'sup',
        'singular': 'sing',
        'verb': 'V'
    }
}


def load_tag(tagname: str) -> dict:
    return TAGS[tagname]


def load_tagname(index: int) -> str:
    local_index = 0
    for tag in TAGS.keys():
        if local_index == index:
            return tag
        local_index += 1
