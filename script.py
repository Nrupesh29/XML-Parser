from xml.etree import ElementTree
import gzip
import base64
import os
import optparse
from cStringIO import StringIO
import xml.sax.saxutils as saxutils

parser = optparse.OptionParser()
parser.add_option('--gzip', dest="compress")
parser.add_option('--gunzip', dest="decompress")

(options, args) = parser.parse_args()

if options.compress:
    filename = options.compress
    compress = True
elif options.decompress:
    filename = options.decompress
    compress = False

try:
    with open(filename, 'rt') as xml:
        tree = ElementTree.parse(xml)

        for node in tree.iter():
            attr = node.attrib.get('test')
            if (attr == "1"):
                if compress:
                    content = ElementTree.tostring(node)
                    content = content.split('>', 1)[1].rsplit('<', 1)[0]
                    compressed_file = StringIO()
                    zipper = gzip.GzipFile(mode='wb', fileobj=compressed_file)
                    zipper.write(content)
                    zipper.close()
                    enc_text =  base64.b64encode(compressed_file.getvalue())
                    for child in list(node):
                        node.remove(child)
                    node.text = enc_text

                else:
                    decompressed_file = gzip.GzipFile(mode='rb', 
                            fileobj=StringIO(base64.b64decode(node.text)))
                    decompressed_data = decompressed_file.read()
                    decompressed_file.close()
                    node.text = decompressed_data

        with open(filename, 'wt') as wxml:
            tree.write(wxml)

        if not compress:
            with open(filename) as f:
                content = f.read()
                with open(filename, 'w') as f:
                    f.write(saxutils.unescape(content))
                    f.close()
    
except NameError:
    print "Invalid options or arguments specified!"
except TypeError:
        print "First compress the file!"
