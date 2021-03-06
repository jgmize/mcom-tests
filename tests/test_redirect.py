#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import requests
import pytest


@pytest.mark.skip_selenium
class TestRedirects(object):
    def _test_get_redirect(self, mozwebqa, origin, final,
                           allow_redirects=True, status_code=301):
        if origin.startswith('http'):
            url = origin
        else:
            url = mozwebqa.base_url + origin
        response = requests.get(url, allow_redirects=allow_redirects)
        if final.startswith('http'):
            result = final
        else:
            result = mozwebqa.base_url + final
        if allow_redirects:
            Assert.equal(response.url, result)
        else:
            Assert.equal(response.headers['location'], result)
            Assert.equal(response.status_code, status_code)

    @pytest.mark.nondestructive
    def test_redirects_from_mozilla_dot_com(self, mozwebqa):
        url = mozwebqa.base_url
        response = requests.get(url)
        Assert.contains(url, response.url)

    @pytest.mark.nondestructive
    def test_fennec_redirects_to_mobile(self, mozwebqa):
        url = mozwebqa.base_url + "/fennec/"
        response = requests.get(url)
        result = mozwebqa.base_url + "/en-US/firefox/partners/"
        Assert.equal(result, response.url)

    @pytest.mark.nondestructive
    def test_firefox_mobile_redirects_to_mobile(self, mozwebqa):
        self._test_get_redirect(mozwebqa,
                                "/firefox/mobile/",
                                "/en-US/firefox/android/")

    @pytest.mark.nondestructive
    def test_aurora_redirects_to_firefox_aurora(self, mozwebqa):
        url = mozwebqa.base_url + "/aurora/"
        response = requests.get(url, allow_redirects=False)
        Assert.equal(response.status_code, 301)

    @pytest.mark.nondestructive
    def test_beta_redirects_to_firefox_beta(self, mozwebqa):
        self._test_get_redirect(mozwebqa,
                                '/beta/',
                                '/firefox/channel/#beta',
                                False, 302)

    @pytest.mark.nondestructive
    def test_redirect_community_to_contribute(self, mozwebqa):
        url = mozwebqa.base_url + "/community/"
        response = requests.get(url)
        Assert.contains("/contribute/", response.url)

    @pytest.mark.nondestructive
    def test_redirect_mobile_notes_to_android_notes(self, mozwebqa):
        self._test_get_redirect(mozwebqa,
                                '/mobile/notes/',
                                '/firefox/android/notes/',
                                False)
        self._test_get_redirect(mozwebqa,
                                '/mobile/beta/notes/',
                                '/firefox/android/beta/notes/',
                                False)
        self._test_get_redirect(mozwebqa,
                                '/mobile/aurora/notes/',
                                '/firefox/android/aurora/notes/',
                                False)
        self._test_get_redirect(mozwebqa,
                                '/mobile/37.0/releasenotes/',
                                '/firefox/android/37.0/releasenotes/',
                                False)
        self._test_get_redirect(mozwebqa,
                                '/mobile/37.0beta/releasenotes/',
                                '/firefox/android/37.0beta/releasenotes/',
                                False)
        self._test_get_redirect(mozwebqa,
                                '/mobile/37.0a2/auroranotes/',
                                '/firefox/android/37.0a2/auroranotes/',
                                False)

    @pytest.mark.nondestructive
    def test_redirect_mobile_to_firefox_mobile(self, mozwebqa):
        self._test_get_redirect(mozwebqa,
                                "/mobile/faq/",
                                "/en-US/firefox/android/faq/")
        self._test_get_redirect(mozwebqa,
                                "/mobile/features/",
                                "/en-US/firefox/android/")
        url = mozwebqa.base_url + "/mobile/platforms/"
        response = requests.get(url)
        Assert.equal(response.status_code, 200)
        Assert.contains('support.mozilla.org', response.url)

    @pytest.mark.nondestructive
    def test_redirect_some_m_to_firefox_mobile(self, mozwebqa):
        self._test_get_redirect(mozwebqa,
                                "/m/faq/",
                                "/en-US/firefox/android/faq/")
        self._test_get_redirect(mozwebqa,
                                "/m/features/",
                                "/en-US/firefox/android/")
        url = mozwebqa.base_url + "/m/platforms/"
        response = requests.get(url)
        Assert.equal(response.status_code, 200)
        Assert.contains('support.mozilla.org', response.url)

    @pytest.mark.nondestructive
    def test_redirect_m(self, mozwebqa):
        self._test_get_redirect(mozwebqa,
                                "/m/",
                                "/en-US/firefox/new/")

    @pytest.mark.nondestructive
    def test_rhino_docs_redirect(self, mozwebqa):
        origin = mozwebqa.base_url + '/rhino/doc.html'
        result = 'https://developer.mozilla.org/en-US/docs/Mozilla/Projects/Rhino/Documentation'
        self._test_get_redirect(mozwebqa, origin, result)

    @pytest.mark.nondestructive
    def test_rhino_download_redirect(self, mozwebqa):
        origin = mozwebqa.base_url + '/rhino/download.html'
        result = \
            'https://developer.mozilla.org/en-US/docs/Mozilla/Projects/Rhino/Download_Rhino'
        self._test_get_redirect(mozwebqa, origin, result)

    @pytest.mark.nondestructive
    def test_rhino_redirect(self, mozwebqa):
        origin = mozwebqa.base_url + '/rhino/'
        result = \
            'https://developer.mozilla.org/en-US/docs/Mozilla/Projects/Rhino'
        self._test_get_redirect(mozwebqa, origin, result)

    @pytest.mark.nondestructive
    def test_redirect_firefox_home_the_product(self, mozwebqa):
        result = \
            'https://blog.mozilla.org/services/2012/08/31/retiring-firefox-home/'
        self._test_get_redirect(mozwebqa, '/mobile/home/', result)
        self._test_get_redirect(mozwebqa, '/fr/mobile/home/', result)

    @pytest.mark.nondestructive
    def test_notes_redirects_to_firefox_notes(self, mozwebqa):
        url = mozwebqa.base_url + "/firefox/notes/"
        response = requests.get(url)
        Assert.contains("/firefox/", response.url)
        Assert.contains("/releasenotes/", response.url)

    @pytest.mark.nondestructive
    def test_all_older_redirect(self, mozwebqa):
        url = mozwebqa.base_url + "/firefox/all-older.html"
        response = requests.get(url)
        Assert.contains("/firefox/new", response.url)

    @pytest.mark.nondestructive
    def test_old_firstrun_redirect(self, mozwebqa):
        url = mozwebqa.base_url + "/en-US/projects/firefox/3.6.13/firstrun/"
        response = requests.get(url)
        Assert.not_equal(response.status_code, 404)

    @pytest.mark.nondestructive
    def test_old_whatsnew_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/en-US/projects/firefox/3.6.13/whatsnew/'
        response = requests.get(url)
        Assert.not_equal(response.status_code, 404)

    @pytest.mark.nondestructive
    def test_partners_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/b2g/'
        response = requests.get(url)
        Assert.contains('/partners/', response.url)

    @pytest.mark.nondestructive
    def test_firefox_metro_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/metrofirefox'
        response = requests.head(url)
        Assert.not_equal(response.status_code, 404)

    @pytest.mark.nondestructive
    def test_locale_redirect_for_newsletter(self, mozwebqa):
        url = mozwebqa.base_url + '/newsletter'
        response = requests.get(url, headers={'Accept-Language': 'pl'})
        Assert.equal(response.url, mozwebqa.base_url + '/pl/newsletter/')

    @pytest.mark.nondestructive
    def test_firefox_os_mobile_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/firefox/mobile/faq/?os=firefox-os'
        response = requests.get(url, headers={'Accept-Language': 'en-US'})
        Assert.contains('/firefox/os/faq/', response.url)

    @pytest.mark.nondestructive
    def test_account_manager_redirect(self, mozwebqa):
        """
        Test that /firefox/account manager redirects
        to /persona
        """
        url = mozwebqa.base_url + '/firefox/accountmanager'
        response = requests.get(url, headers={'Accept-Language': 'en-US'})
        Assert.contains('/persona', response.url)

    @pytest.mark.nondestructive
    def test_developer_redirect(self, mozwebqa):
        """
        Test aurora.mozilla.org redirects to
        http://www.mozilla.org/firefox/channel/#developer
        """
        url = 'http://aurora.mozilla.org'
        response = requests.get(url)
        Assert.contains(
            'https://www.mozilla.org/firefox/channel/#developer',
            [r.headers.get('location', '') for r in response.history])
        Assert.equal(200, response.status_code)

    @pytest.mark.nondestructive
    def test_beta_redirect(self, mozwebqa):
        """
        Test beta.mozilla.org redirects to
        http://www.mozilla.org/firefox/channel/#beta
        """
        url = 'http://beta.mozilla.org'
        response = requests.get(url)
        Assert.contains(
            'http://www.mozilla.org/en-US/firefox/channel/#beta',
            [r.headers.get('location', '') for r in response.history])
        Assert.equal(200, response.status_code)

    @pytest.mark.nondestructive
    def test_apps_redirect(self, mozwebqa):
        """
        Test mozilla.org/apps redirects to
        http[s]://marketplace.firefox.com
        """
        url = mozwebqa.base_url + '/apps'
        response = requests.get(url)
        Assert.contains('marketplace.firefox.com', response.url)
        Assert.equal(200, response.status_code)

    @pytest.mark.nondestructive
    def test_technology_redirect(self, mozwebqa):
        """
        Test mozilla.org/firefox/technology redirects to
        http[s]://developer.mozilla.org/docs/Tools
        """
        url = mozwebqa.base_url + '/firefox/technology'
        response = requests.get(url, allow_redirects=False)
        Assert.equal(301, response.status_code)

    @pytest.mark.nondestructive
    def test_performance_redirect(self, mozwebqa):
        """
        Test mozilla.org/firefox/performance redirects to
        http[s]://www.mozilla.org/en-US/firefox/desktop/fast/
        """
        url = mozwebqa.base_url + '/firefox/performance'
        response = requests.get(url)
        Assert.contains('/firefox/desktop/fast/', response.url)
        Assert.equal(200, response.status_code)

    @pytest.mark.nondestructive
    def test_security_redirect(self, mozwebqa):
        """
        Test mozilla.org/firefox/security redirects to
        http[s]://www.mozilla.org/en-US/firefox/desktop/trust/
        """
        url = mozwebqa.base_url + '/firefox/security'
        response = requests.get(url)
        Assert.contains('/firefox/desktop/trust/', response.url)
        Assert.equal(200, response.status_code)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize("locale", ['son', 'zh-CN', 'ta'])
    def test_firefox_new_redirect(self, mozwebqa, locale):
        url = mozwebqa.base_url + '/firefox/new'
        response = requests.get(url, headers={'Accept-Language': locale})
        Assert.contains(locale, response.url)

    @pytest.mark.nondestructive
    def test_policy_archive_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/privacy/archive/'
        response = requests.get(url)
        Assert.equal(response.status_code, 200)
        Assert.equal(response.history[0].status_code, 301)
        Assert.true(response.history[0].headers['location'].endswith('/en-US/privacy/archive/'))

    @pytest.mark.nondestructive
    def test_dnt_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/dnt'
        response = requests.get(url)
        Assert.equal(response.status_code, 200)
        Assert.equal(response.history[0].status_code, 301)
        Assert.true(response.history[-1].headers['location'].endswith('/firefox/dnt/'))

    @pytest.mark.nondestructive
    def test_firefox_os_notes_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/firefox/os/notes/'
        response = requests.get(url)
        Assert.equal(response.status_code, 200)
        Assert.equal(response.history[0].status_code, 301)
        Assert.equal(response.history[0].headers['location'],
                     'https://developer.mozilla.org/Firefox_OS/Releases')

    @pytest.mark.nondestructive
    def test_firefox_os_notes_version_redirect(self, mozwebqa):
        url = mozwebqa.base_url + '/firefox/os/notes/2.0'
        response = requests.get(url)
        Assert.equal(response.status_code, 200)
        Assert.equal(response.history[0].status_code, 301)
        Assert.equal(response.history[0].headers['location'],
                     'https://developer.mozilla.org/Firefox_OS/Releases/2.0')
