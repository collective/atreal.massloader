from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from atreal.massloader.interfaces import IArchiveWrapper

try:
    from zipfile import ZipFile
    ZIP = True
except:
    ZIP = False

try:
    from py7zlib import Archive7z
    SEVENZIP = True
except:
    SEVENZIP = False


class BaseArchive(object):
    """ A base class to wrapp archive
    """
    implements(IArchiveWrapper)

    mimetypes = []

    archivefile = None

    def __init__(self):
        """
        """
        pass

    def available(self):
        """ True if the matching lib/binary is available
        """
        raise NotImplemented("Subclass Responsiblity")

    def load(self, fileupload = None):
        """
        """
        raise NotImplemented("Subclass Responsiblity")

    def listContent(self):
        """
        """
        raise NotImplemented("Subclass Responsiblity")

    def readFileByName(self, name = None):
        """
        """
        raise NotImplemented("Subclass Responsiblity")

    def mimetypeFileByName(self, name = None):
        """
        """
        raise NotImplemented("Subclass Responsiblity")

    def sizeFileByName(self, name = None):
        """
        """
        raise NotImplemented("Subclass Responsiblity")


class ZipArchive(BaseArchive):
    """
    """
    mimetypes = ['application/zip', ]

    def available(self):
        """
        """
        return ZIP

    def load(self, fileupload = None):
        """
        """
        try:
            self.archivefile = ZipFile(fileupload)
            return True
        except:
            return

    def listContent(self):
        """
        """
        return self.archivefile.namelist()

    def readFileByName(self, name = None):
        """
        """
        if name is None:
            return
        return self.archivefile.read(name)

    def mimetypeFileByName(self, name = None):
        """
        """
        if name is None:
            return
        mimetypes_registry = getToolByName(self, 'mimetypes_registry')
        mimetype = mimetypes_registry.classify(self.archivefile.read(name), filename=name)
        mimetype = str(mimetype) or 'application/octet-stream'
        return mimetype

    def sizeFileByName(self, name = None):
        """
        """
        if name is None:
            return
        infos = self.archivefile.NameToInfo[name]
        return infos.file_size


class SevenZipArchive(BaseArchive):
    """
    """
    mimetypes = ['application/x-7z-compressed', ]

    def available(self):
        """
        """
        return SEVENZIP

    def load(self, fileupload = None):
        """
        """
        try:
            self.archivefile = Archive7z(fileupload)
            return True
        except:
            return

    def listContent(self):
        """
        """
        return self.archivefile.filenames

    def readFileByName(self, name = None):
        """
        """
        if name is None:
            return
        return self.archivefile.getmember(name).read()

    def mimetypeFileByName(self, name = None):
        """
        """
        if name is None:
            return
        mimetypes_registry = getToolByName(self, 'mimetypes_registry')
        mimetype = mimetypes_registry.classify(self.archivefile.getmember(name).read(), filename=name)
        mimetype = str(mimetype) or 'application/octet-stream'
        return mimetype

    def sizeFileByName(self, name = None):
        """
        """
        if name is None:
            return
        return self.archivefile.getmember(name).size


available_archives = [
    ZipArchive,
    SevenZipArchive,
    ]
