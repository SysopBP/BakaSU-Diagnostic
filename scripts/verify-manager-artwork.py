#!/usr/bin/env python3
"""Reject legacy character-art resources in modified source and built artifacts."""
import argparse
from pathlib import Path, PurePosixPath
import tarfile
import zipfile
import xml.etree.ElementTree as ET

LEGACY_DRAWABLES = {
    'ic_launcher_foreground.xml', 'ic_launcher_foreground_alt.xml',
    'ic_launcher_monochrome.xml', 'ic_launcher_monochrome_alt.xml',
}


def forbidden(name):
    path = PurePosixPath(name)
    return (path.name in LEGACY_DRAWABLES or
            (path.suffix == '.svg' and
             (path.name.startswith('ReSukiSU_') or path.name.startswith('zako'))))


def verify_source(root):
    paths = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
    bad = [str(p.relative_to(root)) for p in paths if forbidden(p.as_posix())]
    if bad:
        raise ValueError(f'Legacy artwork remains: {bad}')
    main = root / 'manager/app/src/main'
    fox = (main / 'res/drawable/kitsu_fox.png').read_bytes()
    if (main / 'ic_launcher-playstore.png').read_bytes() != fox:
        raise ValueError('Play Store image is not the replacement fox')
    for name in ('ic_launcher', 'ic_launcher_round', 'ic_launcher_alt', 'ic_launcher_alt_round'):
        icon = ET.parse(main / 'res/mipmap' / (name + '.xml')).getroot()
        attr = '{http://schemas.android.com/apk/res/android}drawable'
        if icon.find('foreground').get(attr) != '@drawable/kitsu_fox':
            raise ValueError(f'{name}: unexpected foreground')
        if icon.find('monochrome').get(attr) != '@drawable/kitsu_fox_mono':
            raise ValueError(f'{name}: unexpected monochrome')
    for p in main.rglob('*'):
        if p.suffix in ('.kt', '.java', '.xml'):
            text = p.read_text()
            if any('R.drawable.' + n[:-4] in text or '@drawable/' + n[:-4] in text
                   for n in LEGACY_DRAWABLES):
                raise ValueError(f'Dangling legacy drawable reference: {p}')


def verify_archive(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if path.suffix == '.apk':
                for required in ('res/drawable/kitsu_fox.png', 'res/drawable/kitsu_fox_mono.png'):
                    if required not in names:
                        raise ValueError(f'Missing replacement artwork: {required}')
    else:
        with tarfile.open(path) as archive:
            names = archive.getnames()
            prefix = 'upstream/manager/app/src/main/'
            fox = archive.extractfile(prefix + 'res/drawable/kitsu_fox.png').read()
            if archive.extractfile(prefix + 'ic_launcher-playstore.png').read() != fox:
                raise ValueError('Source archive Play Store image is not the replacement fox')
    bad = [name for name in names if forbidden(name)]
    if bad:
        raise ValueError(f'Legacy artwork in {path}: {bad}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--archive', type=Path, action='append', default=[])
    args = parser.parse_args()
    if not args.source and not args.archive:
        parser.error('provide --source or --archive')
    try:
        if args.source:
            verify_source(args.source)
        for archive in args.archive:
            verify_archive(archive)
    except (ValueError, KeyError, OSError, ET.ParseError) as error:
        parser.exit(1, str(error) + '\n')
    print('Artwork verification passed')
