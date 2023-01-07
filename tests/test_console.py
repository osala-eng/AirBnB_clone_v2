#!/bin/bash
'''Console test suite'''


import sys
import unittest
from io import StringIO
from console import HBNBCommand
from models.stringtemplates import HBNB_TYPE_STORAGE, FILE, DB
from os import getenv
from models import storage

db = getenv(HBNB_TYPE_STORAGE, FILE)


class test_console(unittest.TestCase):
    '''Test console module'''

    def setUp(self) -> None:
        '''Setup'''
        self.backup = sys.stdout
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        return super().setUp()

    def tearDown(self) -> None:
        '''Teardown'''
        sys.stdout = self.backup
        return super().tearDown()

    def test_quit(self) -> None:
        '''Test quit console'''
        console = self.create()
        self.assertTrue(console.onecmd('quit'))

    def test_EOF(self) -> None:
        '''Test EOF'''
        console = self.create()
        self.assertTrue(console.onecmd('EOF'))

    def test_all(self) -> None:
        '''Test all cmd'''
        console = self.create()
        console.onecmd('all')
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    @unittest.skipIf(db == DB, 'Testing Database Storage Only')
    def test_show(self) -> None:
        '''Test show'''
        console = self.create()
        console.onecmd('create User')
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd('show User ' + user_id)
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertTrue(str is type(x))

    @unittest.skipIf(db == DB, 'Testing Database Storage Only')
    def test_show_class_name(self) -> None:
        '''Test case class name missing'''
        console = self.create()
        console.onecmd('create User')
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd('show')
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual('** class name missing **\n', x)

    def test_show_class_name(self) -> None:
        '''Test case missing id'''
        console = self.create()
        console.onecmd('create User')
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd('show User')
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual('** instance id missing **\n', x)

    @unittest.skipIf(db == DB, 'Testing database storage only')
    def test_show_no_instance_found(self) -> None:
        '''Test case missing id'''
        console = self.create()
        console.onecmd('create User')
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd('show User ' + '124356876')
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual('** no instance found **\n', x)

    def test_create(self) -> None:
        '''Test create'''
        console = self.create()
        console.onecmd('create User email=mail@somemail.com password=abcijf')
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_class_name(self) -> None:
        ''' Test case missing class name'''
        console = self.create()
        console.onecmd('create')
        x = (self.capt_out.getvalue())
        self.assertEqual('** class name missing **\n', x)

    def test_class_name_doest_exist(self) -> None:
        '''Test case name does not exist'''
        console = self.create()
        console.onecmd('create Binita')
        x = (self.capt_out.getvalue())
        self.assertEqual('** class doesn\'t exist **\n', x)

    @unittest.skipIf(db != DB, 'Testing DBstorage only')
    def test_create_db(self) -> None:
        console = self.create()
        console.onecmd('create State name=California')
        result = storage.all('State')
        self.assertTrue(len(result))
