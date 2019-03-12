from django.test import TestCase
from db_manager import db_connector, db_getters, db_errors
# Create your tests here.


class DBManagerGetValueFromHermesCases(TestCase):
    cur = None
    conn = None

    def setUp(self):
        setup_temp = db_connector.connect2django()
        self.cur = setup_temp['cur']
        self.conn = setup_temp['conn']

    def tearDown(self):
        db_connector.close_db_connection(cur=self.cur, conn=self.conn)

    def test_get_value_from_hermes(self):
        self.cur.execute('select test_column1 from hermes.test where test_id=1')
        result = self.cur.fetchone()[0]

        expected = db_getters.get_values_from_hermes(get_values_id='1', table_name='test',
                                                     column='test_column1')

        self.assertEqual(result, expected['test_column1'])
        self.assertFalse(expected['error'])

    def test_get_value_from_hermes_invalid_table_name(self):
        expected = db_getters.get_values_from_hermes(get_values_id='1', table_name='testX',
                                                     column='test_column1')

        self.assertTrue(expected['error'])
        self.assertTrue(expected['message'] is not None)

    def test_get_value_from_hermes_not_id(self):
        expected = db_getters.get_values_from_hermes(get_values_id='300', table_name='test',
                                                     column='test_column1')

        self.assertTrue(expected['error'])
        self.assertTrue(expected['message'] is not None)

    def test_get_value_from_hermes_invalid_column_name(self):
        expected = db_getters.get_values_from_hermes(get_values_id='1', table_name='test',
                                                     column='test_column300')

        self.assertTrue(expected['error'])
        self.assertTrue(expected['message'] is not None)


class DBManagerGetTwimlXmlCases(TestCase):
    cur = None
    conn = None

    def setUp(self):
        setup_temp = db_connector.connect2django()
        self.cur = setup_temp['cur']
        self.conn = setup_temp['conn']

    def tearDown(self):
        db_connector.close_db_connection(cur=self.cur, conn=self.conn)

    def test_get_twiml_xml(self):
        self.cur.execute('select twiml_xml from hermes.test where test_id=2')
        result = self.cur.fetchone()[0]

        expected = db_getters.get_twiml_xml(get_twiml_id='2', get_twiml_table_name='test')

        self.assertEqual(result, expected['twiml_xml'])
        self.assertFalse(expected['error'])

    def test_get_twiml_xml_invalid_id(self):
        expected = db_getters.get_values_from_hermes(get_values_id='5', table_name='test',
                                                     column='twiml_xml')

        self.assertTrue(expected['error'])
        self.assertTrue(expected['message'] is not None)


class DBManagerGetGatherTaskCases(TestCase):
    cur = None
    conn = None

    def setUp(self):
        setup_temp = db_connector.connect2django()
        self.cur = setup_temp['cur']
        self.conn = setup_temp['conn']

    def tearDown(self):
        db_connector.close_db_connection(cur=self.cur, conn=self.conn)

    def test_get_gather_task(self):
        self.cur.execute("select var_values from hermes.task where task_id='660902047gather'")
        result = self.cur.fetchone()[0]

        expected = db_getters.get_task(id_value='660902047', task_name='gather')

        self.assertEqual(result, expected['var_values'])
        self.assertFalse(expected['error'])

    def test_get_gather_task_invalid_id(self):
        expected = db_getters.get_task(id_value='300', task_name='gather')

        self.assertTrue(expected['error'])
        self.assertTrue(expected['message'] is not None)

