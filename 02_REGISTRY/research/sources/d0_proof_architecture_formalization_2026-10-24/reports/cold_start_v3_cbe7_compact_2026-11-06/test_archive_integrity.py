#!/usr/bin/env python3
"""Exercise split-stream restoration and rejection of corrupted parts."""
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
import zlib

from verify_archive import verify_archive

def sha(data):
    return hashlib.sha256(data).hexdigest()

class ArchiveTests(unittest.TestCase):
    def test_split_round_trip_and_corruption(self):
        raw = (b'{"case":"bounded evidence"}\n' * 1000) + b'end'
        c = zlib.compressobj(wbits=31)
        packed = c.compress(raw) + c.flush()
        chunks = [packed[i:i+17] for i in range(0, len(packed), 17)]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'parts').mkdir()
            items = []
            for i, chunk in enumerate(chunks):
                name = f'part-{i:03d}.gzchunk'
                (root/'parts'/name).write_bytes(chunk)
                items.append({'name':name, 'bytes':len(chunk), 'sha256':sha(chunk)})
            manifest = {'parts':items, 'part_max_bytes':17, 'gzip_bytes':len(packed), 'gzip_sha256':sha(packed), 'full_bytes':len(raw), 'full_sha256':sha(raw)}
            output = io.BytesIO()
            self.assertEqual(verify_archive(root, manifest, output), len(raw))
            self.assertEqual(output.getvalue(), raw)
            f = root/'parts'/items[0]['name']
            altered = bytearray(f.read_bytes())
            altered[-1] ^= 1
            f.write_bytes(altered)
            with self.assertRaises((ValueError, zlib.error)):
                verify_archive(root, manifest)

if __name__ == '__main__':
    unittest.main()
