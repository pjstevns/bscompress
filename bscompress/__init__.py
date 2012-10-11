
from ZODB.blob import BlobStorageMixin
from ZODB.blob import rename_or_copy_blob


def restoreBlob(self, oid, serial, data, blobfilename, prev_txn,
                transaction):
    """Write blob data already committed in a separate database
    """
    self.restore(oid, serial, data, '', prev_txn, transaction)
    self._blob_storeblob(oid, serial, blobfilename)

    return self._tid


def _blob_storeblob(self, oid, serial, blobfilename):
    self._lock_acquire()
    try:
        self.fshelper.getPathForOID(oid, create=True)
        targetname = self.fshelper.getBlobFilename(oid, serial)
        rename_or_copy_blob(blobfilename, targetname)

        # if oid already in there, something is really hosed.
        # The underlying storage should have complained anyway
        self.dirty_oids.append((oid, serial))
    finally:
        self._lock_release()


def storeBlob(self, oid, oldserial, data, blobfilename, version,
              transaction):
    """Stores data that has a BLOB attached."""
    assert not version, "Versions aren't supported."
    serial = self.store(oid, oldserial, data, '', transaction)
    self._blob_storeblob(oid, serial, blobfilename)

    return self._tid

BlobStorageMixin.restoreBlob = restoreBlob
BlobStorageMixin._blob_storeblob = _blob_storeblob
BlobStorageMixin.storeBlob = storeBlob


