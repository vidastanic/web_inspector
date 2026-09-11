from unittest.mock import Mock

import pytest

from webchecker.patterns import PatternMatcher
from webchecker.scraper import WebScraper
from webchecker.web_app import WebCheckerApp


def test_cli_stop_prevents_link_fetch_and_next_page():
    scraper = WebScraper(delay=0)
    scraper._extract_links = Mock(return_value=['https://example.com/next'])

    def scrape(*args):
        scraper.stop()
        return ['example']

    scraper._scrape_page = Mock(side_effect=scrape)
    assert scraper.scrape_site('https://example.com', PatternMatcher('™')) == ['example']
    scraper._scrape_page.assert_called_once()
    scraper._extract_links.assert_not_called()
    scraper.close()


@pytest.mark.parametrize('action', ['stop', 'clear'])
def test_web_cancellation_during_page_fetch(action):
    app = WebCheckerApp()
    scraper = WebScraper(delay=0)
    matcher = PatternMatcher('™')
    session = {'scraper': scraper, 'status': 'starting', 'progress': 0}
    app.active_sessions['test'] = session
    client = app.app.test_client()

    def scrape(*args, **kwargs):
        assert client.get(f'/api/{action}/test').status_code == 200
        return ['example']

    scraper._scrape_page = Mock(side_effect=scrape)
    scraper._extract_links = Mock(return_value=['https://example.com/next'])
    app._scrape_worker('test', 'https://example.com', matcher, 2, 3, False)

    assert session['status'] == 'stopped'
    assert session['progress'] == 50
    scraper._scrape_page.assert_called_once()
    scraper._extract_links.assert_not_called()
    if action == 'clear':
        assert 'test' not in app.active_sessions


def test_worker_handles_session_cleared_before_thread_starts():
    app = WebCheckerApp()
    app._scrape_worker('missing', 'https://example.com', PatternMatcher('™'), 2, 3, False)


def test_stop_before_worker_starts_skips_sitemap_requests():
    app = WebCheckerApp()
    scraper = WebScraper(delay=0)
    scraper._discover_sitemap_urls = Mock()
    scraper.stop()
    app.active_sessions['test'] = {'scraper': scraper, 'status': 'stopped', 'progress': 0}
    app._scrape_worker('test', 'https://example.com', PatternMatcher('™'), 2, 3, True)
    assert app.active_sessions['test']['status'] == 'stopped'
    scraper._discover_sitemap_urls.assert_not_called()


def test_web_rejects_zero_page_limit():
    client = WebCheckerApp().app.test_client()
    response = client.post('/api/start-scrape', json={
        'url': 'https://example.com', 'pattern': '™', 'max_pages': 0,
    })
    assert response.status_code == 400
