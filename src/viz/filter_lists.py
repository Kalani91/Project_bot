# Contains generated wordlists for filtering chat messages
# Currently includes: help_words, stop_words

# Generating set of helpwords
help_words = set(
    '''help,difficult,struggling,struggle,hard,tricky,challenging,impossible,tough,complicated,daunting,frustrating,stressful,pita,discouraging,understand,don't understand,problem,trouble,troubles,anyone know,how do,don't know how,trying,tried,do we,do i,what does,can i,not sure how,how to,how can'''.split(','))

list_helpwords = list(help_words)

for word in list_helpwords:
    help_words.add(word.upper())
    help_words.add(word.title())

# Generating set of stopwords
stop_words = set(
    """
: ? * , ' " ! ... @ \\ / # '' `` ` ~ -- - . 'm ) ( = ; & 's n't > < _ .. 're .... 've nbsp 'd 'll [ ] { } $
a about above across after afterwards again against all almost alone along
already also although always am among amongst amount an and another any anyhow
anyone anything anyway anywhere are around as at au
back be became because become becomes becoming been before beforehand behind
being below beside besides between beyond both bottom but by
call can cannot ca could com can't
did do does doing done down due during don't test reload lol aha ah think good thinks want wants edu swin going thing things
each eight either eleven else elsewhere empty enough even ever every i'll look haha xd thanks hmm nice maybe ohh righty sorry use cheers having soz whats
everyone everything everywhere except en looks idk wont won't able
few fifteen fifty first five for former formerly forty four from front full flag
further b c d e f g h i j k l m n o p q r s t u v w x y z
get give go
had has have he hence her here hereafter hereby herein hereupon hers herself
him himself his how however hundred hello hey hi
i if in indeed into is it its itself im i'm it's io isn't i've ive
keep know
last latter latterly least less let like lets
just joined
made make many may me meanwhile might mine more moreover most mostly move much
must my myself
name namely neither never nevertheless next nine no nobody none noone nor not
nothing now nowhere need na
of off often on once one only onto or other others otherwise our ours ourselves
out over own ok oh org okay ohh
part per perhaps please put bad getting
quite
rather re really regarding
same say see seem seemed seeming seems serious several she should show side
since six sixty so some somehow someone something sometime sometimes somewhere
still such shall
take ten than that the their they're them themselves then thence there thereafter
thereby therefore therein thereupon these they third this those though three
through throughout thru thus to together too top toward towards twelve twenty
two
under until up unless upon us used using uh uhh
various very very via was we well were what whatever when whence whenever where
whereafter whereas whereby wherein whereupon wherever whether which while www
whither who whoever whole whom whose why will with within without would
yet you your you're yours yourself yourselves yeah yes 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31""".split()
)

list_stopwords = list(stop_words)

for word in list_stopwords:
    stop_words.add(word.upper())
    stop_words.add(word.title())
