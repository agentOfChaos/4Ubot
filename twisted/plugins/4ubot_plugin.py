from ConfigParser import ConfigParser

from twisted.application.service import IServiceMaker, Service
from twisted.internet.endpoints import clientFromString
from twisted.plugin import IPlugin
from twisted.python import usage, log
from zope.interface import implementer

from bot4u.bot import Bot4UFactory


class Options(usage.Options):
    optParameters = [
        ['config', 'c', 'settings.ini', 'Configuration file.'],
    ]


class Bot4UService(Service):
    _bot = None

    def __init__(self, endpoint, channel, nickname, realname, password, happy_threshold, opuser, opasswd):
        self._endpoint = endpoint
        self._channel = channel
        self._nickname = nickname
        self._realname = realname
        self._password = password
        self._happy_threshold = happy_threshold
        self._opuser = opuser
        self._opasswd = opasswd

    def startService(self):
        """Construct a client & connect to server."""
        from twisted.internet import reactor

        def connected(bot):
            self._bot = bot

        def failure(err):
            log.err(err, _why='Could not connect to specified server.')
            reactor.stop()

        client = clientFromString(reactor, self._endpoint)
        factory = Bot4UFactory(
            self._channel,
            self._nickname,
            self._realname,
            self._password,
            self._happy_threshold,
            self._opuser,
            self._opasswd
        )

        return client.connect(factory).addCallbacks(connected, failure)

    def stopService(self):
        """Disconnect."""
        if self._bot and self._bot.transport.connected:
            self._bot.transport.loseConnection()


@implementer(IServiceMaker, IPlugin)
class BotServiceMaker(object):
    tapname = "tw4u"
    description = "A bot designed with the users' happyness as the first concern."
    options = Options

    def makeService(self, options):
        """Construct the talkbackbot service."""
        config = ConfigParser()
        config.read([options['config']])

        return Bot4UService(
            endpoint=config.get('irc', 'endpoint'),
            channel=config.get('irc', 'channel'),
            nickname=config.get('irc', 'nickname'),
            realname=config.get('irc', 'realname'),
            password=config.get('irc','password'),
            happy_threshold=float(config.get('rea5','threshold')),
            opuser=config.get('op', 'username'),
            opasswd=config.get('op', 'password')
        )

# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.

serviceMaker = BotServiceMaker()
