import re

from plone.i18n.normalizer import cropName
from plone.i18n.normalizer.base import baseNormalize
from plone.i18n.normalizer.interfaces import IURLNormalizer

from zope.component import queryUtility
from zope.interface import implements

# Define and compile static regexes
FILENAME_REGEX = re.compile(r"^(.+)\.(\w{,4})$")
IGNORE_REGEX = re.compile(r"['\"]")
NON_WORD_REGEX = re.compile(r"[\W\-]+")
DANGEROUS_CHARS_REGEX = re.compile(r"[!$%&()*+,/:;<=>?@\\^{|}\[\]~`]+")
URL_DANGEROUS_CHARS_REGEX = re.compile(r"[!#$%&()*+,/:;<=>?@\\^{|}\[\]~`]+")
MULTIPLE_DASHES_REGEX = re.compile(r"\-+")
EXTRA_DASHES_REGEX = re.compile(r"(^\-+)|(\-+$)")
UNDERSCORE_START_REGEX = re.compile(r"(^_+)(.*)$")
# Define static constraints
MAX_LENGTH = 50
MAX_FILENAME_LENGTH = 1023
MAX_URL_LENGTH = 255

class URLNormalizer(object):
    """
    Behaves exactly like ``plone.i18n.normalizer.URLNormalizer`` but doesn't transform ``text`` to lowercase.
    """
    implements(IURLNormalizer)

    def normalize(self, text, locale=None, max_length=MAX_URL_LENGTH):
        """
        Returns a normalized text. text has to be a unicode string and locale
        should be a normal locale, for example: 'pt_BR', 'sr@Latn' or 'de'
        """
        #import logging
        #logger = logging.getLogger('Plone')
        #logger.info('My ``URLNormalizer`` is used!')
        if locale is not None:
            # Try to get a normalizer for the locale
            util = queryUtility(IURLNormalizer, name=locale)
            parts = locale.split('_')
            if util is None and len(parts) > 1:
                # Try to get a normalizer for the base language if we asked
                # for one for a language/country combination and found none
                util = queryUtility(IURLNormalizer, name=parts[0])
            if util is not None:
                text = util.normalize(text, locale=locale)

        text = baseNormalize(text)

        # lowercase text
        #base = text.lower()
        base = text
        ext  = ''

        m = FILENAME_REGEX.match(base)
        if m is not None:
            base = m.groups()[0]
            ext  = m.groups()[1]

        base = base.replace(' ', '-')
        base = IGNORE_REGEX.sub('', base)
        base = URL_DANGEROUS_CHARS_REGEX.sub('-', base)
        base = EXTRA_DASHES_REGEX.sub('', base)
        base = MULTIPLE_DASHES_REGEX.sub('-', base)

        base = cropName(base, maxLength=max_length)

        if ext != '':
            base = base + '.' + ext

        return base

urlnormalizer = URLNormalizer()
