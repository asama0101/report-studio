import pytest
from check_html import find_problems

PRINT_CSS = "<style>@media print { body { color: #000; } }</style>"


def wrap(body: str) -> str:
    return f"<html><head>{PRINT_CSS}</head><body>{body}</body></html>"


@pytest.mark.parametrize(
    "body",
    [
        '<script src="https://x.example/y.js"></script>',
        '<link rel="stylesheet" href="https://x.example/y.css">',
        '<img src="http://x.example/a.png">',
        "<style>@import url(https://x.example/y.css);</style>",
        "<style>body { background: url(http://x.example/a.png); }</style>",
        "<style>@import 'https://x.example/y.css';</style>",
        '<img srcset="https://x.example/a.png 1x, b.png 2x">',
        '<svg><image href="https://x.example/a.png"/></svg>',
        '<svg><image xlink:href="https://x.example/a.png"/></svg>',
        '<svg><use href="https://x.example/s.svg#a"/></svg>',
        '<object data="https://x.example/a.pdf"></object>',
        '<video poster="https://x.example/a.png"></video>',
        '<script src="//cdn.example/y.js"></script>',
    ],
)
def test_external_load_is_reported(body):
    problems = find_problems(wrap(body))
    assert any("外部読み込み" in p for p in problems)


@pytest.mark.parametrize(
    "body",
    [
        '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
        '<a href="https://example.com">リンク</a>',
        '<img src="data:image/png;base64,AAAA">',
    ],
)
def test_allowed_references_are_not_reported(body):
    assert find_problems(wrap(body)) == []


def test_missing_print_css_is_reported():
    problems = find_problems("<html><body>本文</body></html>")
    assert any("印刷 CSS" in p for p in problems)


def test_clean_html_has_no_problems():
    assert find_problems(wrap("<p>本文</p>")) == []
