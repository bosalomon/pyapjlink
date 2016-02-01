# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib
import unittest

from pypjlink.projector import Projector
from .utils import MockProjSocket



NO_AUTH_RESPONSE = 'PJLINK 0\r'

class AuthenticationTC(unittest.TestCase):

    def test_no_auth(self):
        """test detection of no auth projector"""
        power_response = '%1POWR=1\r'
        with MockProjSocket(NO_AUTH_RESPONSE + power_response) as mock_stream:

            proj = Projector.from_address('projhost')
            self.assertFalse(proj.authenticate(lambda: ''))
            # since projector said no auth required, I shouldn't have written
            # anything to it
            self.assertFalse(mock_stream.write.called)

    def test_auth(self):
        """test authentication"""
        auth_response = 'PJLINK 1 00112233\r'
        power_response = '%1POWR=1\r'

        with MockProjSocket(auth_response + power_response) as mock_stream:
            proj = Projector.from_address('projhost')
            self.assertTrue(proj.authenticate(lambda: 'p'))
            # test write of authentication
            self.assertEqual(
                mock_stream.written,
                self._md5_auth_code('00112233', 'p') + '%1POWR ?\r')

    def test_wrong_auth(self):
        """test failed authentication"""
        response = (
            'PJLINK 1 00112233\r'
            'PJLINK ERRA\r'
        )

        with MockProjSocket(response) as mock_stream:
            proj = Projector.from_address('projhost')
            self.assertFalse(proj.authenticate(lambda: 'p'))
            self.assertEqual(
                mock_stream.written,
                self._md5_auth_code('00112233', 'p') + '%1POWR ?\r')

    def _md5_auth_code(self, salt, password):
        return hashlib.md5((salt + password).encode('utf-8')).hexdigest()


class NameTC(unittest.TestCase):

    def test_unicode(self):
        """test utf-8 chars in projector name"""

        response = (
            NO_AUTH_RESPONSE +
            '%1NAME=à€\r'
        )

        with MockProjSocket(response) as mock_stream:
             proj = Projector.from_address('projhost')
             proj.authenticate(lambda: '')
             name = proj.get_name()
             self.assertEqual(name, 'à€')