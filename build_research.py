"""Validate the curated published evidence subset and emit static browser data."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'research/evidence.json').read_text(encoding='utf-8'))
schema = json.loads((ROOT / 'research/evidence.schema.json').read_text(encoding='utf-8'))
assert schema['$defs']['study']['required'] and data['schemaVersion'] == '1.0'
assert len(data['studies']) == 1
study = data['studies'][0]
assert study['id'] == 'kubelka-bickelhaupt-2017-cl-ch3cl'
assert study['reactionEvent'] == 'sn2:0'
assert study['model']['totalCharge'] == -1 and study['model']['multiplicity'] == 1
assert study['publication']['doi'] == '10.1021/acs.jpca.6b12240'
assert study['reactionCoordinate']['kind'] == 'published-irc-stationary-subset'
assert study['reactionCoordinate']['sampledValuesAvailable'] is False
assert [p['id'] for p in study['points']] == ['R', 'RC', 'TS']
assert [p['energy']['value'] for p in study['points']] == [0, -9.2, -0.3]
assert [p['geometry']['C-Cl_out']['value'] for p in study['points']] == [1.790, 1.835, 2.351]
assert all(p['coordinatesFile'] is None for p in study['points'])
assert study['points'][2]['geometry']['Cl_in-C']['status'] == 'derived-from-published'
descriptor_ids = {d['id'] for d in study['descriptors']}
assert len(descriptor_ids) == len(study['descriptors'])
assert {d['category'] for d in study['descriptors']} == {'orbital-interaction', 'energy-decomposition', 'electron-density', 'bond-order', 'geometric-distortion', 'spin-state', 'coordinate-topology'}
for point in study['points']:
    assert point['energy']['unit'] == 'kcal mol⁻¹'
    assert all(q['unit'] == 'Å' for q in point['geometry'].values())
    assert all(name in descriptor_ids for name in point['descriptors'])
    for q in [point['energy'], *point['geometry'].values(), *point['descriptors'].values()]:
        assert q['sourceLocation'] and q['convention']
        assert q['status'] in ('published', 'derived-from-published')
assert math.isclose(study['points'][2]['descriptors']['strain']['value'] + study['points'][2]['descriptors']['interaction']['value'], study['points'][2]['energy']['value'], abs_tol=1e-9)
assert all(d['method'] and d['unit'] and d['normalization'] and d['applicability'] for d in study['descriptors'])
assert all(a['localPath'] is None or (ROOT / a['localPath']).exists() for a in study['artifacts'])
out = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
(ROOT / 'dist/research-data.json').write_text(out, encoding='utf-8')
(ROOT / 'dist/research-data.js').write_text('window.SorgResearch=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
print(f"Validated 1 published SN2 evidence record / 3 tabulated points / {len(study['descriptors'])} descriptor definitions; no QC calculation run.")
