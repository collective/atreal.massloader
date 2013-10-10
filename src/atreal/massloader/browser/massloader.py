from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


from Products.statusmessages.interfaces import IStatusMessage

from atreal.massloader import MassLoaderMessageFactory as _
from atreal.massloader.interfaces import IMassLoader


class MassLoaderView(BrowserView):
    """
    """

    template = ViewPageTemplateFile('massloader.pt')
    log = None

    def __call__(self):
        """
        """
        # if form is not submitted return
        if not self.request.has_key('form.button.submit'):
            return self.template()

        #
        if self.request.has_key('up_file') and self.request.form['up_file']:
            up_file = self.request.form['up_file']
            build_report = self.request.has_key('build_report')
            status, self.log = IMassLoader(self.context).process(up_file,
                                                                 build_report)
            IStatusMessage(self.request).addStatusMessage(status, type='info')
            return self.template()
        else:
            status = _(u"You have to select a file.")
            redirecturl = self.context.absolute_url()+'/@@massloader'
            self.request.response.redirect(redirecturl)
            IStatusMessage(self.request).addStatusMessage(status, type='info')

    def available(self):
        """
        """
        return IMassLoader(self.context).available()

    def getMaxFileSize(self):
        """
        """
        return IMassLoader(self.context).getMaxFileSize / 1000000


class MassLoaderActionProvider(BrowserView):
    """
    """

    def available(self):
        """
        """
        try:
            return IMassLoader(self.context).available()
        except:
            return False
