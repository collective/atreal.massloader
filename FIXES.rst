Fixes
========================
2013-10-03
------------------------
Fix description
~~~~~~~~~~~~~~~~~~~~~~~~
The original version of massloader used own "safe" id's, which were used
in the slugs when creating a file. This doesn't seem to be a standard Plone
behaviour, thus, we fall back to normal P

2013-10-01
------------------------
Fix description
~~~~~~~~~~~~~~~~~~~~~~~~
The original version of massloader wasn't saving the filename which comes 
from archive properly. After some debugging, the following has been found:

In section `# Object not exists, we have to create it` of method 
`atreal.massloader.adapter.MassLoader._createObject` near line 376,
right after the following code

>>> if self._setData(obj, data, filename) is False:
>>>     return False, CREATEERROR, None, ""

add the following line:

>>> obj.setFilename(filename)

Fixed by
~~~~~~~~~~~~~~~~~~~~~~~~
Artur Barseghyan