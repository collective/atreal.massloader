=================
atreal.massloader
=================

.. contents::


Overview
========
MassLoader allows to do massive uploads via Zip or 7Zip files. When an archive
is uploaded via MassLoader, its contents are created in the current folder.

* `Project Page @ Plone <http://plone.org/products/massloader>`_
* `Source code @ GitHub <https://github.com/collective/atreal.massloader>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/atreal.massloader>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/collective/atreal.massloader>`_


Description
===========

* MassLoader creates Files and Images or only Files with files in archive.
* MassLoader add an action on Folder, Large Plone Folder and Plone Site. You can
  change theses portal types in the control panel.
* MassLoader has a content size limit, and is able to protect your server from
  logic bombs.
* MassLoader can handle any size of archive file, without overload of your server.


Important
=========

* The permission is only set by default to the role 'Manager' and 'Owner'.
* From the version 3.0.0beta1, the portal type of new object can be managed via
  2 mechanisms, selectable in the control panel :
  
  * If content type registry detects an Image, MassLoader creates an Image, if
    it's not an image MassLoader creates a file with the portal type selected
    in Control Panel.
  * Or the checkbox is checked in Control Panel and Massloader creates only
    files with the portal type selected in Control Panel/

* Default max size for each file to be uncompressed is set to 20 Mb. You can
  modify this size limit in the control panel.
* If a folder with a same id already exists, it is conserved. If a same file
  exists whith the same id, just the datas are updated.


Issues
======

* 7zip archives are not valid when they contain only empty folders (problem with
  python library pylzma).
* 7zip archives with empty folders : the empty folders are not created.


Installation
============

To install atreal.massloader into the global Python environment (or a workingenv),
using a traditional Zope 2 instance, you can do this:

 * When you're reading this you have probably already run 
   ``easy_install atreal.massloader``. Find out how to install setuptools
   (and EasyInstall) here:
   http://peak.telecommunity.com/DevCenter/EasyInstall

 * If you are using Zope 2.9 (not 2.10), get `pythonproducts`_ and install it 
   via::

       python setup.py install --home /path/to/instance

   into your Zope instance.

 * Create a file called ``atreal.massloader-configure.zcml`` in the
   ``/path/to/instance/etc/package-includes`` directory.  The file
   should only contain this::

       <include package="atreal.massloader" />

.. _pythonproducts: http://plone.org/products/pythonproducts


Alternatively, if you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

 * Add ``atreal.massloader`` to the list of eggs to install, e.g.:
 
    [buildout]
    ...
    eggs =
        ...
        atreal.massloader
        
  * Tell the plone.recipe.zope2instance recipe to install a ZCML slug:
  
    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        atreal.massloader
        
  * Re-run buildout, e.g. with:
  
    $ ./bin/buildout
        
You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.


Authors
=======

|atreal|_

* `atReal Team`_

  - Matthias Broquet [tiazma]
  - Florent Michon [fmichon]

.. |atreal| image:: http://www.atreal.fr/medias/atreal-logo-48.png
.. _atreal: http://www.atreal.fr/
.. _atReal Team: mailto:contact@atreal.fr


Contributors
============

* `atReal Team`_

  - Romain BEYLERIAN [rbeylerian]

  .. _atReal Team: mailto:contact@atreal.fr


Credits
=======

* Sponsorised by ML-COM - www.ml-com.com (and some international research labs)
* Sponsorised by City of Albi (Fr), www.mairie-albi.fr
