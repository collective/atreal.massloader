# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Text, Choice, Bool, List
from zope.formlib import form

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from atreal.massloader import MassLoaderMessageFactory as _
from plone.app.controlpanel.form import ControlPanelForm


class IMassLoaderSchema(Interface):

    massloader_max_file_size = TextLine(
        title=_(u'ml_label_max_file_size',
            default=u"Limit size of each file in the zip file (in MegaBytes)"),
        description=_(u"ml_help_max_file_size",
            default=u"Each file contained in the zip file must fit this maximum\
                size. If the size exceeds this limit, the object will not be created."),
        default=u'20',
        required=True)

    massloader_possible_types = List(
        title = _(u'ml_label_possible_types',
            default=u"MassLoader Aware Types"),
        required = False,
        default = ['Large Plone Folder', 'Plone Site', 'Folder'],
        description = _(u"ml_help_possible_types",
            default=u"Content Type where we can use MassLoader on it. Of course,\
                you have to selected only Folderish Content Types in order to \
                see MassLoader run correctly."),
        value_type = Choice(
            title=u"ml_label_possible_types",
            source="plone.app.vocabularies.PortalTypes"))

    massloader_image_like_file = Bool(
        title=_(u'ml_label_image_like_file',
            default=u"Treat Images like Files"),
        description=_(u"ml_help_image_like_file",
            default=u"In order to create Images as Portal Type Files."),
        default=False,
        required=False)

    massloader_file_portal_type = Choice(
        title=_(u'ml_label_file_portal_type',
            default=u"Portal Type for file"),
        description=_(u"ml_help_file_portal_type",
            default=u"The portal type you want in order to create files. \
                Be aware that the content type must implement setFile."),
        default=u'File',
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        required=False)

    massloader_folder_portal_type = Choice(
        title=_(u'ml_label_folder_portal_type',
            default=u"Portal Type for folder"),
        description=_(u"ml_help_folder_portal_type",
            default=u"The portal type you want in order to create folders. \
                Be aware that the content type must be folderish and allow the \
                file type selected."),
        default=u'Folder',
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        required=False)

    massloader_additional_fields = Text(
        title=_(u'ml_label_additional_fields',
                default=u"Additional Fields"),
        description=_(u"ml_help_additional_fields",
                      default=u"One by line"),
        default=u'',
        required=False)


class MassLoaderControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IMassLoaderSchema)

    def __init__(self, context):
        super(MassLoaderControlPanelAdapter, self).__init__(context)

    massloader_possible_types = ProxyFieldProperty(IMassLoaderSchema['massloader_possible_types'])
    massloader_max_file_size = ProxyFieldProperty(IMassLoaderSchema['massloader_max_file_size'])
    massloader_image_like_file = ProxyFieldProperty(IMassLoaderSchema['massloader_image_like_file'])
    massloader_file_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_file_portal_type'])
    massloader_folder_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_folder_portal_type'])
    massloader_additional_fields = ProxyFieldProperty(IMassLoaderSchema['massloader_additional_fields'])


class MassLoaderControlPanel(ControlPanelForm):

    form_fields = form.FormFields(IMassLoaderSchema)

    label = _("MassLoader settings")
    description = _("MassLoader settings for this site.")
    form_name = _("MassLoader settings")
