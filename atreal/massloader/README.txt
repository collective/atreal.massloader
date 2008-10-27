MassLoader allows to do massive uploads via Zip files. When a zip file is uploaded via MassLoader, 
its contents are created in the current folder.  

MassLoader is developed in a zope3/Five way. It respects the Plone architecture.

    * MassLoader relies on mimetypes_registry in order to check the content file. 
      Therefore, MassLoader is able to find what kind of content is a file, even 
      if the file doesn't have any extension, based on the file's content.
        
    * MassLoader is developed in a zope3/Five way. It adapts Folder in order to provide its new action.

    * MassLoader has a content size limit, and is able to protect your server from logic bombs.

    * MassLoader can handle any size of zip file, without overload of your server.

::IMPORTANT::

* The permission is only set by default to the role 'Manager' and 'Owner'.

* In this actual version, portal type of object created are just "Image" or "File".

* Default max size for each file to be uncompressed is set to 20 Mb. 
You can modify this size limit in the control panel.

* If a folder with a same id already exists, it is conserved. If a same file exists whith the same id, just the datas
are updated. 
