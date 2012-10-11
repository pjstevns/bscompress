bscompress
==========

Experimental Blobstorage Compressor

2012, Paul J Stevens, paul@nfg.nl


- Blobstorage should use less space if possible.
- Make copying and moving content faster.

excessive duplication of content
--------------------------------

I spent the last year working on upgrading a Plone-2.5 installation. This installation uses the never-released PloneMultisite product. A product meant to allow managers to workflow content into a set of Plone sites using a hub-spoke model. 

One of the problems with this model was the sometimes extreme duplication of content. Whenever a file, i.e. a PDF document was added through this workflow, it would be copied, sometimes up to 10 times! Did I mention that all the sub-sites use LinguaPlone, and that the PDF files were in language dependent FileFields? So, for each language in each sub-site a new copy was created for every PDF file uploaded!

If you’ve worked with Plone-2.5 you can imagine what this did with the ZODB: it exploded, making the Plone installation extremely slow. Thank the zope crew for blob-storage. It pulled the blobs out of the ZODB, and put them into the file-system. Much better, thank you! Combined with the overall improved state of Plone-4 things started to rock again. But I still wasn’t too happy with the size of the blob-storage. All the duplicated content was still claiming way too much space.

Having some experience with de-duplication of content I thought I’d look into a simple solution: leverage the standard unix link(2) facility.

Before trying to fix the blob-storage code in Zope, it seemed a nice way to try my hand at some prototyping and proof-of-concept.

So the premise is simple: for each blob-file, calculate a sha1 hash, and build lists of filenames that share the same hash value, and replace all the duplicate files with hard-links.

Whipping up a quick python script shows some really significant saving:
Current usage
14625	var/blobstorage
scanning... done
optimizing... done
Optimized usage
2395	var/blobstorage


Those numbers are actually MB - output from ‘du -ms’. Pretty nice savings, right?

Feel free to try it. Just make sure you backup your blob-storage tree first!

The ultimate goal at this stage would be to fix ZODB/src/ZODB/blob.py to support updating the blobs, without also updating all the linked files. Once that is in place blobstorage would not only take significantly less space, but moving and copying large amounts of data in you Plone site would become much, much faster since no blobs would have to be written onto the filesystem; only links would have to be added.

---
