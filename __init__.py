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

        page_no = 0

        with CurrentDir(tempdir):
            for item in oeb_book.manifest:
                if item.media_type in image_types:
                    log.info('Found image ' + item.id + ' ' + item.media_type + ' ' + item.href)

                    file_name = os.path.join(tempdir, os.path.basename(item.href))
                    with open(file_name, 'wb') as image:
                        image.write(item.data)

        log.info('Finished extracting images, repackaging them as CBZ ' + output_path)

        zfile = zipfile.ZipFile(output_path, mode="w")
        zfile.add_dir(tempdir, '/')
        log.info('Added files. Preparing to compress.')

        zfile.write(output_path, os.path.basename(output_path), zipfile.ZIP_DEFLATED)

        log.info('Cleaning up temp dir...')
        shutil.rmtree(tempdir)
        log.info('All done.')
