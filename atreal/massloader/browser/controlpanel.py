# -*- coding: utf-8 -*-

from atreal.massloader import MassLoaderMessageFactory as _
from plone.app.registry.browser import controlpanel
from Products.CMFPlone.interfaces import IPloneSiteRoot

from zope.component import adapts
from zope.interface import Interface, implements
from zope.schema import Bool, Choice, List, Text, TextLine


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
        default = ['Plone Site', 'Folder'],
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


class MassLoaderControlPanelForm(controlpanel.RegistryEditForm):

    schema = IMassLoaderSchema
    label = _("MassLoader settings")
    description = _("MassLoader settings for this site.")


class MassLoaderControlPanel(controlpanel.ControlPanelFormWrapper):
    implements(IMassLoaderSchema)
    form = MassLoaderControlPanelForm
