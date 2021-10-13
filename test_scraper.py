import pytest

def test_url_valid(page_source):
    assert page_source != None

def test_story_link_tag_exists(page_source):
    story_links = page_source.find_all('a', {'class': 'storylink'})
    assert len(story_links) > 0

def test_hn_user_tag_exists(page_source):
    hn_users = page_source.find_all('a', {'class': 'hnuser'})
    assert len(hn_users) > 0

def test_score_tag_exists(page_source):
    hn_users = page_source.find_all('span', {'class': 'score'})
    assert len(hn_users) > 0

def test_timestamp_user_tag_exists(page_source):
    hn_users = page_source.find_all('span', {'class': 'age'})
    assert len(hn_users) > 0