from better_profanity import profanity


def testIfBad(message):
    isProfain = profanity.contains_profanity(message)
    if isProfain:
        return {
            "profanity": isProfain,
            "message": "This contains bad words.",
        }
    else:
        return {
            "profanity": isProfain,
            "message": "This does not contain bad words.",
        }
