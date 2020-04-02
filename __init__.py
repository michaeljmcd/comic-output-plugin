from __future__ import print_function
from calibre.customize.conversion import OutputFormatPlugin
from calibre.ptempfile import PersistentTemporaryDirectory
from calibre import CurrentDir
import os, re, shutil

class ComicOutputPlugin(OutputFormatPlugin):
    name = 'Comic Output Plugin'
    description = 'Extracts images from an ebook and creates a CBZ comic archive from them.'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Michael McDermott'
    version = (1, 0, 1)

    file_type = 'cbz'

    def convert(self, oeb_book, output_path, input_plugin, opts, log):
        from calibre.utils import zipfile
        from templite import Templite
        from lxml import etree

        image_types = ['image/jpeg', 'image/png']

        tempdir = os.path.realpath(PersistentTemporaryDirectory())

        log.info('Creating temp dir ' + tempdir)

        with CurrentDir(tempdir):
            cover_ref = None
            cover_ext = None

            if oeb_book.guide['cover'] is not None:
                cover_ref = oeb_book.guide['cover'].href
                orig_name, file_extension = os.path.splitext(cover_ref)
                cover_ext = file_extension
                
            for item in oeb_book.manifest:
                if item.media_type in image_types:
                    log.info('Found image ' + item.id + ' ' + item.media_type + ' ' + item.href)

                    if cover_ref is not None and item.href == cover_ref:
                        file_name = os.path.join(tempdir, '00000' + cover_ext)
                    else:
                        file_name = os.path.join(tempdir, os.path.basename(item.href))

                    with open(file_name, 'wb') as image:
                        image.write(item.data)

        log.info('Finished extracting images, repackaging them as CBZ ' + output_path)

        zfile = zipfile.ZipFile(output_path, mode="w")
        zfile.add_dir(tempdir)
        log.info('Added files. Preparing to compress.')

        log.info('Cleaning up temp dir...')
        shutil.rmtree(tempdir)
        log.info('All done.')
