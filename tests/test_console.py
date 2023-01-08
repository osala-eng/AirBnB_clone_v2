#!/usr/bin/python3
'''Console test suite'''
import sys
import unittest
from io import StringIO
from console import HBNBCommand
from models.stringtemplates import HBNB_TYPE_STORAGE, FILE, DB
from os import getenv, rename, remove
from models import storage
from models import State
from models.engine.db_storage import DBStorage
from unittest.mock import create_autospec
from pycodestyle import StyleGuide
import datetime


class TestConsole(unittest.TestCase):
    '''Test console module'''
    __db_file_name = None
    db = getenv(HBNB_TYPE_STORAGE, FILE)
    LOCAL_DB_NAME = 'file.json'
    CONSOLE_FILE = 'console.py'
    @classmethod
    def setUpClass(self) -> None:
        '''Test Class Setup'''
        try:
            self.__db_file_name = f'temp{datetime.utcnow()}'
            rename(self.LOCAL_DB_NAME, self.__db_file_name)
        except Exception:
            pass
        self.__cmd = HBNBCommand()
        return super().setUpClass()

    @classmethod
    def tearDownClass(self) -> None:
        '''Class teardown'''
        try:
            rename(self.__db_file_name, self.LOCAL_DB_NAME)
        except Exception:
            pass
        del self.__cmd
        if self.db == DB:
            storage.close()
        return super().tearDownClass()

    def setUp(self) -> None:
        '''Setup'''
        self.backup = sys.stdout
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        if self.db == FILE:
            storage.__objects = {}

    def tearDown(self) -> None:
        '''Teardown'''
        try:
            remove(self.LOCAL_DB_NAME)
        except Exception:
            pass
        sys.stdout = self.backup

    def test_pep8(self) -> None:
        '''Test pep8 styling'''
        style = StyleGuide(quit=True)
        pep = style.check_files([self.CONSOLE_FILE])
        self.assertEqual(pep.total_errors, 0, 'Fix pycodestyle style')

    def test_docstring(self) -> None:
        '''Ensure each method has a Descriptiop'''
        self.assertIsNotNone(HBNBCommand.__doc__)
        Methods = [f for f in dir(HBNBCommand) if callable(
            getattr(HBNBCommand, f)) and not f.startswith('__')]
        for method in Methods:
            self.assertIsNotNone(method.__doc__)

    def test_emptyline(self) -> None:
        '''Test Empty line input'''
        console = self.__cmd
        console.onecmd('\n')
        stdout = self.capt_out.getvalue()
        self.assertEqual('', stdout)

    def test_quit(self) -> None:
        '''Test quit console'''
        console = self.__cmd
        with self.assertRaises(SystemExit):
            console.onecmd('quit')
            stdout = self.capt_out.getvalue()
            self.assertEqual('', stdout)

    def test_eof(self) -> None:
        '''Test EOF'''
        console = self.__cmd
        with self.assertRaises(SystemExit):
            self.assertTrue(console.onecmd('EOF'))

    def test_all(self) -> None:
        '''Test all cmd'''
        console = self.__cmd
        console.onecmd('all')
        stdout = self.capt_out.getvalue()
        self.assertTrue(isinstance(stdout, str))
    @unittest.skipIf(db == DB, 'Testing Database Storage Only')
    def test_show(self) -> None:
        '''Test show'''
        console = self.__cmd
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
        console = self.__cmd
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
        console = self.__cmd
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
        console = self.__cmd
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
        console = self.__cmd
        console.onecmd('create User email=mail@somemail.com password=abcijf')
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_class_name(self) -> None:
        ''' Test case missing class name'''
        console = self.__cmd
        console.onecmd('create')
        x = (self.capt_out.getvalue())
        self.assertEqual('** class name missing **\n', x)

    def test_class_name_doest_exist(self) -> None:
        '''Test case name does not exist'''
        console = self.__cmd
        console.onecmd('create Binita')
        x = (self.capt_out.getvalue())
        self.assertEqual('** class doesn\'t exist **\n', x)

    @unittest.skipIf(db != DB, 'Testing DBstorage only')
    def test_create_db(self) -> None:
        console = self.__cmd
        console.onecmd('create State name=California')
        result = storage.all('State')
        self.assertTrue(len(result))


if __name__ == '__main__':
    unittest.main()
