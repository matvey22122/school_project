from main import _is_teacher


def test_is_teacher():
    assert _is_teacher('no') == False, "Should be False"
    assert _is_teacher('matvey22122') == True, "Should be True"
