# -*- coding: utf-8 -*-

from Products.Five  import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from zope.component import queryUtility
import transaction

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from atreal.massloader import MassLoaderMessageFactory as _
from atreal.massloader.interfaces import IMassLoaderProvider
from atreal.massloader.browser.controlpanel import IMassLoaderSchema

from zipfile import ZipFile

class MassLoaderProvider (BrowserView):

    implements (IMassLoaderProvider)
    encoding = 'cp850'
    msg = {
            'noUpFile':_(u'ml_py_noUpFile',"Uploaded file doesn't exist"),
            'notZipFile':_(u'ml_py_notZipFile','Uploaded file is not a valid zip file'),                
            'generalError':_(u'ml_py_generalError','Some errors occured while loading files'),
            'success':_(u'ml_py_success','All files were successfully loaded'),
            'noReport':_(u'ml_py_noReport','Error while building the report'),
            'createError':_(u'ml_py_createError','Error while creating object'),
            'updateError':_(u'ml_py_updateError','Error while updating object'),
            'updateOK':_(u'ml_py_updateOK','File updated'),
            'createOK':_(u'ml_py_createOK','File created'),
            'contextNotAllowed':_(u'ml_py_contextNotAllowed','You are not allowed to import an archive here'),
            # the win patch create already the folders, so they are all conserved
            # We change the message for neutral one, XXX to be fixed later...  
            'folderExisted':_(u'ml_py_folderExisted','Folder OK'),
            'folderOK':_(u'ml_py_folderOK','Folder created'),
            }
    log = {}
    wannaReport = {}
    report = {}
   
    def __init__ (self, context, request):
        self.context = context
        self.request = request
        self.maxFileSize = int((self.getMaxFileSize ())) * 1000000L

    @property
    def _options (self):
        _siteroot = queryUtility (IPloneSiteRoot)
        return IMassLoaderSchema (_siteroot)
    
    def getMaxFileSize (self):
        """ Return the maxFileSize from Settings
        """
        return getattr (self._options, 'massloader_max_file_size', '20')

    def isCtrEnabled (self):
        """ Return the ctr_enabled from Settings
        """
        return getattr (self._options, 'massloader_ctr_enabled')

    def getImagePortalType (self):
        """ Return the portal type to create Image in Settings
        """
        return getattr (self._options, 'massloader_image_portal_type', 'Image')
    
    def getFilePortalType (self):
        """ Return the portal type to create File in Settings
        """
        return getattr (self._options, 'massloader_file_portal_type', 'File')

    def isKeywordsEnabled (self):
        """ Return True if this option is enabled in Settings
        """
        return getattr (self._options, 'massloader_keywords_enable', False)
    
    def isMassLoaderAware (self):
        """ Return True if the context is a selected content types in Settings
        """
        if self.context.portal_type in getattr (self._options, 'massloader_possible_types', []):
            return True
        else:
            return False

    def loadKeywordsAndDescription (self, obj, **kwargs):
        """ Set on new object created Keywords and Description of the context
            if this option is enabled in Settings
        """
        if self.isKeywordsEnabled ():
            obj.setDescription (self.context.Description ())
            obj.setSubject (self.context.Subject ())
    
    def redirectToContext (self):
        """ Redirect to the context page with the portal status message
            contextNotAllowed
        """
        self.outMassLoader (self.msg['contextNotAllowed'], self.context.absolute_url ())
    
    def initReport (self, md5Id):
        """ init the string used for building the report """
        tabHead = ' <table class="listing" \
                   tal:attributes="summary string:Import results" \
                   tal:condition="python:results"> \
              <tr> \
                <th>Original file name</th>\
                <th>Direct Link</th>\
                <th>Size</th>\
                <th>Status</th>\
                <th>Notes</th>\
              </tr>\
        '
        self.report[md5Id] = tabHead

    def addLine (self, entry, md5Id):
        """ Add a line into the report """
        tabLine = '     <tr>\
                  <td>%s</td>\
                  <td>\
                    <a href="%s">%s</a>\
                  </td>\
                  <td>%s</td>\
                  <td>%s</td>\
                  <td>%s</td>\
                </tr>\
        '
        values = [entry[item] for item in ['filename','url','title','size','status','info']]
        self.report[md5Id] += tabLine % tuple(values) 
        
    def finalizeReport (self, zipFileName, md5Id):
        """
        """
        tabFooter = '</table>\
        '
        putils = getToolByName(self, 'plone_utils')
        ptypes = getToolByName(self, 'portal_types')
        self.report[md5Id] += tabFooter
        id = self.safeNormalize(putils,zipFileName+'-'+md5Id)
        try:
            ptypes.constructContent(type_name='Document', container=self.context,id=id)
            report = self.context[id]
            report.setText(self.report[md5Id])
            report.setTitle('Report %s' % zipFileName)
            report.setDescription('Import report for the zip file %s' % zipFileName)
            report.reindexObject()
        except:
            return False
        return True


    def setLog (self, md5Id, filename, title='N/A', size='0', url=None,
                status='Ok', info=None):
        """
        """
        entry = {
                    'filename':filename,
                    'title':title,
                    'size':size,
                    'url':url, 
                    'status':status,
                    'info':info,
                }
        if self.wannaReport[md5Id]:
            self.addLine(entry,md5Id)
        self.log[md5Id].append(entry)


    def getLog (self, md5Id):
        """
        """
        return self.log.pop(md5Id,[])


    def getFileTitle (self, item, lPath):
        """ Return type and title """
        if item.endswith('/'):
            return lPath[len(lPath)-2],True
        else:
            return lPath[len(lPath)-1],False


    def manage_additionalOperation (self, type, obj, **kwargs):
        """ Here we hardcoded the object creation, 
            until we find a way to proceed generically.
            Add your CT specific operation here.
        """
        if not self.isCtrEnabled():
            if type == self.getImagePortalType():
                obj.setImage(kwargs['data'])
    
            elif type == self.getFilePortalType():
                obj.setFile(kwargs['data'], filename=kwargs['filename'])
        else:
            if type == 'Document':
                obj.setText(kwargs['data'])
            else:
                obj.update_data(kwargs['data'])
    
    
    def reencode (self, txt):
        """
        """
        try:
            return txt.decode('utf-8')
        except:
            return txt.decode(self.encoding).encode('utf-8')
    
    
    def safeNormalize (self, putils, txt):
        """
        """
        try:
            return putils.normalizeString(txt)
        except:
            return putils.normalizeString(unicode(txt,self.encoding))

    
    def getContainer (self, path, item):
        """ Return the container object """
        ind = path.index(item)
        if not ind:
            return self.context
        else:
            putils = getToolByName(self, 'plone_utils')
            pcatalog = getToolByName(self,'portal_catalog')
            id = self.safeNormalize(putils,path[ind-1])
            normPath = [self.safeNormalize(putils,item) for item in path[:ind]]
            cPath = '/'.join(list(self.context.getPhysicalPath())+normPath)
            brain = pcatalog(path=cPath,getId=id)
            if len(brain) == 1:
                return brain[0].getObject()
            else:
                return False


    def validateFile (self, filename, zFile):
        """ Validate few parameters of the compressed file """
        zInfo = zFile.NameToInfo[filename]
        if zInfo.file_size > self.maxFileSize:
            return False,zInfo.file_size
        return True,zInfo.file_size         
  

    def createObject (self, id, isFolder, title, container, zFile, filename):
        """ Create the object """
        putils = getToolByName(self, 'plone_utils')
        ptypes = getToolByName(self, 'portal_types')
        if isFolder:
            if id in container.keys():
            # Object exists yet, it's a folder, so we keep it without change
                code = "folderExisted"
                obj = container[id]
            else:     
                try:
                    type = 'Folder'
                    ptypes.constructContent(type_name=type, container=container, 
                                            id=id, title=title)
                    obj = container[id]
                    self.loadKeywordsAndDescription(obj)
                    obj.reindexObject()
                except:
                    return False,'createError',None,''
                code = 'folderOK'
        else:
            if id in container.keys():
                try:
                    obj = container[id]
                    data = zFile.read(filename)
                    type = obj.getPortalTypeName()
                    self.manage_additionalOperation(type,obj,data=data,
                                                    filename=filename)
                    obj.reindexObject()
                    transaction.savepoint(optimistic=True)
                except:
                    return False,"updateError",None,''
                code = 'updateOK'
            else:
                try:
                    mtr = getToolByName(self,'mimetypes_registry')
                    ctr = getToolByName(self,'content_type_registry')                
                    data = zFile.read(filename)
                    mimetype = mtr.classify(data,filename=filename).__str__()
                    type = ctr.findTypeName(filename,mimetype,None)
                    if not self.isCtrEnabled():
                        if type != self.getImagePortalType():
                            type = self.getFilePortalType()
                    ptypes.constructContent(type_name=type, container=container, 
                                            id=id)
                    obj = container[id]
                    self.loadKeywordsAndDescription(obj)
                    self.manage_additionalOperation(type,obj,data=data,
                                                    filename=filename)
                    obj.setTitle(title)
                    obj.setFormat(mimetype)
                    obj.reindexObject()
                    transaction.savepoint(optimistic=True)
                except:
                    return False,"createError",None,''
                code = 'createOK'
        return True,code,obj.absolute_url(),obj.getObjSize()


    def loadZipFile (self):
        """ Load the incoming file into a ZipFile object """
        if 'up_file' in self.request.keys() and self.request['up_file']:
            try:
                zFile = ZipFile (self.request['up_file'])
                md5Id = self.uniqueId(zFile.NameToInfo.keys())
                self.log[md5Id] = []
            except:
                return 'notZipFile',None
            return zFile,md5Id
        return 'noUpFile',None


    def winPatch (self, zFile, md5Id):
        """ When using the zip functionnality of Microsoft Windows,
           the zip specification is not well implemented. 
           So, we have to check it first ...  
        """
        putils = getToolByName(self, 'plone_utils')
        rootFolderList = []
        for item in zFile.namelist():
            lPath = item.split('/')
            if len(lPath)>=2 and lPath[0] not in rootFolderList:
                rootFolderList.append(lPath[0])
                id = self.safeNormalize(putils,lPath[0])
                container = self.context
                rt,code,url,size = self.createObject(id,True,
                                                self.safeNormalize(putils,lPath[0]),
                                                container,zFile,item)
                if not rt:
                    self.setLog(md5Id,self.reencode(item),status='failed',
                                info=self.msg[code])
                continue
                self.setLog(md5Id,item,title=self.reencode(lPath[0]),url=url,
                            info=self.msg[code])


    def buildTree (self, zFile, md5Id):
        """ Build the tree matching zFile """
        putils = getToolByName(self, 'plone_utils')
        error = False

        # if the user wants a saved report
        if 'build_report' in self.request.keys() and self.request['build_report']:
            self.wannaReport[md5Id] = True
            self.initReport(md5Id) 
        else:
            self.wannaReport[md5Id] = False

        self.winPatch(zFile,md5Id)
        for item in zFile.namelist():
            normalizeItem = self.reencode(item)
            rPath = []
            lPath = item.split('/')
            title,isFolder = self.getFileTitle(item,lPath) 
            if not isFolder:
                isCorrectSize,size = self.validateFile(item,zFile)
                if not isCorrectSize:
                    self.setLog(md5Id,normalizeItem,size=size,status='failed',
                                info=_(u'ml_py_maxsize',u'File size exceeds the maximal size defined in the configuration'))
                    error = True
                    continue 
            id = self.safeNormalize(putils,title)
            container = self.getContainer(lPath,title)
            title= self.reencode(title)
            if not container:
                self.setLog(md5Id,normalizeItem,size=size,status='failed',
                        info=_(u'ml_py_noparent',u'Unable to find parent object'))
                error = True
                continue 
            rt,code,url,size = self.createObject(id,isFolder,title,container,
                                                zFile,item)
            if not rt:
                self.setLog(md5Id,normalizeItem,size=size,status='failed',
                            info=self.msg[code])
                error = True
                continue
            self.setLog(md5Id,normalizeItem,title,size,url,info=self.msg[code])
        if self.wannaReport[md5Id]:
            if not self.finalizeReport(self.request['up_file'].filename,md5Id):
                return 'noReport'
        if error:
            return 'generalError'
        else:
            return 'success'


    def outMassLoader (self, out, url):
        """ Add a portal message within the return status """
        putils = getToolByName(self, 'plone_utils')
        putils.addPortalMessage(out)
        self.request.RESPONSE.redirect(url)


    def uniqueId (self, mlist):
        """ Generate a unique ID to identifiate each file contained
            into the zip file.
        """
        import md5
        return md5.new('-'.join(mlist)).hexdigest()


    def runMassLoader (self):
        """ runMassLoader """
        zf,md5Id = self.loadZipFile()
        curl = self.context.absolute_url()
        if isinstance(zf,ZipFile):
            code = self.buildTree(zf,md5Id)
            out = self.msg[code]
            url = curl+'/@@massloader_result?log='+md5Id
        else:
            out = self.msg[zf]
            url = curl+'/@@massloader_import'
        self.outMassLoader(out,url)


class MassLoaderActionProvider (BrowserView):

    def __init__ (self, context, request):
        self.request = request
        self.context = context
    
    @property
    def _options (self):
        _siteroot = queryUtility (IPloneSiteRoot)
        return IMassLoaderSchema (_siteroot)
    
    def showMassLoaderAction (self):
        """ Return True if the context is a selected content types in Settings
        """
        if self.context.portal_type in getattr (self._options, 'massloader_possible_types', []):
            return True
        else:
            return False
