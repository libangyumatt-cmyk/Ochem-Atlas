"""Package the GitHub-ready source without Site identity or Git metadata."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
target = root / 'dist/sorg-atlas-source.zip'
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in ['README.md', 'build_data.py', 'package_source.py', 'verify.cjs',
                 '.gitignore', '.github/workflows/pages.yml']:
        archive.write(root / name, 'sorg-atlas/' + name)
    for path in sorted((root / 'dist').iterdir()):
        if path.is_file() and path.suffix != '.zip':
            archive.write(path, 'sorg-atlas/dist/' + path.name)
print('Created dist/sorg-atlas-source.zip')
