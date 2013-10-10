from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from atreal.massloader.interfaces import IArchiveUtility
from atreal.massloader.archives import available_archives


class ArchiveUtility(object):
    """
    """

    implements(IArchiveUtility)

    def initialize(self, fileupload = None):
        """
        """
        #
        if fileupload is None:
            return

        #
        mimetypes_registry = getToolByName(self, 'mimetypes_registry')
        mimetype = mimetypes_registry.classify(fileupload.read(1024),
                                               filename=fileupload.filename)
        mimetype = str(mimetype) or 'application/octet-stream'
        fileupload.seek(0)

        #
        archive_class = None
        for x in available_archives:
            if mimetype in x.mimetypes:
                archive_class = x
        if archive_class is None:
            return

        #
        archive = archive_class()
        if archive.available() is None:
            return
        if archive.load(fileupload) is None:
            return

        #
        return archive
