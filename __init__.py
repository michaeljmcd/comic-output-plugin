from __future__ import print_function
from calibre.customize.conversion import OutputFormatPlugin
from calibre.ptempfile import PersistentTemporaryDirectory
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

        tempdir = os.path.realpath(PersistentTemporaryDirectory())

        log.info('Creating temp dir ' + tempdir)
