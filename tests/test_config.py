import json
from pathlib import Path

from emanate import config
from utils import chdir, directory_tree, home


def test_json_resolution():
    with directory_tree({
            'src': {
                'emanate.json': json.dumps(
                    {"source": ".", "destination": "../dest"},
                ),
            },
    }) as tmpdir:

        config_cwd = config.from_json(tmpdir / 'src' / 'emanate.json')
        assert config.is_resolved(config_cwd)

        with chdir(tmpdir):
            config_tmp = config.from_json(Path('src') / 'emanate.json')
            assert config.is_resolved(config_tmp)

        with chdir(tmpdir / 'src'):
            config_src = config.from_json(Path('emanate.json'))
            assert config.is_resolved(config_src)

        assert config_cwd == config_tmp == config_src
        assert config_cwd.destination.is_absolute()
        assert config_cwd.source.is_absolute()


def test_defaults():
    assert config.defaults().destination == Path.home()
    assert config.defaults().source == Path.cwd()

    with directory_tree({}) as tmpdir:
        with chdir(tmpdir):
            assert config.defaults().source.samefile(tmpdir)
            assert Path.cwd().samefile(tmpdir)

        with home(tmpdir):
            assert config.defaults().destination.samefile(tmpdir)
            assert Path.home().samefile(tmpdir)
