"""Tests various methods of the Download
class.

All the methods that start with test are used
to test a certain function. The test method
will have the name of the method being tested
seperated by an underscore.

If the method to be tested is extract_content,
the test method name will be test_extract_content
"""

from downloader_cli.download import Download


TEST_URL = "http://212.183.159.230/5MB.zip"


def test__extract_border_icon():
    """Test the _extract_border_icon method"""
    download = Download(TEST_URL)

    icon_one = download._extract_border_icon("#")
    icon_two = download._extract_border_icon("[]")
    icon_none = download._extract_border_icon("")
    icon_more = download._extract_border_icon("sdafasdfasdf")

    assert icon_one == ('#', '#'), "Should be ('#', '#')"
    assert icon_two == ('[', ']'), "Should be ('[', '])"
    assert icon_none == ('|', '|'), "Should be ('|', '|')"
    assert icon_more == ('|', '|'), "Should be ('|', '|')"


def test__build_headers():
    """Test the _build_headers method"""
    download = Download(TEST_URL)

    download._build_headers(1024)
    header_built = download.headers

    assert header_built == {"Range": "bytes={}-".format(1024)}, \
        "Should be 1024"


def test__preprocess_conn():
    """Test the _preprocess_conn method"""
    download = Download(TEST_URL)
    download._preprocess_conn()

    assert download.f_size == 5242880, "Should be 5242880"
