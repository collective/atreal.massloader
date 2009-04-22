# -*- coding: utf-8 -*-

from zope.interface import Interface

class IMassLoaderProvider(Interface):
    """ provider interface """
    
    def runMassLoader():
        """ runMassLoader """
