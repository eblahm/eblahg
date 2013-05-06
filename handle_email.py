import logging
import re
import StringIO
import email
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from eblahg import models


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        if hasattr(mail_message, 'attachments'):
            for fn, att in mail_message.attachments:
                f = StringIO.StringIO(att)
                msg = email.message_from_string(f.read())
                full_text = msg.get_payload(decode=True)
                full_text = full_text.decode('utf-8')
                title = re.search(r'title:(.+)\n', full_text)
                body = re.sub(r'title:.+\n', "", full_text)

                new = models.articles()
                if title is None:
                    new.title = "Untitled"
                else:
                    new.title = title.group(1).strip()
                new.body = body
                try:
                    new.put()
                    logging.info(
                        "New Post: %s<br>" % (new.title) +
                        "From: %s" % (mail_message.sender)
                    )
                except:
                    logging.info("Put Error")

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
