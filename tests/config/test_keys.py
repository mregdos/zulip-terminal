import pytest

from zulipterminal.config import keys

AVAILABLE_COMMANDS = list(keys.KEY_BINDINGS.keys())

USED_KEYS = {key
             for values in keys.KEY_BINDINGS.values()
             for key in values['keys']}


@pytest.fixture(params=keys.KEY_BINDINGS.keys())
def valid_command(request):
    return request.param


@pytest.fixture(params=['BLAH*10'])
def invalid_command(request):
    return request.param


def test_keys_for_command(valid_command):
    assert (keys.KEY_BINDINGS[valid_command]['keys'] ==
            keys.keys_for_command(valid_command))


def test_keys_for_command_invalid_command(invalid_command):
    with pytest.raises(keys.InvalidCommand):
        keys.keys_for_command(invalid_command)


def test_is_command_key_matching_keys(valid_command):
    for key in keys.keys_for_command(valid_command):
        assert keys.is_command_key(valid_command, key)


def test_is_command_key_nonmatching_keys(valid_command):
    keys_to_test = USED_KEYS - keys.keys_for_command(valid_command)
    for key in keys_to_test:
        assert not keys.is_command_key(valid_command, key)


def test_is_command_key_invalid_command(invalid_command):
    with pytest.raises(keys.InvalidCommand):
        keys.is_command_key(invalid_command, 'esc')  # key doesn't matter


def test_is_command_elligible_for_tips(valid_command):
    assert (keys.is_command_elligible_for_tips(valid_command) ==
            ('is_random_tip' not in keys.KEY_BINDINGS[valid_command] or
            keys.KEY_BINDINGS[valid_command]['is_random_tip']))


def test_HELP_is_not_allowed_as_tip():
    assert (keys.KEY_BINDINGS['HELP']['is_random_tip'] is False)
    assert (keys.is_command_elligible_for_tips('HELP') is False)
