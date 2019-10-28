#Private settings
PRIVATE = 'PR'
PUBLIC = 'PU'
PRIVACY_CHOICES = [(PRIVATE, 'Private'), (PUBLIC, 'Public')]

#coordinate space
MNI = 'mni'
TALAI = 'TALA'
COORDINATE_TYPES = {MNI: "MNI", TALAI: "talairach"}
COORDINATE_SPACE_CHOICE = [(MNI, 'mni'), (TALAI, 'talairach')]

#stimuli type
WORD_LIST = "word_list"
IMAGE = "image"
SENTENCE = "sentence"
STIMULI_TYPE_CHOICE = [(WORD_LIST, "Word List"),
                       (IMAGE, "Images"), (SENTENCE, "Sentences")]
STIMULI_TYPES = {WORD_LIST: "Word List", IMAGE: "Image", SENTENCE: "Sentence"}

#model types
ENG1000 = "english1000"
WORD2VEC = "word2vec"
ELMo = "ELMo"
BERT = "BERT"
CNN = "CNN"
MODEL_TYPE_CHOICE = [(ENG1000,  "english1000"), (WORD2VEC,
                                                 "word2vec"), (ELMo, "ELMo"), (BERT, "BERT"), (CNN, "CNN")]
MODEL_TYPES = {
    WORD_LIST: [ENG1000, WORD2VEC],
    SENTENCE: [ELMo, BERT],
    IMAGE: [CNN, ENG1000]
}


# word list suggestions
WORD_LIST_CONDITIONS = {
    "number": "one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more",
    "quantity": "coin, coins, cent, cents, penny, pennies, nickel, nickels, dime, dimes, quarter, quarters, dollar, dollars, ounce, ounces, pound, pounds, millimeter, millimeters, centimeter, centimeters, meter, meters, inch, inches, foot, feet, yard, yards, mile, miles, kilometer, kilometers, gram, grams, kilogram, kilograms",
    "time": "second, seconds, minute, minutes, hour, hours, day, days, week, weeks, month, months, year, years, decade, decades, century, centuries, later, sooner, before, after, soon, tomorrow, tonight, next, first, last, afternoon, afternoons, morning, mornings, night, nights, today, yesterday",
    "sight_words": "colorless, white, ivory, yellow, gold, orange, green, olive, turquoise, azure, pink, crimson, maroon, lavender, purple, silver, brown, black, mottled, red, ruby, blue, spotted, round, oval, triangular, rectangular, square, shapeless, immense, massive, large, tiny, small, tall, short, wide, long, narrow, lean, round, flat, curved, wavy, ruffled, angular, hollow, tapered, wiry, lopsided, freckled, wrinkled, striped, bright, clear, glossy, jeweled, fiery, shimmering, muddy, drab, dark, grimy, worn, cluttered, fresh, flowery, transparent, sheer, opaque, muscular, handsome, robust, fragile, pale, perky, lacy, shadowy",
    "sounds_words": "crash, squawk, crackle, chime, ring, thud, whine, buzz, laugh, silence, bump, bark, clink, gurgle, chuckle, boom, bleat, hiss, giggle, cry, thunder, bray, snort, guffaw, bawled, bang, blare, bellow, sing, crow, roar, rumble, growl, hum, chatter, scream, grate, whimper, mutter, mumble, screech, slam, stammer, murmur, wail, shout, clap, snap, whisper, babble, yell, stomp, rustle, sigh, cheer, whistle, jangle, whir, hush, storm, chirp",
    "touch_words": "cool, wet, silky, sandy, cold, slippery, velvety, gritty, icy, spongy, smooth, rough, lukewarm, mushy, soft, sharp, tepid, oily, woolly, thick, warm, waxy, furry, dry, hot, fleshy, feathery, dull, steamy, rubbery, fuzzy, thin, sticky, bumpy, hairy, fragile, damp, crisp, leathery, tender",
    "smell_words": "sweet, piney, acrid, sickly, scented, pungent, burnt, stagnant, fragrant, spicy, gaseous, musty, aromatic, gamy, putrid, moldy, perfumed, fishy, spoiled, dry, fresh, briny, sour, damp, earthy, sharp, rancid, dank",
    "taste_words": "oily, rich, bland, ripe, buttery, hearty, tasteless, medicinal, salty, mellow, sour, fishy, bitter, sugary, vinegary, spicy, bittersweet, crisp, fruity, hot, sweet, savory, tangy, burnt",
    "actions": "climb, run, walk, jump, dance, talk, negotiate, work, type, write, jog, drive, sing, bike, build, manage, assemble",
    "place_words": "house, building, hotel, office, parking, lot, park, street, road, sidewalk, highway, path, field, mountain, forest, beach, cinema, restaurant, bistro, shop, store",
    "tools": "hammer, chisel, nail, saw, drill, scythe, screw, driver, nail, paintbrush, pliers, tongs, pincers, nippers",
    "animals": "sheep, cow, horse, bird, crow, dog, cat, spider, ant, bug, butterfly, chicken, turkey, lizard, slug, snail, goat, pig, donkey, bunny, rabbit, fly, lamb, kitten, puppy, monkey, ape, chimpanzee, gorilla, fish, salmon, bear, panda, doe, buck, fox, raccoon, skunk, squirrel, roach"
}

SUBJECT_JSON_SUFFIX = "_[inflated]_mg2_9d_['rois'].json"

