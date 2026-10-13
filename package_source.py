"""Package the GitHub-ready source without Site identity or Git metadata."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
target = root / 'dist/sorg-atlas-source.zip'
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in ['README.md', 'build_data.py', 'english_content.py', 'quantum_literature.py', 'qc_review.py', 'build_figures.py', 'v028_figures.py', 'v028_content.py', 'v029_content.py', 'package_source.py', 'verify.cjs', 'verify-ui.cjs', 'package.json', 'package-lock.json', 'AUDIT.md', 'V028_AUDIT.md', 'V029_AUDIT.md',
                 '.gitignore', '.github/workflows/pages.yml']:
        archive.write(root / name, 'sorg-atlas/' + name)
    for path in sorted((root / 'dist').rglob('*')):
        if path.is_file() and path.suffix != '.zip':
            archive.write(path, 'sorg-atlas/' + str(path.relative_to(root)))
    for path in sorted((root / 'audit').rglob('*')):
        if path.is_file():archive.write(path, 'sorg-atlas/' + str(path.relative_to(root)))
print('Created dist/sorg-atlas-source.zip')
