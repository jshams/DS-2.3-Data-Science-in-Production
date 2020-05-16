from random import choice

quotes = [
    ("Game shows are designed to make us feel better about the random, useless facts that are all we have left of our education.", "Chuck Palahniuk"),
    ("The amount of random conversations that lead to culture-shifting ideas is insane.", "Virgil Abloh"),
    ("The Christian leaders of the future have to be theologians, persons who know the heart of God and are trained - through prayer, study, and careful analysis - to manifest the divine event of God's saving work in the midst of the many seemingly random events of their time.", "Henri Nouwen"),
    ("I know that a Christmas tree farm in Pennsylvania is about the most random place for a country singer to come from, but I had an awesome childhood.", "Taylor Swift"),
    ("O! many a shaft, at random sent, Finds mark the archer little meant! And many a word, at random spoken, May soothe or wound a heart that's broken!", "Walter Scott"),
    ("I used to write random little stupid things when I was five, but then the first song I really wrote was one called 'Fingers Crossed,' which is on SoundCloud.", "Billie Eilish"),
    ("All of the Vines that were acted & setup & had nice cameras, those weren't the good Vines. The good Vines were, like, a random little kid in the middle of a forest, like, yelling.", "Billie Eilish"),
    ("It is necessary to fall in love... if only to provide an alibi for all the random despair you are going to feel anyway.", "Albert Camus"),
    ("I believe life is an intelligent thing: that things aren't random.", "Steve Jobs"),
    ("There should be a law that no ordinary newspaper should be allowed to write about art. The harm they do by their foolish and random writing it would be impossible to overestimate - not to the artist, but to the public, blinding them to all but harming the artist not at all.", "Oscar Wilde")
]


class Response:
    def __init__(self, quote, author):
        self.body = {
            'quote': quote,
            'author': author
        }


def get_quote(quotes=quotes):
    quote = choice(quotes)
    return Response(*quote)
