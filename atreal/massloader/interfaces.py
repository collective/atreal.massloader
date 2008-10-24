from zope.interface import Interface

class IMassLoaderAware(Interface):
    """ marker interface """
    
class IMassLoaderProvider(Interface):
    """ provider interface """
    
    def runMassLoader():
        """ runMassLoader """
