"""Package the GitHub-ready source without Site identity or Git metadata."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
target = root / 'dist/sorg-atlas-source.zip'
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in ['V037_R2_AUDIT.md','build_diels_alder_r2.py','verify-diels-alder-r2.cjs']:
        archive.write(root / name, 'sorg-atlas/' + name)
    for name in ['README.md', 'build_data.py', 'build_research.py', 'english_content.py', 'quantum_literature.py', 'qc_review.py', 'build_figures.py', 'v028_figures.py', 'v028_content.py', 'v029_content.py', 'v035_mechanisms.py', 'package_source.py', 'verify.cjs', 'verify-foundations.cjs', 'verify-orbitals.cjs', 'verify-ui.cjs', 'verify-diversity.cjs', 'verify-reaction-lab.cjs', 'package.json', 'package-lock.json', 'AUDIT.md', 'V028_AUDIT.md', 'V029_AUDIT.md', 'V030_AUDIT.md', 'V031_AUDIT.md', 'V032_AUDIT.md', 'V033_AUDIT.md', 'V034_AUDIT.md', 'V035_AUDIT.md', 'V036_AUDIT.md', 'V037_AUDIT.md', 'build_diels_alder.py', 'verify-diels-alder.cjs', 'verify-volume-archives.cjs', 'V037_FOLLOWUP_AUDIT.md', 'build_reaction_systems.py', 'verify-carbonyl.cjs',
                 '.gitignore', '.github/workflows/pages.yml']:
        archive.write(root / name, 'sorg-atlas/' + name)
    for path in sorted((root / 'dist').rglob('*')):
        if path.is_file() and path != target and not path.name.endswith('.run.lock') and '__pycache__' not in path.parts and not any(p.endswith('.tmp') for p in path.parts) and not path.name.endswith('.pending') and not ('r2' in path.parts and path.name.startswith('eval-') and path.suffix in ['.log','.json']):
            archive.write(path, 'sorg-atlas/' + str(path.relative_to(root)))
    for path in sorted((root / 'audit').rglob('*')):
        if path.is_file():archive.write(path, 'sorg-atlas/' + str(path.relative_to(root)))
    for path in sorted((root / 'research').rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:archive.write(path, 'sorg-atlas/' + str(path.relative_to(root)))
print('Created dist/sorg-atlas-source.zip')
