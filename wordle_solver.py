"""
interactive Wordle solver.
easy to use,
How to use?
1. Open https://www.nytimes.com/games/wordle/index.html
2. Guess your first word
3. Input info from output of guess as required by code

For further instruction read READ_ME github https://github.com/Jacob-Link under Wordle directory
"""
import random
from collections import Counter


class Word:
    def __init__(self, word):
        self.val = word
        self.sum_letter_position_score = 0


def input_info(green_info, yellow_info, black_info, word_attempt):
    """
    :return: Dosnt return anything due to using lists and dict which are sent to function in py as the original,
        (similar to pointers in c), no need to return the object due to the update in place.
    """
    print()
    green_update = ''
    yellow_update = ''
    black_update = ''
    flag_ = 1
    while flag_:
        green_update = input("Green letters: ")
        flag_ = check_letter_input(green_update, word_attempt)

    flag_ = 1
    while flag_:
        yellow_update = input("Yellow letters: ")
        flag_ = check_letter_input(yellow_update, word_attempt)

    flag_ = 1
    while flag_:
        black_update = input("Black letters: ")
        flag_ = check_letter_input(black_update, word_attempt)

    # green update
    green_update = green_update.replace(' ', '').split(',')
    green_update = [x for x in green_update if x != '']
    for let in green_update:
        index_ = word_attempt.index(let)
        green_info[index_] = let  # update '_' with the green letter
        if let in yellow_info:
            yellow_info.__delitem__(let)  # remove the green letter from the yellow dict

    # check if won and inputted all green
    all_green = 1
    for letter in green_info:
        if letter == '_':
            all_green = 0

    # yellow update
    yellow_update = yellow_update.replace(' ', '').split(',')
    yellow_update = [x for x in yellow_update if x != '']
    for let in yellow_update:
        index_ = word_attempt.index(let)
        if let in yellow_info:
            yellow_info[let].append(index_)
        else:
            yellow_info[let] = [index_]

    # black update
    black_update = black_update.replace(' ', '').split(',')
    black_update = [x for x in black_update if x != '']
    black_info += black_update

    total_updated_letters = len(green_update + yellow_update + black_update)

    print()

    if total_updated_letters > 5:
        return 'ABORT'  # only error which i decided to abort code if detected.

    else:
        if all_green:
            return 'W'  # user inputted that all the letters were green
        else:
            return 'All GOOD'


def filter_words(green_info, yellow_info, black_info, words_to_filter):
    # correct letter position
    green_position = []
    for index_, letter in enumerate(green_info):
        if letter != '_':
            green_position.append(index_)

    return_optional_results = []
    for word in words_to_filter:
        flag_ = 0  # if check fails - flag_ == 1
        # check 1
        for index_ in green_position:
            if green_info[index_] != word[index_]:
                flag_ = 1

        # check 2
        for letter in black_info:
            if letter in word:
                flag_ = 1

        # check 3
        for letter in yellow_info:
            if letter not in word:
                flag_ = 1
            else:
                for position in yellow_info[letter]:
                    if word[position] == letter:
                        flag_ = 1

        if flag_ == 0:
            return_optional_results.append(word)

    return return_optional_results


def calc_score(list_of_words):
    first = [word.val[0] for word in list_of_words]
    second = [word.val[1] for word in list_of_words]
    third = [word.val[2] for word in list_of_words]
    fourth = [word.val[3] for word in list_of_words]
    fifth = [word.val[4] for word in list_of_words]

    counters = [Counter(first), Counter(second), Counter(third), Counter(fourth), Counter(fifth)]

    for word in list_of_words:
        score = 0
        score_norm = 0
        for index, letter in enumerate(word.val):
            score += counters[index][letter]
        word.sum_letter_position_score = score

    list_of_words.sort(key=lambda x: x.sum_letter_position_score, reverse=True)  # sort letters by score
    return list_of_words


def find_next_word(green_info, yellow_info, black_info, words, step, num_to_return):
    """
    return: tuple, (first recommended word, list of 3 top words with their score)
    """
    words_after_filter = filter_words(green_info, yellow_info, black_info, words)
    words_obj = [Word(x) for x in words_after_filter]
    sorted_obj_list = calc_score(words_obj)

    if step < 3:  # return highest scoring non duplicate word
        for word in sorted_obj_list:
            if len(set(word.val)) == 5:
                return_list = [(x.val, x.sum_letter_position_score) for x in sorted_obj_list][:num_to_return]
                return word.val, return_list

        return_list = [(x.val, x.sum_letter_position_score) for x in sorted_obj_list][:num_to_return]
        return sorted_obj_list[0].val, return_list  # less than 4 attempts, only duplicates remain

    else:
        return_list = [(x.val, x.sum_letter_position_score) for x in sorted_obj_list][:num_to_return]
        return sorted_obj_list[0].val, return_list


def update_info_to_unique_key(green_info, yellow_info, black_info):
    key = ['_', '_', '_', '_', '_']

    # green unique_key
    for i, let in enumerate(green_info):
        if let != '_':
            key[i] = '1'

    # yellow unique_key
    for k in yellow_info:
        key[yellow_info[k][0]] = '2'

    # black unique_key
    for let in black_info:
        key[attempt_word.find(let)] = '3'

    re = ""
    return re.join(key)


def check_word(input_word, past_words):
    errors = []
    flag_ = 0
    if len(input_word) != 5:
        flag_ = 1
        errors.append('*** ERROR: Word must be 5 letters long ***')
    for let in input_word:
        if ord(let) < ord('a') or ord(let) > ord('z'):
            flag_ = 1
            errors.append('*** ERROR: Word must contain lowercase English letters only ***')
            break

    if input_word in past_words:
        flag_ = 1
        errors.append(
            '*** Insanity ***\nDoing the same thing over and over again...\n...and expecting different results\n'
            '"Albert Einstein"\n\n '
            '*** Error: you\'ve already chosen that word... wake up ***')

    if len(errors) != 0:
        print()
    for error in errors:
        print(error)

    if flag_:
        return 1
    return 0


def check_letter_input(update, input_word):
    flag_ = 0
    print_general = 0
    update = update.replace(' ', '').split(',')
    checked_update = []
    for elem in update:
        if len(elem) != 1 and elem != '':
            flag_ = 1
            print_general = 1
        if len(elem) == 1:
            if ord(elem) < ord('a') or ord(elem) > ord('z'):
                flag_ = 1
                print_general = 1
            else:
                checked_update.append(elem)  # valid letter

    if len(checked_update) > 5:
        print("*** ERROR: To many letters in update ***")
        flag_ = 1

    for letter in checked_update:
        if letter not in input_word:
            flag_ = 1
            print('*** ERROR: Letters in update do not appear in the guessed word ***')
            break

    if flag_:
        if print_general:
            print(
                '*** ERROR: Invalid update. Update must be lowercase English letters. '
                'Separated by commas ***\n*** Example: t, r, y, a, g, a, i, n ***\n')
        return 1
    return 0


if __name__ == '__main__':
    green = ['_', '_', '_', '_', '_']
    black = []
    yellow = {}
    history = []
    abort = 0
    input_win = 0  # flag for inputting all green word
    unique_key = 0
    hack_num = 3
    attempt_word = ''
    first_word = ''
    reco_word = ''
    
    legal_words = ['cigar', 'rebut', 'sissy', 'humph', 'awake', 'blush', 'focal', 'evade', 'naval', 'serve', 'heath',
                   'dwarf', 'model', 'karma', 'stink', 'grade', 'quiet', 'bench', 'abate', 'feign', 'major', 'death',
                   'fresh', 'crust', 'stool', 'colon', 'abase', 'marry', 'react', 'batty', 'pride', 'floss', 'helix',
                   'croak', 'staff', 'paper', 'unfed', 'whelp', 'trawl', 'outdo', 'adobe', 'crazy', 'sower', 'repay',
                   'digit', 'crate', 'cluck', 'spike', 'mimic', 'pound', 'maxim', 'linen', 'unmet', 'flesh', 'booby',
                   'forth', 'first', 'stand', 'belly', 'ivory', 'seedy', 'print', 'yearn', 'drain', 'bribe', 'stout',
                   'panel', 'crass', 'flume', 'offal', 'agree', 'error', 'swirl', 'argue', 'bleed', 'delta', 'flick',
                   'totem', 'wooer', 'front', 'shrub', 'parry', 'biome', 'lapel', 'start', 'greet', 'goner', 'golem',
                   'lusty', 'loopy', 'round', 'audit', 'lying', 'gamma', 'labor', 'islet', 'civic', 'forge', 'corny',
                   'moult', 'basic', 'salad', 'agate', 'spicy', 'spray', 'essay', 'fjord', 'spend', 'kebab', 'guild',
                   'aback', 'motor', 'alone', 'hatch', 'hyper', 'thumb', 'dowry', 'ought', 'belch', 'dutch', 'pilot',
                   'tweed', 'comet', 'jaunt', 'enema', 'steed', 'abyss', 'growl', 'fling', 'dozen', 'boozy', 'erode',
                   'world', 'gouge', 'click', 'briar', 'great', 'altar', 'pulpy', 'blurt', 'coast', 'duchy', 'groin',
                   'fixer', 'group', 'rogue', 'badly', 'smart', 'pithy', 'gaudy', 'chill', 'heron', 'vodka', 'finer',
                   'surer', 'radio', 'rouge', 'perch', 'retch', 'wrote', 'clock', 'tilde', 'store', 'prove', 'bring',
                   'solve', 'cheat', 'grime', 'exult', 'usher', 'epoch', 'triad', 'break', 'rhino', 'viral', 'conic',
                   'masse', 'sonic', 'vital', 'trace', 'using', 'peach', 'champ', 'baton', 'brake', 'pluck', 'craze',
                   'gripe', 'weary', 'picky', 'acute', 'ferry', 'aside', 'tapir', 'troll', 'unify', 'rebus', 'boost',
                   'truss', 'siege', 'tiger', 'banal', 'slump', 'crank', 'gorge', 'query', 'drink', 'favor', 'abbey',
                   'tangy', 'panic', 'solar', 'shire', 'proxy', 'point', 'robot', 'prick', 'wince', 'crimp', 'knoll',
                   'sugar', 'whack', 'mount', 'perky', 'could', 'wrung', 'light', 'those', 'moist', 'shard', 'pleat',
                   'aloft', 'skill', 'elder', 'frame', 'humor', 'pause', 'ulcer', 'ultra', 'robin', 'cynic', 'aroma',
                   'caulk', 'shake', 'dodge', 'swill', 'tacit', 'other', 'thorn', 'trove', 'bloke', 'vivid', 'spill',
                   'chant', 'choke', 'rupee', 'nasty', 'mourn', 'ahead', 'brine', 'cloth', 'hoard', 'sweet', 'month',
                   'lapse', 'watch', 'today', 'focus', 'smelt', 'tease', 'cater', 'movie', 'saute', 'allow', 'renew',
                   'their', 'slosh', 'purge', 'chest', 'depot', 'epoxy', 'nymph', 'found', 'shall', 'stove', 'lowly',
                   'snout', 'trope', 'fewer', 'shawl', 'natal', 'comma', 'foray', 'scare', 'stair', 'black', 'squad',
                   'royal', 'chunk', 'mince', 'shame', 'cheek', 'ample', 'flair', 'foyer', 'cargo', 'oxide', 'plant',
                   'olive', 'inert', 'askew', 'heist', 'shown', 'zesty', 'trash', 'larva', 'forgo', 'story', 'hairy',
                   'train', 'homer', 'badge', 'midst', 'canny', 'shine', 'gecko', 'farce', 'slung', 'tipsy', 'metal',
                   'yield', 'delve', 'being', 'scour', 'glass', 'gamer', 'scrap', 'money', 'hinge', 'album', 'vouch',
                   'asset', 'tiara', 'crept', 'bayou', 'atoll', 'manor', 'creak', 'showy', 'phase', 'froth', 'depth',
                   'gloom', 'flood', 'trait', 'girth', 'piety', 'goose', 'float', 'donor', 'atone', 'primo', 'apron',
                   'blown', 'cacao', 'loser', 'input', 'gloat', 'awful', 'brink', 'smite', 'beady', 'rusty', 'retro',
                   'droll', 'gawky', 'hutch', 'pinto', 'egret', 'lilac', 'sever', 'field', 'fluff', 'agape', 'voice',
                   'stead', 'berth', 'madam', 'night', 'bland', 'liver', 'wedge', 'roomy', 'wacky', 'flock', 'angry',
                   'trite', 'aphid', 'tryst', 'midge', 'power', 'elope', 'cinch', 'motto', 'stomp', 'upset', 'bluff',
                   'cramp', 'quart', 'coyly', 'youth', 'rhyme', 'buggy', 'alien', 'smear', 'unfit', 'patty', 'cling',
                   'glean', 'label', 'hunky', 'khaki', 'poker', 'gruel', 'twice', 'twang', 'shrug', 'treat', 'waste',
                   'merit', 'woven', 'needy', 'clown', 'irony', 'ruder', 'gauze', 'chief', 'onset', 'prize', 'fungi',
                   'charm', 'gully', 'inter', 'whoop', 'taunt', 'leery', 'class', 'theme', 'lofty', 'tibia', 'booze',
                   'alpha', 'thyme', 'doubt', 'parer', 'chute', 'stick', 'trice', 'alike', 'recap', 'saint', 'glory',
                   'grate', 'admit', 'brisk', 'soggy', 'usurp', 'scald', 'scorn', 'leave', 'twine', 'sting', 'bough',
                   'marsh', 'sloth', 'dandy', 'vigor', 'howdy', 'enjoy', 'valid', 'ionic', 'equal', 'floor', 'catch',
                   'spade', 'stein', 'exist', 'quirk', 'denim', 'grove', 'spiel', 'mummy', 'fault', 'foggy', 'flout',
                   'carry', 'sneak', 'libel', 'waltz', 'aptly', 'piney', 'inept', 'aloud', 'photo', 'dream', 'stale',
                   'unite', 'snarl', 'baker', 'there', 'glyph', 'pooch', 'hippy', 'spell', 'folly', 'louse', 'gulch',
                   'vault', 'godly', 'threw', 'fleet', 'grave', 'inane', 'shock', 'crave', 'spite', 'valve', 'skimp',
                   'claim', 'rainy', 'musty', 'pique', 'daddy', 'quasi', 'arise', 'aging', 'valet', 'opium', 'avert',
                   'stuck', 'recut', 'mulch', 'genre', 'plume', 'rifle', 'count', 'incur', 'total', 'wrest', 'mocha',
                   'deter', 'study', 'lover', 'safer', 'rivet', 'funny', 'smoke', 'mound', 'undue', 'sedan', 'pagan',
                   'swine', 'guile', 'gusty', 'equip', 'tough', 'canoe', 'chaos', 'covet', 'human', 'udder', 'lunch',
                   'blast', 'stray', 'manga', 'melee', 'lefty', 'quick', 'paste', 'given', 'octet', 'risen', 'groan',
                   'leaky', 'grind', 'carve', 'loose', 'sadly', 'spilt', 'apple', 'slack', 'honey', 'final', 'sheen',
                   'eerie', 'minty', 'slick', 'derby', 'wharf', 'spelt', 'coach', 'erupt', 'singe', 'price', 'spawn',
                   'fairy', 'jiffy', 'filmy', 'stack', 'chose', 'sleep', 'ardor', 'nanny', 'niece', 'woozy', 'handy',
                   'grace', 'ditto', 'stank', 'cream', 'usual', 'diode', 'valor', 'angle', 'ninja', 'muddy', 'chase',
                   'reply', 'prone', 'spoil', 'heart', 'shade', 'diner', 'arson', 'onion', 'sleet', 'dowel', 'couch',
                   'palsy', 'bowel', 'smile', 'evoke', 'creek', 'lance', 'eagle', 'idiot', 'siren', 'built', 'embed',
                   'award', 'dross', 'annul', 'goody', 'frown', 'patio', 'laden', 'humid', 'elite', 'lymph', 'edify',
                   'might', 'reset', 'visit', 'gusto', 'purse', 'vapor', 'crock', 'write', 'sunny', 'loath', 'chaff',
                   'slide', 'queer', 'venom', 'stamp', 'sorry', 'still', 'acorn', 'aping', 'pushy', 'tamer', 'hater',
                   'mania', 'awoke', 'brawn', 'swift', 'exile', 'birch', 'lucky', 'freer', 'risky', 'ghost', 'plier',
                   'lunar', 'winch', 'snare', 'nurse', 'house', 'borax', 'nicer', 'lurch', 'exalt', 'about', 'savvy',
                   'toxin', 'tunic', 'pried', 'inlay', 'chump', 'lanky', 'cress', 'eater', 'elude', 'cycle', 'kitty',
                   'boule', 'moron', 'tenet', 'place', 'lobby', 'plush', 'vigil', 'index', 'blink', 'clung', 'qualm',
                   'croup', 'clink', 'juicy', 'stage', 'decay', 'nerve', 'flier', 'shaft', 'crook', 'clean', 'china',
                   'ridge', 'vowel', 'gnome', 'snuck', 'icing', 'spiny', 'rigor', 'snail', 'flown', 'rabid', 'prose',
                   'thank', 'poppy', 'budge', 'fiber', 'moldy', 'dowdy', 'kneel', 'track', 'caddy', 'quell', 'dumpy',
                   'paler', 'swore', 'rebar', 'scuba', 'splat', 'flyer', 'horny', 'mason', 'doing', 'ozone', 'amply',
                   'molar', 'ovary', 'beset', 'queue', 'cliff', 'magic', 'truce', 'sport', 'fritz', 'edict', 'twirl',
                   'verse', 'llama', 'eaten', 'range', 'whisk', 'hovel', 'rehab', 'macaw', 'sigma', 'spout', 'verve',
                   'sushi', 'dying', 'fetid', 'brain', 'buddy', 'thump', 'scion', 'candy', 'chord', 'basin', 'march',
                   'crowd', 'arbor', 'gayly', 'musky', 'stain', 'dally', 'bless', 'bravo', 'stung', 'title', 'ruler',
                   'kiosk', 'blond', 'ennui', 'layer', 'fluid', 'tatty', 'score', 'cutie', 'zebra', 'barge', 'matey',
                   'bluer', 'aider', 'shook', 'river', 'privy', 'betel', 'frisk', 'bongo', 'begun', 'azure', 'weave',
                   'genie', 'sound', 'glove', 'braid', 'scope', 'wryly', 'rover', 'assay', 'ocean', 'bloom', 'irate',
                   'later', 'woken', 'silky', 'wreck', 'dwelt', 'slate', 'smack', 'solid', 'amaze', 'hazel', 'wrist',
                   'jolly', 'globe', 'flint', 'rouse', 'civil', 'vista', 'relax', 'cover', 'alive', 'beech', 'jetty',
                   'bliss', 'vocal', 'often', 'dolly', 'eight', 'joker', 'since', 'event', 'ensue', 'shunt', 'diver',
                   'poser', 'worst', 'sweep', 'alley', 'creed', 'anime', 'leafy', 'bosom', 'dunce', 'stare', 'pudgy',
                   'waive', 'choir', 'stood', 'spoke', 'outgo', 'delay', 'bilge', 'ideal', 'clasp', 'seize', 'hotly',
                   'laugh', 'sieve', 'block', 'meant', 'grape', 'noose', 'hardy', 'shied', 'drawl', 'daisy', 'putty',
                   'strut', 'burnt', 'tulip', 'crick', 'idyll', 'vixen', 'furor', 'geeky', 'cough', 'naive', 'shoal',
                   'stork', 'bathe', 'aunty', 'check', 'prime', 'brass', 'outer', 'furry', 'razor', 'elect', 'evict',
                   'imply', 'demur', 'quota', 'haven', 'cavil', 'swear', 'crump', 'dough', 'gavel', 'wagon', 'salon',
                   'nudge', 'harem', 'pitch', 'sworn', 'pupil', 'excel', 'stony', 'cabin', 'unzip', 'queen', 'trout',
                   'polyp', 'earth', 'storm', 'until', 'taper', 'enter', 'child', 'adopt', 'minor', 'fatty', 'husky',
                   'brave', 'filet', 'slime', 'glint', 'tread', 'steal', 'regal', 'guest', 'every', 'murky', 'share',
                   'spore', 'hoist', 'buxom', 'inner', 'otter', 'dimly', 'level', 'sumac', 'donut', 'stilt', 'arena',
                   'sheet', 'scrub', 'fancy', 'slimy', 'pearl', 'silly', 'porch', 'dingo', 'sepia', 'amble', 'shady',
                   'bread', 'friar', 'reign', 'dairy', 'quill', 'cross', 'brood', 'tuber', 'shear', 'posit', 'blank',
                   'villa', 'shank', 'piggy', 'freak', 'which', 'among', 'fecal', 'shell', 'would', 'algae', 'large',
                   'rabbi', 'agony', 'amuse', 'bushy', 'copse', 'swoon', 'knife', 'pouch', 'ascot', 'plane', 'crown',
                   'urban', 'snide', 'relay', 'abide', 'viola', 'rajah', 'straw', 'dilly', 'crash', 'amass', 'third',
                   'trick', 'tutor', 'woody', 'blurb', 'grief', 'disco', 'where', 'sassy', 'beach', 'sauna', 'comic',
                   'clued', 'creep', 'caste', 'graze', 'snuff', 'frock', 'gonad', 'drunk', 'prong', 'lurid', 'steel',
                   'halve', 'buyer', 'vinyl', 'utile', 'smell', 'adage', 'worry', 'tasty', 'local', 'trade', 'finch',
                   'ashen', 'modal', 'gaunt', 'clove', 'enact', 'adorn', 'roast', 'speck', 'sheik', 'missy', 'grunt',
                   'snoop', 'party', 'touch', 'mafia', 'emcee', 'array', 'south', 'vapid', 'jelly', 'skulk', 'angst',
                   'tubal', 'lower', 'crest', 'sweat', 'cyber', 'adore', 'tardy', 'swami', 'notch', 'groom', 'roach',
                   'hitch', 'young', 'align', 'ready', 'frond', 'strap', 'puree', 'realm', 'venue', 'swarm', 'offer',
                   'seven', 'dryer', 'diary', 'dryly', 'drank', 'acrid', 'heady', 'theta', 'junto', 'pixie', 'quoth',
                   'bonus', 'shalt', 'penne', 'amend', 'datum', 'build', 'piano', 'shelf', 'lodge', 'suing', 'rearm',
                   'coral', 'ramen', 'worth', 'psalm', 'infer', 'overt', 'mayor', 'ovoid', 'glide', 'usage', 'poise',
                   'randy', 'chuck', 'prank', 'fishy', 'tooth', 'ether', 'drove', 'idler', 'swath', 'stint', 'while',
                   'begat', 'apply', 'slang', 'tarot', 'radar', 'credo', 'aware', 'canon', 'shift', 'timer', 'bylaw',
                   'serum', 'three', 'steak', 'iliac', 'shirk', 'blunt', 'puppy', 'penal', 'joist', 'bunny', 'shape',
                   'beget', 'wheel', 'adept', 'stunt', 'stole', 'topaz', 'chore', 'fluke', 'afoot', 'bloat', 'bully',
                   'dense', 'caper', 'sneer', 'boxer', 'jumbo', 'lunge', 'space', 'avail', 'short', 'slurp', 'loyal',
                   'flirt', 'pizza', 'conch', 'tempo', 'droop', 'plate', 'bible', 'plunk', 'afoul', 'savoy', 'steep',
                   'agile', 'stake', 'dwell', 'knave', 'beard', 'arose', 'motif', 'smash', 'broil', 'glare', 'shove',
                   'baggy', 'mammy', 'swamp', 'along', 'rugby', 'wager', 'quack', 'squat', 'snaky', 'debit', 'mange',
                   'skate', 'ninth', 'joust', 'tramp', 'spurn', 'medal', 'micro', 'rebel', 'flank', 'learn', 'nadir',
                   'maple', 'comfy', 'remit', 'gruff', 'ester', 'least', 'mogul', 'fetch', 'cause', 'oaken', 'aglow',
                   'meaty', 'gaffe', 'shyly', 'racer', 'prowl', 'thief', 'stern', 'poesy', 'rocky', 'tweet', 'waist',
                   'spire', 'grope', 'havoc', 'patsy', 'truly', 'forty', 'deity', 'uncle', 'swish', 'giver', 'preen',
                   'bevel', 'lemur', 'draft', 'slope', 'annoy', 'lingo', 'bleak', 'ditty', 'curly', 'cedar', 'dirge',
                   'grown', 'horde', 'drool', 'shuck', 'crypt', 'cumin', 'stock', 'gravy', 'locus', 'wider', 'breed',
                   'quite', 'chafe', 'cache', 'blimp', 'deign', 'fiend', 'logic', 'cheap', 'elide', 'rigid', 'false',
                   'renal', 'pence', 'rowdy', 'shoot', 'blaze', 'envoy', 'posse', 'brief', 'never', 'abort', 'mouse',
                   'mucky', 'sulky', 'fiery', 'media', 'trunk', 'yeast', 'clear', 'skunk', 'scalp', 'bitty', 'cider',
                   'koala', 'duvet', 'segue', 'creme', 'super', 'grill', 'after', 'owner', 'ember', 'reach', 'nobly',
                   'empty', 'speed', 'gipsy', 'recur', 'smock', 'dread', 'merge', 'burst', 'kappa', 'amity', 'shaky',
                   'hover', 'carol', 'snort', 'synod', 'faint', 'haunt', 'flour', 'chair', 'detox', 'shrew', 'tense',
                   'plied', 'quark', 'burly', 'novel', 'waxen', 'stoic', 'jerky', 'blitz', 'beefy', 'lyric', 'hussy',
                   'towel', 'quilt', 'below', 'bingo', 'wispy', 'brash', 'scone', 'toast', 'easel', 'saucy', 'value',
                   'spice', 'honor', 'route', 'sharp', 'bawdy', 'radii', 'skull', 'phony', 'issue', 'lager', 'swell',
                   'urine', 'gassy', 'trial', 'flora', 'upper', 'latch', 'wight', 'brick', 'retry', 'holly', 'decal',
                   'grass', 'shack', 'dogma', 'mover', 'defer', 'sober', 'optic', 'crier', 'vying', 'nomad', 'flute',
                   'hippo', 'shark', 'drier', 'obese', 'bugle', 'tawny', 'chalk', 'feast', 'ruddy', 'pedal', 'scarf',
                   'cruel', 'bleat', 'tidal', 'slush', 'semen', 'windy', 'dusty', 'sally', 'igloo', 'nerdy', 'jewel',
                   'shone', 'whale', 'hymen', 'abuse', 'fugue', 'elbow', 'crumb', 'pansy', 'welsh', 'syrup', 'terse',
                   'suave', 'gamut', 'swung', 'drake', 'freed', 'afire', 'shirt', 'grout', 'oddly', 'tithe', 'plaid',
                   'dummy', 'broom', 'blind', 'torch', 'enemy', 'again', 'tying', 'pesky', 'alter', 'gazer', 'noble',
                   'ethos', 'bride', 'extol', 'decor', 'hobby', 'beast', 'idiom', 'utter', 'these', 'sixth', 'alarm',
                   'erase', 'elegy', 'spunk', 'piper', 'scaly', 'scold', 'hefty', 'chick', 'sooty', 'canal', 'whiny',
                   'slash', 'quake', 'joint', 'swept', 'prude', 'heavy', 'wield', 'femme', 'lasso', 'maize', 'shale',
                   'screw', 'spree', 'smoky', 'whiff', 'scent', 'glade', 'spent', 'prism', 'stoke', 'riper', 'orbit',
                   'cocoa', 'guilt', 'humus', 'shush', 'table', 'smirk', 'wrong', 'noisy', 'alert', 'shiny', 'elate',
                   'resin', 'whole', 'hunch', 'pixel', 'polar', 'hotel', 'sword', 'cleat', 'mango', 'rumba', 'puffy',
                   'filly', 'billy', 'leash', 'clout', 'dance', 'ovate', 'facet', 'chili', 'paint', 'liner', 'curio',
                   'salty', 'audio', 'snake', 'fable', 'cloak', 'navel', 'spurt', 'pesto', 'balmy', 'flash', 'unwed',
                   'early', 'churn', 'weedy', 'stump', 'lease', 'witty', 'wimpy', 'spoof', 'saner', 'blend', 'salsa',
                   'thick', 'warty', 'manic', 'blare', 'squib', 'spoon', 'probe', 'crepe', 'knack', 'force', 'debut',
                   'order', 'haste', 'teeth', 'agent', 'widen', 'icily', 'slice', 'ingot', 'clash', 'juror', 'blood',
                   'abode', 'throw', 'unity', 'pivot', 'slept', 'troop', 'spare', 'sewer', 'parse', 'morph', 'cacti',
                   'tacky', 'spool', 'demon', 'moody', 'annex', 'begin', 'fuzzy', 'patch', 'water', 'lumpy', 'admin',
                   'omega', 'limit', 'tabby', 'macho', 'aisle', 'skiff', 'basis', 'plank', 'verge', 'botch', 'crawl',
                   'lousy', 'slain', 'cubic', 'raise', 'wrack', 'guide', 'foist', 'cameo', 'under', 'actor', 'revue',
                   'fraud', 'harpy', 'scoop', 'climb', 'refer', 'olden', 'clerk', 'debar', 'tally', 'ethic', 'cairn',
                   'tulle', 'ghoul', 'hilly', 'crude', 'apart', 'scale', 'older', 'plain', 'sperm', 'briny', 'abbot',
                   'rerun', 'quest', 'crisp', 'bound', 'befit', 'drawn', 'suite', 'itchy', 'cheer', 'bagel', 'guess',
                   'broad', 'axiom', 'chard', 'caput', 'leant', 'harsh', 'curse', 'proud', 'swing', 'opine', 'taste',
                   'lupus', 'gumbo', 'miner', 'green', 'chasm', 'lipid', 'topic', 'armor', 'brush', 'crane', 'mural',
                   'abled', 'habit', 'bossy', 'maker', 'dusky', 'dizzy', 'lithe', 'brook', 'jazzy', 'fifty', 'sense',
                   'giant', 'surly', 'legal', 'fatal', 'flunk', 'began', 'prune', 'small', 'slant', 'scoff', 'torus',
                   'ninny', 'covey', 'viper', 'taken', 'moral', 'vogue', 'owing', 'token', 'entry', 'booth', 'voter',
                   'chide', 'elfin', 'ebony', 'neigh', 'minim', 'melon', 'kneed', 'decoy', 'voila', 'ankle', 'arrow',
                   'mushy', 'tribe', 'cease', 'eager', 'birth', 'graph', 'odder', 'terra', 'weird', 'tried', 'clack',
                   'color', 'rough', 'weigh', 'uncut', 'ladle', 'strip', 'craft', 'minus', 'dicey', 'titan', 'lucid',
                   'vicar', 'dress', 'ditch', 'gypsy', 'pasta', 'taffy', 'flame', 'swoop', 'aloof', 'sight', 'broke',
                   'teary', 'chart', 'sixty', 'wordy', 'sheer', 'leper', 'nosey', 'bulge', 'savor', 'clamp', 'funky',
                   'foamy', 'toxic', 'brand', 'plumb', 'dingy', 'butte', 'drill', 'tripe', 'bicep', 'tenor', 'krill',
                   'worse', 'drama', 'hyena', 'think', 'ratio', 'cobra', 'basil', 'scrum', 'bused', 'phone', 'court',
                   'camel', 'proof', 'heard', 'angel', 'petal', 'pouty', 'throb', 'maybe', 'fetal', 'sprig', 'spine',
                   'shout', 'cadet', 'macro', 'dodgy', 'satyr', 'rarer', 'binge', 'trend', 'nutty', 'leapt', 'amiss',
                   'split', 'myrrh', 'width', 'sonar', 'tower', 'baron', 'fever', 'waver', 'spark', 'belie', 'sloop',
                   'expel', 'smote', 'baler', 'above', 'north', 'wafer', 'scant', 'frill', 'awash', 'snack', 'scowl',
                   'frail', 'drift', 'limbo', 'fence', 'motel', 'ounce', 'wreak', 'revel', 'talon', 'prior', 'knelt',
                   'cello', 'flake', 'debug', 'anode', 'crime', 'salve', 'scout', 'imbue', 'pinky', 'stave', 'vague',
                   'chock', 'fight', 'video', 'stone', 'teach', 'cleft', 'frost', 'prawn', 'booty', 'twist', 'apnea',
                   'stiff', 'plaza', 'ledge', 'tweak', 'board', 'grant', 'medic', 'bacon', 'cable', 'brawl', 'slunk',
                   'raspy', 'forum', 'drone', 'women', 'mucus', 'boast', 'toddy', 'coven', 'tumor', 'truer', 'wrath',
                   'stall', 'steam', 'axial', 'purer', 'daily', 'trail', 'niche', 'mealy', 'juice', 'nylon', 'plump',
                   'merry', 'flail', 'papal', 'wheat', 'berry', 'cower', 'erect', 'brute', 'leggy', 'snipe', 'sinew',
                   'skier', 'penny', 'jumpy', 'rally', 'umbra', 'scary', 'modem', 'gross', 'avian', 'greed', 'satin',
                   'tonic', 'parka', 'sniff', 'livid', 'stark', 'trump', 'giddy', 'reuse', 'taboo', 'avoid', 'quote',
                   'devil', 'liken', 'gloss', 'gayer', 'beret', 'noise', 'gland', 'dealt', 'sling', 'rumor', 'opera',
                   'thigh', 'tonga', 'flare', 'wound', 'white', 'bulky', 'etude', 'horse', 'circa', 'paddy', 'inbox',
                   'fizzy', 'grain', 'exert', 'surge', 'gleam', 'belle', 'salvo', 'crush', 'fruit', 'sappy', 'taker',
                   'tract', 'ovine', 'spiky', 'frank', 'reedy', 'filth', 'spasm', 'heave', 'mambo', 'right', 'clank',
                   'trust', 'lumen', 'borne', 'spook', 'sauce', 'amber', 'lathe', 'carat', 'corer', 'dirty', 'slyly',
                   'affix', 'alloy', 'taint', 'sheep', 'kinky', 'wooly', 'mauve', 'flung', 'yacht', 'fried', 'quail',
                   'brunt', 'grimy', 'curvy', 'cagey', 'rinse', 'deuce', 'state', 'grasp', 'milky', 'bison', 'graft',
                   'sandy', 'baste', 'flask', 'hedge', 'girly', 'swash', 'boney', 'coupe', 'endow', 'abhor', 'welch',
                   'blade', 'tight', 'geese', 'miser', 'mirth', 'cloud', 'cabal', 'leech', 'close', 'tenth', 'pecan',
                   'droit', 'grail', 'clone', 'guise', 'ralph', 'tango', 'biddy', 'smith', 'mower', 'payee', 'serif',
                   'drape', 'fifth', 'spank', 'glaze', 'allot', 'truck', 'kayak', 'virus', 'testy', 'tepee', 'fully',
                   'zonal', 'metro', 'curry', 'grand', 'banjo', 'axion', 'bezel', 'occur', 'chain', 'nasal', 'gooey',
                   'filer', 'brace', 'allay', 'pubic', 'raven', 'plead', 'gnash', 'flaky', 'munch', 'dully', 'eking',
                   'thing', 'slink', 'hurry', 'theft', 'shorn', 'pygmy', 'ranch', 'wring', 'lemon', 'shore', 'mamma',
                   'froze', 'newer', 'style', 'moose', 'antic', 'drown', 'vegan', 'chess', 'guppy', 'union', 'lever',
                   'lorry', 'image', 'cabby', 'druid', 'exact', 'truth', 'dopey', 'spear', 'cried', 'chime', 'crony',
                   'stunk', 'timid', 'batch', 'gauge', 'rotor', 'crack', 'curve', 'latte', 'witch', 'bunch', 'repel',
                   'anvil', 'soapy', 'meter', 'broth', 'madly', 'dried', 'scene', 'known', 'magma', 'roost', 'woman',
                   'thong', 'punch', 'pasty', 'downy', 'knead', 'whirl', 'rapid', 'clang', 'anger', 'drive', 'goofy',
                   'email', 'music', 'stuff', 'bleep', 'rider', 'mecca', 'folio', 'setup', 'verso', 'quash', 'fauna',
                   'gummy', 'happy', 'newly', 'fussy', 'relic', 'guava', 'ratty', 'fudge', 'femur', 'chirp', 'forte',
                   'alibi', 'whine', 'petty', 'golly', 'plait', 'fleck', 'felon', 'gourd', 'brown', 'thrum', 'ficus',
                   'stash', 'decry', 'wiser', 'junta', 'visor', 'daunt', 'scree', 'impel', 'await', 'press', 'whose',
                   'turbo', 'stoop', 'speak', 'mangy', 'eying', 'inlet', 'crone', 'pulse', 'mossy', 'staid', 'hence',
                   'pinch', 'teddy', 'sully', 'snore', 'ripen', 'snowy', 'attic', 'going', 'leach', 'mouth', 'hound',
                   'clump', 'tonal', 'bigot', 'peril', 'piece', 'blame', 'haute', 'spied', 'undid', 'intro', 'basal',
                   'rodeo', 'guard', 'steer', 'loamy', 'scamp', 'scram', 'manly', 'hello', 'vaunt', 'organ', 'feral',
                   'knock', 'extra', 'condo', 'adapt', 'willy', 'polka', 'rayon', 'skirt', 'faith', 'torso', 'match',
                   'mercy', 'tepid', 'sleek', 'riser', 'twixt', 'peace', 'flush', 'catty', 'login', 'eject', 'roger',
                   'rival', 'untie', 'refit', 'aorta', 'adult', 'judge', 'rower', 'artsy', 'rural', 'shave', 'bobby',
                   'eclat', 'fella', 'gaily', 'harry', 'hasty', 'hydro', 'liege', 'octal', 'ombre', 'payer', 'sooth',
                   'unset', 'unlit', 'vomit', 'fanny', 'fetus', 'butch', 'stalk', 'flack', 'widow', 'augur']

    keys_second_recommendation = {'23211': 'becap', '21133': 'caphs', '21333': 'baffs', '12332': 'ampul',
                                  '33312': 'hiply', '13321': 'krunk', '13121': 'gravs', '33111': 'agrin',
                                  '23313': 'germy', '23213': 'nymph', '13223': 'pricy', '23231': 'crimp',
                                  '33321': 'chirp', '12233': 'brond', '33311': 'corni', '31232': 'mincy',
                                  '32331': 'boing', '33213': 'pyric', '33123': 'prick', '12133': 'chimp',
                                  '23133': 'brogh', '11333': 'hinky', '31332': 'corby', '31331': 'bipod',
                                  '31233': 'bronc', '13233': 'purin', '32223': 'bidon', '13133': 'chirk',
                                  '31333': 'bidon', '12333': 'prick', '31133': 'prick', '13123': 'prink',
                                  '13333': 'unrip', '13332': 'unrip', '32133': 'chirm', '33313': 'brond',
                                  '23333': 'chirm', '33231': 'boric', '33323': 'corni', '32233': 'corni',
                                  '32231': 'chimb', '33133': 'chynd', '23331': 'corni', '13331': 'chirp',
                                  '33232': 'cromb', '32333': 'pricy', '32332': 'bronc', '33223': 'bipod',
                                  '33331': 'corni', '13323': 'prink', '31131': 'brond', '13131': 'prink',
                                  '33332': 'bidon', '33131': 'prick', '23123': 'boart'}

    daily_quotes = ['Only when the tide goes out do you discover who\'s been swimming naked.\n"Warren Buffett"',
                    'It takes 20 years to build a reputation and five minutes to ruin it. If you think about that, you\'ll do things differently.\n"Warren Buffett"',
                    'Someone is sitting in the shade today because someone planted a tree a long time ago.\n"Warren Buffett"',
                    'Rule No.1: Never lose money. Rule No.2: Never forget rule No.1.\n"Warren Buffett"',
                    'Chains of habit are too light to be felt until they are too heavy to be broken.\n"Warren Buffett"',
                    'Price is what you pay. Value is what you get.\n"Warren Buffett"',
                    'It\'s far better to buy a wonderful company at a fair price than a fair company at a wonderful price.\n"Warren Buffett"',
                    'Risk comes from not knowing what you\'re doing.\n"Warren Buffett"',
                    'Wall Street is the only place that people ride to in a Rolls Royce to get advice from those who take the subway.\n"Warren Buffett"',
                    'When a management with a reputation for brilliance tackles a business with a reputation for bad economics, it is the reputation of the business that remains intact.\n"Warren Buffett"',
                    'Time is the friend of the wonderful company, the enemy of the mediocre.\n"Warren Buffett"',
                    'In the business world, the rearview mirror is always clearer than the windshield.\n"Warren Buffett"',
                    'It\'s better to hang out with people better than you. Pick out associates whose behavior is better than yours and you\'ll drift in that direction.\n"Warren Buffett"',
                    'You only have to do a very few things right in your life so long as you don\'t do too many things wrong.\n"Warren Buffett"',
                    'Predicting rain doesn\'t count. Building arks does.\n"Warren Buffett"',
                    'Our favorite holding period is forever.\n"Warren Buffett"',
                    'Should you find yourself in a chronically leaking boat, energy devoted to changing vessels is likely to be more productive than energy devoted to patching leaks.\n"Warren Buffett"',
                    'We simply attempt to be fearful when others are greedy and to be greedy only when others are fearful.\n"Warren Buffett"',
                    'Only buy something that you\'d be perfectly happy to hold if the market shut down for 10 years.\n"Warren Buffett"',
                    'Derivatives are financial weapons of mass destruction.\n"Warren Buffett"',
                    'The only way to get love is to be lovable. It\'s very irritating if you have a lot of money. You\'d like to think you could write a check: \'I\'ll buy a million dollars\' worth of love.\' But it doesn\'t work that way. The more you give love away, the more you get.\n"Warren Buffett"',
                    'I buy expensive suits. They just look cheap on me.\n"Warren Buffett"',
                    'When you combine ignorance and leverage, you get some pretty interesting results.\n"Warren Buffett"',
                    'There seems to be some perverse human characteristic that likes to make easy things difficult.\n"Warren Buffett"',
                    'If a business does well, the stock eventually follows.\n"Warren Buffett"',
                    'If past history was all there was to the game, the richest people would be librarians.\n"Warren Buffett"',
                    'I never attempt to make money on the stock market. I buy on the assumption that they could close the market the next day and not reopen it for five years.\n"Warren Buffett"',
                    'Basically, when you get to my age, you\'ll really measure your success in life by how many of the people you want to have love you actually do love you.\n"Warren Buffett"',
                    'Wide diversification is only required when investors do not understand what they are doing.\n"Warren Buffett"',
                    'The best thing I did was to choose the right heroes.\n"Warren Buffett"',
                    'We enjoy the process far more than the proceeds.\n"Warren Buffett"',
                    'A public-opinion poll is no substitute for thought.\n"Warren Buffett"',
                    'Look at market fluctuations as your friend rather than your enemy; profit from folly rather than participate in it.\n"Warren Buffett"',
                    'The business schools reward difficult complex behavior more than simple behavior, but simple behavior is more effective.\n"Warren Buffett"',
                    'Today people who hold cash equivalents feel comfortable. They shouldn\'t. They have opted for a terrible long-term asset, one that pays virtually nothing and is certain to depreciate in value.\n"Warren Buffett"',
                    'Of the billionaires I have known, money just brings out the basic traits in them. If they were jerks before they had money, they are simply jerks with a billion dollars.\n"Warren Buffett"',
                    'The investor of today does not profit from yesterday\'s growth.\n"Warren Buffett"',
                    'If you get to my age in life and nobody thinks well of you, I don\'t care how big your bank account is, your life is a disaster.\n"Warren Buffett"',
                    'Why not invest your assets in the companies you really like? As Mae West said, \'Too much of a good thing can be wonderful\'.\n"Warren Buffett"',
                    'We believe that according the name \'investors\' to institutions that trade actively is like calling someone who repeatedly engages in one-night stands a \'romantic.\'\n"Warren Buffett"',
                    'The big question about how people behave is whether they\'ve got an Inner Scorecard or an Outer Scorecard. It helps if you can be satisfied with an Inner Scorecard.\n"Warren Buffett"',
                    'I bought a company in the mid-\'90s called Dexter Shoe and paid $400 million for it. And it went to zero. And I gave about $400 million worth of Berkshire stock, which is probably now worth $400 billion. But I\'ve made lots of dumb decisions. That\'s part of the game.\n"Warren Buffett"',
                    'Learn from yesterday, live for today, hope for tomorrow. The important thing is not to stop questioning.\n"Albert Einstein"',
                    'If you can\'t explain it simply, you don\'t understand it well enough.\n"Albert Einstein"',
                    'Only two things are infinite, the universe and human stupidity, and I\'m not sure about the former.\n"Albert Einstein"',
                    'Life is like riding a bicycle. To keep your balance, you must keep moving.\n"Albert Einstein"',
                    'Look deep into nature, and then you will understand everything better.\n"Albert Einstein"',
                    'We cannot solve our problems with the same thinking we used when we created them.\n"Albert Einstein"',
                    'Strive not to be a success, but rather to be of value.\n"Albert Einstein"',
                    'Coincidence is God\'s way of remaining anonymous.\n"Albert Einstein"',
                    'Weakness of attitude becomes weakness of character.\n"Albert Einstein"',
                    'I never think of the future - it comes soon enough.\n"Albert Einstein"',
                    'I have no special talent. I am only passionately curious.\n"Albert Einstein"',
                    'A person who never made a mistake never tried anything new.\n"Albert Einstein"',
                    'It\'s not that I\'m so smart, it\'s just that I stay with problems longer.\n"Albert Einstein"',
                    'You can\'t blame gravity for falling in love.\n"Albert Einstein"',
                    'Reality is merely an illusion, albeit a very persistent one.\n"Albert Einstein"',
                    'Logic will get you from A to B. Imagination will take you everywhere.\n"Albert Einstein"',
                    'No problem can be solved from the same level of consciousness that created it.\n"Albert Einstein"',
                    'Peace cannot be kept by force; it can only be achieved by understanding.\n"Albert Einstein"',
                    'The only source of knowledge is experience.\n"Albert Einstein"',
                    'We can\'t solve problems by using the same kind of thinking we used when we created them.\n"Albert Einstein"',
                    'Anyone who doesn\'t take truth seriously in small matters cannot be trusted in large ones either.\n"Albert Einstein"',
                    'It is the supreme art of the teacher to awaken joy in creative expression and knowledge.\n"Albert Einstein"',
                    'Imagination is everything. It is the preview of life\'s coming attractions.\n"Albert Einstein"',
                    'The world is a dangerous place to live; not because of the people who are evil, but because of the people who don\'t do anything about it.\n"Albert Einstein"',
                    'The only reason for time is so that everything doesn\'t happen at once.\n"Albert Einstein"',
                    'Intellectuals solve problems, geniuses prevent them.\n"Albert Einstein"',
                    'I know not with what weapons World War III will be fought, but World War IV will be fought with sticks and stones.\n"Albert Einstein"',
                    'Great spirits have always encountered violent opposition from mediocre minds.\n"Albert Einstein"',
                    'Nationalism is an infantile disease. It is the measles of mankind.\n"Albert Einstein"',
                    'Common sense is the collection of prejudices acquired by age eighteen.\n"Albert Einstein"',
                    'I live in that solitude which is painful in youth, but delicious in the years of maturity.\n"Albert Einstein"',
                    'If we knew what it was we were doing, it would not be called research, would it?\n"Albert Einstein"',
                    'Anyone who has never made a mistake has never tried anything new.\n"Albert Einstein"',
                    'Any man who can drive safely while kissing a pretty girl is simply not giving the kiss the attention it deserves.\n"Albert Einstein"',
                    'Whoever is careless with the truth in small matters cannot be trusted with important matters.\n"Albert Einstein"',
                    'The true sign of intelligence is not knowledge but imagination.\n"Albert Einstein"',
                    'If people are good only because they fear punishment, and hope for reward, then we are a sorry lot indeed.\n"Albert Einstein"',
                    'Only a life lived for others is a life worthwhile.\n"Albert Einstein"',
                    'Everything should be made as simple as possible, but not simpler.\n"Albert Einstein"',
                    'If you are out to describe the truth, leave elegance to the tailor.\n"Albert Einstein"',
                    'The value of a man should be seen in what he gives and not in what he is able to receive.\n"Albert Einstein"',
                    'Education is what remains after one has forgotten what one has learned in school.\n"Albert Einstein"',
                    'Once we accept our limits, we go beyond them.\n"Albert Einstein"',
                    'The hardest thing to understand in the world is the income tax.\n"Albert Einstein"',
                    'No amount of experimentation can ever prove me right; a single experiment can prove me wrong.\n"Albert Einstein"',
                    'The important thing is not to stop questioning. Curiosity has its own reason for existing.\n"Albert Einstein"',
                    'A table, a chair, a bowl of fruit and a violin; what else does a man need to be happy?\n"Albert Einstein"',
                    'Intellectual growth should commence at birth and cease only at death.\n"Albert Einstein"',
                    'Everyone should be respected as an individual, but no one idolized.\n"Albert Einstein"',
                    'Pure mathematics is, in its way, the poetry of logical ideas.\n"Albert Einstein"',
                    'A question that sometimes drives me hazy: am I or are the others crazy?\n"Albert Einstein"',
                    'There are two ways to live: you can live as if nothing is a miracle; you can live as if everything is a miracle.\n"Albert Einstein"',
                    'He who can no longer pause to wonder and stand rapt in awe, is as good as dead; his eyes are closed.\n"Albert Einstein"',
                    'Try not to become a man of success, but rather try to become a man of value.\n"Albert Einstein"',
                    'It is strange to be known so universally and yet to be so lonely.\n"Albert Einstein"',
                    'The gift of fantasy has meant more to me than my talent for absorbing positive knowledge.\n"Albert Einstein"',
                    'Before God we are all equally wise - and equally foolish.\n"Albert Einstein"',
                    'In matters of truth and justice, there is no difference between large and small problems, for issues concerning the treatment of people are all the same.\n"Albert Einstein"',
                    'The monotony and solitude of a quiet life stimulates the creative mind.\n"Albert Einstein"',
                    'All that is valuable in human society depends upon the opportunity for development accorded the individual.\n"Albert Einstein"']

    print("Good morning!\nWordle solver up and ready.\n")
    count = 1

    while count <= 6:
        print(f'----- {count} -----')
        abort = 0
        flag = 1
        while flag:
            attempt_word = input("Input guess: ")
            if attempt_word == 'HACK':  # prints all word left nd not just the top 3
                hack_num = 2500
                next_guess_tup = find_next_word(green, yellow, black, legal_words, count, hack_num)
                print("\n################## HACK ####################")
                print(f'\t\tWord\tScore')
                for index, word_tup in enumerate(next_guess_tup[1]):
                    print(f'\t{index + 1}.  {word_tup[0]}\t{word_tup[1]}')
                print("##########################################")
                hack_num = 3
            else:
                if attempt_word == 'v':  # shortcut to chose the recommended word
                    if count == 1:
                        print("*** First attempt, no recommended word yet, guess your word ***")
                    else:
                        attempt_word = reco_word
                        print(f"Chosen the recommended word: {reco_word.upper()}")
                        flag = 0  # exit while loop
                else:
                    flag = check_word(attempt_word, history)  # if detected error flag = 1

        history.append(attempt_word)

        flag = input_info(green, yellow, black, attempt_word)  # update the info from the colors of the input word

        if flag == 'ABORT':
            print("\n*** Invalid update information, over 5 letters inputted in total ***")
            print("\nStart again...")
            abort = 1
            break
        elif flag == 'W':
            input_win = 1
            break

        if count == 1:
            first_word = attempt_word
            unique_key = update_info_to_unique_key(green, yellow, black)

        try:
            next_guess_tup = find_next_word(green, yellow, black, legal_words, count, hack_num)

        except IndexError:
            # error occurs when input info wasnt from real game
            # or word with double letters was inputted in a contradicting way
            print("\n*** Error ***")
            print("*** Info sequence does not exist"
                  " or usage of word with duplicate letter which was interpreted incorrectly in update info ***")
            print("\nINPUT 'HACK' in 'input guess' stage, to reveal more words")
            abort = 1
            break

        if len(next_guess_tup[1]) != 1:
            print(f'\t\tWord\tScore')
            for index, word_tup in enumerate(next_guess_tup[1]):
                print(f'\t{index + 1}.  {word_tup[0]}\t{word_tup[1]}')

            if count == 1 and unique_key in keys_second_recommendation and first_word == 'slate':
                key_sec_word = keys_second_recommendation[unique_key]
                reco_word = key_sec_word
                print(f'Recommended word: {key_sec_word.upper()} (Based on unique key)\n')
                if key_sec_word in {'caphs', 'baffs'}:
                    print("*** Only if 's' is GREEN, input as new info ***\n")
                if key_sec_word == 'ampul':
                    print("*** Only if 'l' is GREEN, input as new info ***\n")
                if key_sec_word == 'hiply':
                    print("*** If 'y' not GREEN, NEXT recommended word: TEETH ***\n")

            else:
                reco_word = next_guess_tup[0]
                print(f'\nRecommended word: {reco_word.upper()}\n')

        else:  # only 1 word remaining
            print(f"Last word in list of words (!!!) >>> {next_guess_tup[0].upper()}")
            break

        count += 1

    if not abort:
        if count == 6:
            print("\nLost... That sucks.\n")
        else:
            print(f"\nCongrats, Won in {count + 1 - input_win} attempts!\n\n")
            print(daily_quotes[random.randint(0, len(daily_quotes))])  # generate random quote
            print()
            print("Have a great day!")
