#!/usr/bin/env python3
"""Verify and restore the exact D0 chat archive. Never execute archived code."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, lzma, sys

def digest(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'Duplicate JSON key: '+key)
        out[key] = value
    return out

def verify(root):
    m = json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
    require(m['format']=='d0-chat-snapshot-v1', 'Unsupported format')
    chunks=[]
    for i,p in enumerate(m['parts']):
        require(p['name']==f'part-{i:03d}.xz', 'Wrong chunk order')
        data=(root/'payload'/p['name']).read_bytes()
        require(len(data)==p['bytes'], 'Wrong chunk length')
        require(digest(data)==p['sha256'], 'Wrong chunk SHA256')
        git=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(git==p['git_blob'], 'Wrong Git blob')
        chunks.append(data)
    packed=b''.join(chunks); spec=m['payload']
    require(len(packed)==spec['compressed_bytes'], 'Wrong payload length')
    require(digest(packed)==spec['sha256'], 'Wrong payload SHA256')
    dec=lzma.LZMADecompressor()
    raw=dec.decompress(packed,max_length=spec['json_bytes']+1)
    require(dec.eof and not dec.unused_data and len(raw)==spec['json_bytes'],
            'Unexpected decompressed size or stream')
    obj=json.loads(raw.decode('utf-8'),object_pairs_hook=unique_pairs)
    require(isinstance(obj,dict) and len(obj)==m['file_count'], 'Wrong member count')
    files={}
    for name,text in obj.items():
        path=PurePosixPath(name)
        require(isinstance(text,str) and not path.is_absolute() and
                '..' not in path.parts and '\\' not in name and
                path.parts and path.parts[0]=='packages' and str(path)==name,
                'Unsafe member: '+name)
        files[name]=text.encode('utf-8')
    require(sum(map(len,files.values()))==m['file_bytes'], 'Wrong total bytes')
    inventory={}; package=None
    for line in (root/'FILES.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            package=line[3:].removesuffix('.zip')
        elif line.startswith('| `'):
            cols=[x.strip() for x in line.split('|')[1:-1]]
            name='packages/'+package+'/'+cols[0].strip('`')
            require(name not in inventory, 'Duplicate inventory member')
            inventory[name]=(int(cols[1]),cols[2].strip('`'))
    require(set(inventory)==set(files), 'Inventory differs from payload')
    for name,data in files.items():
        require((len(data),digest(data))==inventory[name], 'Member differs: '+name)
    return files

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract',type=Path,help='Restore below this directory; no different existing file is overwritten')
    args=parser.parse_args(); root=Path(__file__).resolve().parent
    files=verify(root)
    if args.extract is not None:
        output=args.extract.expanduser().resolve(); planned=[]
        for name,data in files.items():
            target=output.joinpath(*PurePosixPath(name).parts)
            require(target.resolve().is_relative_to(output),'Extraction escapes destination')
            require(not target.is_symlink(),'Refusing destination symlink')
            if target.exists():
                require(target.is_file() and target.read_bytes()==data,
                        'Refusing to overwrite: '+str(target))
            else:
                planned.append((target,data))
        for target,data in planned:
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as f:
                f.write(data)
    print(json.dumps({'status':'PASS_ARCHIVE_INTEGRITY','files':len(files),
                      'bytes':sum(map(len,files.values())),
                      'mathematical_tests_executed':False},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,lzma.LZMAError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr)
        sys.exit(1)
