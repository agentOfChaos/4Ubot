from textblob import TextBlob

def get_sentiment(blob):
    blob = TextBlob(text.decode("utf-8")).translate(to="en")
    return blob.sentiment

def is_unhappy(text, thr, logfun):
    ret = False
    megablob = TextBlob(text.decode("utf-8")).translate(to="en")
    if logfun != None:
        logfun(str(len(megablob.sentences)) + " new sentences detectd: ")
    for sentence in megablob.sentences:
        if logfun != None:
            logfun("Analyzed sentiment: " + str(sentence.sentiment) + ", threshold: " + str(thr))
        if sentence.sentiment[0] < thr:
            ret = True
    return ret