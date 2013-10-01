================================
atreal.massloader Package Readme
================================

Overview
--------
MassLoader allows to do massive uploads via Zip or 7Zip files. When an archive
is uploaded via MassLoader, its contents are created in the current folder.

Description
-----------

* MassLoader creates Files and Images or only Files with files in archive.
* MassLoader add an action on Folder, Large Plone Folder and Plone Site. You can
change theses portal types in the control panel.
* MassLoader has a content size limit, and is able to protect your server from
logic bombs.
* MassLoader can handle any size of archive file, without overload of your server.


Important
---------

* The permission is only set by default to the role 'Manager' and 'Owner'.
* From the version 3.0.0beta1, the portal type of new object can be managed via
2 mechanisms, selectable in the control panel :
  * If content type registry detects an Image, MassLoader creates an Image, if
    it's not an image MassLoader creates a file with the portal type selected
    in Control Panel
  * Or the checkbox is checked in Control Panel and Massloader creates only
    files with the portal type selected in Control Panel
* Default max size for each file to be uncompressed is set to 20 Mb. You can
modify this size limit in the control panel.
* If a folder with a same id already exists, it is conserved. If a same file
exists whith the same id, just the datas are updated.


Issues
------

* 7zip archives are not valid when they contain only empty folders (problem with
python library pylzma)
* 7zip archives with empty folders : the empty folders are not created


Authors
-------

:atReal Team - contac@atreal.net :
    Matthias Broquet <tiazma>
    Florent Michon <f10w>


Credits
-------

* Sponsorised by ML-COM - www.ml-com.com (and some international research labs)
* Sponsorised by City of Albi (Fr), www.mairie-albi.fr




