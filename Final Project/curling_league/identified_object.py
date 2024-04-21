class IdentifiedObject:

    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        if hasattr(other, '_oid'):
            return self._oid == other.oid
        else:
            return False

    def __hash__(self):
        return hash(self._oid)
