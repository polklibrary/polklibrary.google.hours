# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from polklibrary.google.hours.testing import POLKLIBRARY_GOOGLE_HOURS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that polklibrary.google.hours is properly installed."""

    layer = POLKLIBRARY_GOOGLE_HOURS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if polklibrary.google.hours is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('polklibrary.google.hours'))

    def test_browserlayer(self):
        """Test that IPolklibraryGoogleHoursLayer is registered."""
        from polklibrary.google.hours.interfaces import IPolklibraryGoogleHoursLayer
        from plone.browserlayer import utils
        self.assertIn(IPolklibraryGoogleHoursLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = POLKLIBRARY_GOOGLE_HOURS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['polklibrary.google.hours'])

    def test_product_uninstalled(self):
        """Test if polklibrary.google.hours is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('polklibrary.google.hours'))

    def test_browserlayer_removed(self):
        """Test that IPolklibraryGoogleHoursLayer is removed."""
        from polklibrary.google.hours.interfaces import IPolklibraryGoogleHoursLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPolklibraryGoogleHoursLayer, utils.registered_layers())
