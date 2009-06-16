# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice, Bool, List
from zope.formlib import form

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.fieldsets.fieldsets import FormFieldsets
from atreal.massloader import MassLoaderMessageFactory as _
from plone.app.controlpanel.form import ControlPanelForm

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

MASSLOADER_OPTION_TYPE = {
    _(u"Option 3 - Based on Content Type Registry"): 'opt3',
    _(u"Option 1 - Based on two Content Types : Image and File"): 'opt1',
    _(u"Option 2 - Based on only one Content Type : File"): 'opt2',

}

MASSLOADER_OPTION_TYPE_VOCABULARY = SimpleVocabulary(
    [SimpleTerm(v, v, k) for k, v in MASSLOADER_OPTION_TYPE.items()]
    )


class IMassLoaderMainSchema(Interface):

    massloader_possible_types = List(
        title = _(u'ml_label_possible_types',
                  default=u"MassLoader Aware Types"),
        required = False,
        default = ['Large Plone Folder', 'Plone Site', 'Folder'],
        description = _(u"ml_help_possible_types",
                        default=u"Content Type where we can use MassLoader on it. Of course, you have to selected only Folderish Content Types in order to see MassLoader run correctly."),
        value_type = Choice( title=u"ml_label_possible_types", source="plone.app.vocabularies.PortalTypes" )
        )
    
    massloader_keywords_enable = Bool(
        title=_(u'ml_label_keywords_enable',
                default=u"Enable Keywords and Description transfert ?"),
        description=_(u"ml_help_keywords_enable",
                      default=u"This option allows you to apply the description and the keywords of the folder in which one you import the zip file with all the new objects created. If the object is already exists : the description and keywords will not be applied."),
        default=False,
        required=True)
    
    massloader_max_file_size = TextLine(
        title=_(u'ml_label_max_file_size',
                default=u"Limit size of each file in the zip file (in MegaBytes)"),
        description=_(u"ml_help_max_file_size",
                      default=u"Each file contained in the zip file must fit this maximum size. If the size exceeds this limit, the object will not be created."),
        default=u'20',
        required=True)
    
class IMassLoaderTypesSchema(Interface):

    massloader_option_type = Choice(
        title=_(u'ml_label_option_type',
                default=u"Option for portal type construction"),
        description=_(u"ml_help_option_type",
                      default=u"Option 1 : The portal type that receive the object will be based on the two follow-up options, "
                      u"Option 2 : The portal type that receive the object will be based on the second one follow-up option, "
                      u"Option 3 : The choice of the portal type that receive the object will be based on the Content Type Registry (in ZMI). Be aware that checking this option will disable the 2 follow-up options."),
        default=u'opt1',
        vocabulary=MASSLOADER_OPTION_TYPE_VOCABULARY,
        required=True)
   
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

class IMassLoaderSchema(IMassLoaderMainSchema, IMassLoaderTypesSchema):
    """
    """

class MassLoaderControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IMassLoaderSchema)

    def __init__(self, context):
        super(MassLoaderControlPanelAdapter, self).__init__(context)

    massloader_option_type = ProxyFieldProperty(IMassLoaderSchema['massloader_option_type'])
    massloader_possible_types = ProxyFieldProperty(IMassLoaderSchema['massloader_possible_types'])
    massloader_max_file_size = ProxyFieldProperty(IMassLoaderSchema['massloader_max_file_size'])
    massloader_image_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_image_portal_type'])
    massloader_file_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_file_portal_type'])
    massloader_keywords_enable = ProxyFieldProperty(IMassLoaderSchema['massloader_keywords_enable'])

ml_mainset = FormFieldsets(IMassLoaderMainSchema)
ml_mainset.id = 'main'
ml_mainset.label = _(u'label_rfs_main', default=u'Main')

ml_typesset = FormFieldsets(IMassLoaderTypesSchema)
ml_typesset.id = 'types'
ml_typesset.label = _(u'label_ml_types', default=u'Types')
    
class MassLoaderControlPanel(ControlPanelForm):
    
    form_fields = FormFieldsets(ml_mainset, ml_typesset)
    
    label = _("MassLoader settings")
    description = _("MassLoader settings for this site.")
    form_name = _("MassLoader settings")
