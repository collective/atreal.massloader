# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice, Bool, List
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
                      default=u"Each file contained in the zip file must fit this maximum size. If the size exceeds this limit, the object will not be created."),
        default=u'20',
        required=True)

    massloader_ctr_enabled = Bool(
        title=_(u'ml_label_ctr_enabled',
                default=u"Portal type based on Content Type Registry ?"),
        description=_(u"ml_help_ctr_enabled",
                      default=u"If checked, the choice of the portal type that receive the object will be based on the Content Type Registry (in ZMI). Be aware that checking this option will disable the 2 follow-up options."),
        default=True,)
   
    massloader_image_portal_type = Choice(
        title=_(u'ml_label_image_portal_type',
                default=u"Portal Type for image"),
        description=_(u"ml_help_image_portal_type",
                      default=u"The portal type you want in order to create images. Be aware that the content type must implement setImage."),
        default=u'Image',
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        required=True)
    
    massloader_file_portal_type = Choice(
        title=_(u'ml_label_file_portal_type',
                default=u"Portal Type for file"),
        description=_(u"ml_help_file_portal_type",
                      default=u"The portal type you want in order to create files. Be aware that the content type must implement setFile."),
        default=u'File',
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        required=True)

    massloader_keywords_enable = Bool(
        title=_(u'ml_label_keywords_enable',
                default=u"Enable Keywords and Description transfert ?"),
        description=_(u"ml_help_keywords_enable",
                      default=u"This option allows you to apply the description and the keywords of the folder in which one you import the zip file with all the new objects created. If the object is already exists : the description and keywords will not be applied."),
        default=False,
        required=True)

    massloader_possible_types = List(
        title = _(u'ml_label_possible_types',
                  default=u"MassLoader Aware Types"),
        required = False,
        default = ['Large Plone Folder', 'Plone Site', 'Folder'],
        description = _(u"ml_help_possible_types",
                        default=u"Content Type where we can use MassLoader on it. Of course, you have to selected only Folderish Content Types in order to see MassLoader run correctly."),
        value_type = Choice( title=u"ml_label_possible_types", source="plone.app.vocabularies.PortalTypes" )
        )

class MassLoaderControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IMassLoaderSchema)

    def __init__(self, context):
        super(MassLoaderControlPanelAdapter, self).__init__(context)

    massloader_max_file_size = ProxyFieldProperty(IMassLoaderSchema['massloader_max_file_size'])
    massloader_ctr_enabled = ProxyFieldProperty(IMassLoaderSchema['massloader_ctr_enabled'])
    massloader_image_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_image_portal_type'])
    massloader_file_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_file_portal_type'])
    massloader_keywords_enable = ProxyFieldProperty(IMassLoaderSchema['massloader_keywords_enable'])
    massloader_possible_types = ProxyFieldProperty(IMassLoaderSchema['massloader_possible_types'])
    
class MassLoaderControlPanel(ControlPanelForm):
    form_fields = form.FormFields(IMassLoaderSchema)
    label = _("MassLoader settings")
    description = _("MassLoader settings for this site.")
    form_name = _("MassLoader settings")
