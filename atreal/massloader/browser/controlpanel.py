from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice
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

class MassLoaderControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IMassLoaderSchema)

    def __init__(self, context):
        super(MassLoaderControlPanelAdapter, self).__init__(context)

    massloader_max_file_size = ProxyFieldProperty(IMassLoaderSchema['massloader_max_file_size'])
    massloader_image_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_image_portal_type'])
    massloader_file_portal_type = ProxyFieldProperty(IMassLoaderSchema['massloader_file_portal_type'])
    
class MassLoaderControlPanel(ControlPanelForm):
    form_fields = form.FormFields(IMassLoaderSchema)
    label = _("MassLoader settings")
    description = _("MassLoader settings for this site.")
    form_name = _("MassLoader settings")
