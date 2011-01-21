import transaction

from zope.interface import implements
from zope.component import queryUtility

from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from atreal.massloader import MassLoaderMessageFactory as _
from atreal.massloader.interfaces import IMassLoader, IArchiveUtility
from atreal.massloader.browser.controlpanel import IMassLoaderSchema

NOUPLOADFILE = 1
NOCORRECTFILE = 2
EXCEEDEDFILESIZE = 3
NOPARENT = 4
FOLDERALREADYEXISTS = 5
FOLDERCREATEOK = 6
FOLDERCREATEERROR = 7
CREATEOK = 8
CREATEERROR = 9
UPDATEOK = 10
UPDATEERROR = 11
GENERALOK = 12
GENERALERROR = 13


class MassLoader(object):
    """
    """

    implements(IMassLoader)

    encoding = 'cp850'

    msg = {
        NOUPLOADFILE: _(u"ml_py_noUpFile", u"Uploaded file doesn't exist"),
        NOCORRECTFILE: _(u"ml_py_notZipFile", u"Uploaded file is not a valid "
                         "zip file"),
        EXCEEDEDFILESIZE: _(u"ml_py_maxsize", u"File size exceeds the maximal "
                            "size defined in the configuration"),
        NOPARENT: _(u"ml_py_noparent", u"Unable to find parent object"),
        FOLDERALREADYEXISTS: _(u"ml_py_folderExisted", u"Folder Already "
                               "Exists"),
        FOLDERCREATEOK: _(u"ml_py_folderOK", u"Folder created"),
        FOLDERCREATEERROR: _(u"ml_py_createFolderError", u"Error while "
                             "creating folder"),
        CREATEOK: _(u"ml_py_createOK", u"File created"),
        CREATEERROR: _(u"ml_py_createError", u"Error while creating object"),
        UPDATEOK: _(u"ml_py_updateOK", u"File updated"),
        UPDATEERROR: _(u"ml_py_updateError", u"Error while updating object"),
        GENERALOK: _(u"ml_py_success", u"All files were successfully loaded"),
        GENERALERROR: _(u"ml_py_generalError", u"Some errors occured while "
                        "loading files"),
        }

    def __init__(self, context):
        """
        """
        #
        self.context = context
        self.log = []
        self.archive = None
        self.domain = 'atreal.massloader'
        #
        self.putils = getToolByName(self.context, 'plone_utils')
        self.ptypes = getToolByName(self.context, 'portal_types')
        self.mtr = getToolByName(self.context, 'mimetypes_registry')
        self.ctr = getToolByName(self.context, 'content_type_registry')
        self.pc = getToolByName(self.context, 'portal_catalog')
        self.translate = getToolByName(self.context,
                                       'translation_service').utranslate
        #
        props = getToolByName(self.context, 'portal_properties')
        stp = props.site_properties
        self.view_types = stp.getProperty('typesUseViewActionInListings', ())

    @property
    def _options(self):
        """
        """
        _siteroot = queryUtility(IPloneSiteRoot)
        return IMassLoaderSchema(_siteroot)

    def available(self):
        """
        """
        if self.context.portal_type not in self.portalTypesAware():
            return False
        return True

    @property
    def getMaxFileSize(self):
        """ Return the maxFileSize from Settings
        """
        return int(getattr(self._options, 'massloader_max_file_size',
                           '20')) * 1000000L

    def portalTypesAware(self):
        """
        """
        return getattr(self._options, 'massloader_possible_types', [])

    def getAdditionalFields(self):
        """
        """
        additional = getattr(self._options, 'massloader_additional_fields', '')
        if additional is None or additional == '':
            return []
        return additional.split('\n')

    def portalTypeForFolder(self):
        """
        """
        return getattr(self._options, 'massloader_folder_portal_type', 'Folder')

    def portalTypeForFile(self, filename, mimetype):
        """
        """
        if not self.treatImageLikeFile():
            type = self.ctr.findTypeName(filename, mimetype, None)
            if type == 'Image':
                return type
        return getattr(self._options, 'massloader_file_portal_type', 'File')

    def treatImageLikeFile(self):
        """
        """
        return getattr(self._options, 'massloader_image_like_file', False)

    def _reencode(self, txt):
        """
        """
        try:
            return txt.decode('utf-8')
        except:
            return txt.decode(self.encoding)

    def _safeNormalize(self, txt):
        """
        """
        #
        while txt.startswith('_'):
            txt = txt[1:]
        #
        try:
            return self.putils.normalizeString(txt)
        except:
            return self.putils.normalizeString(unicode(txt, self.encoding))

    def _log(self, filename, title=(u"N/A"), size='0', url='',
             status=_(u"Failed"), info=None):
        """
        """
        #
        if info is not None and self.msg.has_key(info):
            info = self.msg[info]
        else:
            info = u""

        #
        entry = {'filename': filename,
                 'title': title,
                 'size': size,
                 'url': url,
                 'status': self._translate(status),
                 'info': self._translate(info), }

        #
        self.log.append(entry)

    def _translate(self, elem):
        """
        """
        return self.translate(self.domain, elem, context=self.context)

    def _printLog(self):
        """
        """
        #
        tabHead = ' <table class="listing" \
                   tal:attributes="summary string:Import results" \
                   tal:condition="python:results"> \
              <tr> \
                <th>'+self._translate(_(u"Original file name"))+'</th>\
                <th>'+self._translate(_(u"Direct Link"))+'</th>\
                <th>'+self._translate(_(u"Size"))+'</th>\
                <th>'+self._translate(_(u"Status"))+'</th>\
                <th>'+self._translate(_(u"Notes"))+'</th>\
              </tr>\
        '
        #
        tabBody = ''
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
        for entry in self.log:
            values = [entry[item] for item in ['filename', 'url', 'title',
                                               'size', 'status', 'info']]
            tabBody += tabLine % tuple(values)
        #
        tabFooter = '</table>\
        '
        #
        return u"" + tabHead + tabBody + tabFooter

    def _getContainer(self, path, item):
        """ Return the container object
        """
        # We get the index of item in path
        lenPath = len(path)
        if path[lenPath - 1]!='':
            ind = lenPath - 1
        else:
            ind = lenPath - 2

        # Index is 0, container is the context
        if not ind:
            return self.context
        # Index is not 0, search of container
        else:
            # We construct the query
            query = {}
            # We normalize the path
            normPath = [self._safeNormalize(item) for item in path[:ind]]
            queryPath = '/'.join(list(self.context.getPhysicalPath())+normPath)
            query['path'] = {'query': queryPath, 'depth': 0}
            # Id of the container, previous element in path
            query['getId'] = self._safeNormalize(path[ind-1])
            # We search an object with path and id
            brain = self.pc(query)
            # One match : everything is ok, we return the object container
            if len(brain) == 1:
                return brain[0].getObject()
            # We have to create the parents
            else:
                container = self._getContainer(path[:ind], path[ind-1])
                id = self._safeNormalize(path[ind-1])
                title = self._reencode(path[ind-1])
                isFolder = True
                rt, code, url, size = self._createObject(id,
                                                         isFolder,
                                                         title,
                                                         container,
                                                         id)
                if not rt:
                    self._log(self._reencode('/'.join(path[:ind]))+'/',
                              info=code)
                else:
                    self._log(self._reencode('/'.join(path[:ind]))+'/', title,
                              status=_(u"Ok"), url=url, info=code)
                return self._getContainer(path, item)

    def _checkFileSize(self, name=None):
        """
        """
        if name is None:
            return
        if self.archive.sizeFileByName(name) > self.getMaxFileSize:
            return False
        return True

    def _setData(self, obj, data, filename):
        """
        """
        #
        if type(filename) == unicode:
            filename = filename.encode('utf-8')

        #
        if obj.portal_type == 'Image':
            try:
                obj.setImage(data, filename=filename)
            except:
                return False
        else:
            try:
                obj.setFile(data, filename=filename)
            except:
                return False

    def _loadAdditionnalsFields(self, obj):
        """
        """
        for field in self.getAdditionalFields():
            #
            if getattr(self.context, 'getField', None) is None:
                continue
            getfield = self.context.getField(field) or self.context.getField(field.lower())
            if getfield is None:
                continue
            getfield = getfield.getAccessor(self.context)
            #
            if getattr(obj, 'getField', None) is None:
                continue
            setfield = obj.getField(field) or obj.getField(field.lower())
            if setfield is None:
                continue
            setfield = setfield.getMutator(obj)
            #
            setfield(getfield())

    def _createObject(self, id, isFolder, title, container, filename):
        """ Create the object
        """
        if isFolder:
            if id in container.keys():
                # Object already exists, it's a folder we keep it without change
                obj = container[id]
                code = FOLDERALREADYEXISTS
            else:
                # Object not exists, we have to create it
                try:
                    # Object Construction
                    type = self.portalTypeForFolder()
                    self.ptypes.constructContent(type_name=type,
                                                 container=container,
                                                 id=id,
                                                 title=title)
                    obj = container[id]
                    #
                    self._loadAdditionnalsFields(obj)
                    #
                    obj.reindexObject()
                    #
                    code = FOLDERCREATEOK
                except:
                    #
                    return False, FOLDERCREATEERROR, None, ""
        else:
            if id in container.keys():
                # Object already exists, it's not a folder, we have to update it
                try:
                    # Update
                    obj = container[id]
                    #
                    data = self.archive.readFileByName(filename)
                    #
                    if self._setData(obj, data, filename) is False:
                        return False, UPDATEERROR, None, ""
                    #
                    obj.reindexObject()
                    #
                    transaction.savepoint(optimistic=True)
                    notify(ObjectModifiedEvent(obj))
                    #
                    code = UPDATEOK
                except:
                    #
                    return False, UPDATEERROR, None, ""
            else:
                # Object not exists, we have to create it
                try:
                    # Object Construction
                    mimetype = self.archive.mimetypeFileByName(filename)
                    type = self.portalTypeForFile(filename, mimetype)
                    self.ptypes.constructContent(type_name=type,
                                                 container=container,
                                                 id=id,
                                                 title=title)
                    obj = container[id]
                    #
                    self._loadAdditionnalsFields(obj)
                    #
                    data = self.archive.readFileByName(filename)
                    if self._setData(obj, data, filename) is False:
                        return False, CREATEERROR, None, ""
                    obj.setFormat(mimetype)
                    #
                    obj.reindexObject()
                    #
                    transaction.savepoint(optimistic=True)
                    notify(ObjectCreatedEvent(obj))
                    #
                    code = CREATEOK
                except:
                    #
                    return False, CREATEERROR, None, ""

        #
        url = obj.absolute_url()
        if obj.portal_type in self.view_types:
            url += '/view'
        return True, code, url, obj.getObjSize()

    def process(self, fileupload=None, wantreport=False):
        """
        """
        #
        error = False

        #
        self.archive = queryUtility(IArchiveUtility).initialize(fileupload)
        if self.archive is None:
            return self.msg[NOCORRECTFILE], ''

        #
        for item in self.archive.listContent():
            #
            normalizeItem = self._reencode(item)

            #
            path = item.split('/')
            if item.endswith('/'):
                title = path[len(path) - 2]
                isFolder = True
            else:
                title = path[len(path) - 1]
                isFolder = False

            # We check the size of the file
            if not isFolder and not self._checkFileSize(item):
                self._log(normalizeItem, info=EXCEEDEDFILESIZE)
                error = True
                continue

            # We check the container
            container = self._getContainer(path, title)
            if not container:
                self._log(normalizeItem, info=NOPARENT)
                error = True
                continue

            # We create or update the object
            id = self._safeNormalize(title)
            title = self._reencode(title)
            rt, code, url, size = self._createObject(id,
                                                     isFolder,
                                                     title,
                                                     container,
                                                     item)
            if not rt:
                self._log(normalizeItem, info=code)
                error = True
                continue
            self._log(normalizeItem, status=_(u"Ok"), title=title, size=size,
                      url=url, info=code)

        # We create or update the report
        if wantreport:
            filename = fileupload.filename
            id = 'report-'+self._safeNormalize(filename)
            if not self.context.hasObject(id):
                alreadyexists = False
                self.ptypes.constructContent(type_name='Document',
                                             container=self.context, id=id)
            else:
                alreadyexists = True
            report = self.context[id]
            text = self._printLog()
            if alreadyexists:
                text += report.getText().decode('utf-8')
            else:
                title = self._translate(_('Report'))
                report.setTitle(title + ' ' + filename)
                desc = self._translate(_('Import report for the zip file'))
                report.setDescription(desc + ' ' + filename)
            report.setText(text)
            report.reindexObject()

        # Return
        if error:
            return self.msg[GENERALERROR], self._printLog()
        else:
            return self.msg[GENERALOK], self._printLog()
