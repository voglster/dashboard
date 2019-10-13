from modules.todo import remove_links


def test_remove_links():
    test_cases = [
        ("this is a test http://foo.bar (yes)", "this is a test yes"),
        ("http://foo.bar", "http://foo.bar"),
        ("test http://foo.bar (qqq) fluff", "test qqq fluff"),
    ]
    for input, expected_output in test_cases:
        assert remove_links(input) == expected_output
