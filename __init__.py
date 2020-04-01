from calibre.customize.conversion import OutputFormatPlugin

class ComicOutputPlugin(OutputFormatPlugin):
    name = 'Comic Output Plugin'
    description = 'Extracts images from an ebook and creates a CBZ comic archive from them.'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Michael McDermott'
    version = (1, 0, 0)

    file_type = 'cbz'

    def convert(oeb_book, output, input_plugin, opts, log):
        print('Hello world')
