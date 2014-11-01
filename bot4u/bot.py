from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc
import happy

class Bot4U(irc.IRCClient):
    def __init__(self):
        self.watches = []

    def connectionMade(self):
        """Called when a connection is made."""
        self.nickname = self.factory.nickname
        self.realname = self.factory.realname
        self.password = self.factory.password
        self.opuser = self.factory.opuser
        self.opasswd = self.factory.opasswd
        irc.IRCClient.connectionMade(self)
        log.msg("connectionMade")

    def connectionLost(self, reason):
        """Called when a connection is lost."""
        irc.IRCClient.connectionLost(self, reason)
        log.msg("connectionLost {!r}".format(reason))

    # callbacks for events

    def signedOn(self):
        """Called when bot has successfully signed on to server."""
        log.msg("Signed on")
        if self.nickname != self.factory.nickname:
            log.msg('Your nickname was already occupied, actual nickname is '
                    '"{}".'.format(self.nickname))
        self.join(self.factory.channel)

    def joined(self, channel):
        """Called when the bot joins the channel."""
        log.msg("[{nick} has joined {channel}]"
                .format(nick=self.nickname, channel=self.factory.channel,))
        log.msg("Attempting to OPER: " + self.opuser + ", " + self.opasswd)
        self.oper(self.opuser,self.opasswd)
        self.mode(channel,True,"o",user=self.nickname)

    def userRenamed(self, oldname, newname):
        """Called when a user changes name."""
        log.msg("[{nick} was renamed to {newnick}]"
                .format(nick=oldname, newnick=newname,))
        if oldname in self.watches:
            self.watches.remove(oldname)
            self.watches.append(newname)

    def me(self, channel, action):
        self.sendLine("PRIVMSG " + channel + " :" + chr(1) + "ACTION " + action + chr(1))

    def oper(self, opuser, opasswd):
        self.sendLine("OPER " + opuser + " " + opasswd)

    def privmsg(self, user, channel, msg):
        """Called when the bot receives a message."""
        senderNick = user.split('!', 1)[0]
        isunhappy = happy.is_unhappy(msg,self.factory.happy_threshold,log.msg)
        if isunhappy:
            if senderNick in self.watches:
                self.kick(channel,senderNick,reason="spreading unhappyness")
                self.me(channel,"drops " + senderNick + " into the closest judgement chute")
                self.watches.remove(senderNick)
                log.msg("Kicked user " + senderNick)
            else:
                self.msg(channel,senderNick + ": WARNING: your behaviour is threatening the peace of our beloved"
                                              " channel " + channel + ", futher violations won't be tolerated.")
                self.watches.append(senderNick)
                log.msg("User " + senderNick + " added to the watchlist")


class Bot4UFactory(protocol.ClientFactory):
    protocol = Bot4U

    def __init__(self, channel, nickname, realname, password, happy_threshold, opuser, opasswd):
        """Initialize the bot factory with our settings."""
        self.channel = channel
        self.nickname = nickname
        self.realname = realname
        self.password = password
        self.happy_threshold = happy_threshold
        self.opuser = opuser
        self.opasswd = opasswd