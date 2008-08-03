import turbogears as tg
from turbogears import controllers, expose, flash
# from ffbstatssa import model
from turbogears import identity, redirect
from cherrypy import request, response
# from ffbstatssa import json
# import logging
# log = logging.getLogger("ffbstatssa.controllers")
# dbmechanic
from ffbstatssa.model import metadata
from dbsprockets.dbmechanic.frameworks.tg import DBMechanic
from dbsprockets.saprovider import SAProvider

class Root(controllers.RootController):
    dbmechanic = DBMechanic(SAProvider(metadata), '/dbmechanic')
    
    @expose(template="ffbstatssa.templates.welcome")
    # @identity.require(identity.in_group("admin"))
    def index(self):
        import time
        # log.debug("Happy TurboGears Controller Responding For Duty")
        flash("Your application is now running")
        return dict(now=time.ctime())

    @expose(template="ffbstatssa.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous and identity.was_login_attempted() \
                and not identity.get_identity_errors():
            redirect(tg.url(forward_url or previous_url or '/', kw))

        forward_url = None
        previous_url = request.path

        if identity.was_login_attempted():
            msg = _("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg = _("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg = _("Please log in.")
            forward_url = request.headers.get("Referer", "/")

        response.status = 403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
            original_parameters=request.params, forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        redirect("/")
