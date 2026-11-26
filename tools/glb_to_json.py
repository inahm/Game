"""Convert .glb files to self-contained glTF JSON (.json) with the binary buffer embedded as base64.

The artifact host serves .json but not .glb; GLTFLoader reads both forms.
Usage: python3 tools/glb_to_json.py models/*.glb
"""
import base64, json, struct, sys

for path in sys.argv[1:]:
    data = open(path, 'rb').read()
    magic, _version, _length = struct.unpack('<4sII', data[:12])
    assert magic == b'glTF', path + ' is not a GLB file'
    offset, gltf, binary = 12, None, b''
    while offset < len(data):
        chunk_len, chunk_type = struct.unpack('<II', data[offset:offset + 8])
        chunk = data[offset + 8:offset + 8 + chunk_len]
        if chunk_type == 0x4E4F534A:   # JSON
            gltf = json.loads(chunk)
        elif chunk_type == 0x004E4942:  # BIN
            binary = chunk
        offset += 8 + chunk_len
    if gltf.get('buffers'):
        gltf['buffers'][0]['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode(binary).decode('ascii')
    out = path[:-4] + '.json'
    with open(out, 'w') as f:
        json.dump(gltf, f, separators=(',', ':'))
    print(out, len(open(out, 'rb').read()) // 1024, 'KB')
