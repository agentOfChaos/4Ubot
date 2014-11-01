4Ubot
=====

4U bot applies sentiment analysis during an IRC chat session, and kicks users responsible for "unhappy" messages.  
The bot needs channel operator status to run properly; see the settings.ini file for further information.

Running
-------

$ twistd -n tw4u

Dependancies
------------

[textblob](https://github.com/sloria/TextBlob>)   
twisted   

(Both installable via pip)

Credits
-------

[newcoder](http://newcoder.io/) for the twisted IRC bot structure upon which this bot is based   
[Sluggy Freelance](http://www.sluggy.com/) wihch inspired me with the unerlying concept (as well as the name for the bot)  