import os

os.environ['SBIS_PYTHON_UNITTEST'] = '1'
from sbis_root import *
import unittest
import uuid
import datetime
from datetime import date
from datetime import time


class IFieldRecordAPITests(unittest.TestCase):
    reason = 'Тест для версии выше 3.5.2 включительно'

    def setUp(self):
        format = CreateRecordFormat()
        self.record = CreateRecord(format)  # равнозначно self.record = Record()

    def test_add_set_get_record_bool(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddBool('bool_field', True)
        self.assertIsInstance(self.record.bool_field, bool)
        self.assertTrue(self.record.bool_field)
        self.assertTrue(bool(self.record['bool_field']))

        self.record.AddBool('bool_field_2')
        self.record['bool_field_2'].FromFalse()
        self.assertFalse(self.record.bool_field_2)
        self.assertFalse(bool(self.record['bool_field_2']))
        self.record['bool_field_2'].FromTrue()
        self.assertTrue(self.record.bool_field_2)
        self.assertTrue(bool(self.record['bool_field_2']))
        self.record['bool_field_2'].FromNull()
        self.assertIsNone(self.record.bool_field_2)

        self.record.AddBool('bool_field_3')
        self.record['bool_field_3'] = None
        self.assertIsNone(self.record.bool_field_3)

        self.record.AddBool('bool_field_4')
        self.record.bool_field_4 = True
        self.assertTrue(self.record.bool_field_4)
        self.assertTrue(bool(self.record['bool_field_4']))

        self.record.AddBool('bool_field_5')
        for val in [True, False, None]:
            self.record['bool_field_5'].From(val)
            self.assertEqual(self.record.bool_field_5, val)

    def test_add_set_get_record_string(self):
        '''Автор: Краснов Д.В.'''
        field_text = 'ЖЁЛТАЯ ФУТБОЛКА'
        self.record.AddString('string_field', field_text)
        self.assertIsInstance(self.record.string_field, str)
        self.assertEqual(self.record.string_field, field_text)
        self.assertEqual(str(self.record['string_field']), field_text)

        self.record.AddString('string_field_2')
        self.record['string_field_2'].From(field_text)
        self.assertEqual(self.record.string_field_2, field_text)
        self.assertEqual(str(self.record['string_field_2']), field_text)

        self.record.AddString('string_field_3')
        self.record['string_field_3'] = field_text
        self.assertEqual(self.record.string_field_3, field_text)
        self.assertEqual(str(self.record['string_field_3']), field_text)

        self.record.AddString('string_field_4')
        self.record.string_field_4 = field_text
        self.assertEqual(self.record.string_field_4, field_text)
        self.assertEqual(str(self.record['string_field_4']), field_text)

    def test_add_set_get_record_int64(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddInt64('int64_field', 64)
        self.assertIsInstance(self.record.int64_field, int)
        self.assertEqual(64, self.record.int64_field)
        self.assertEqual(64, int(self.record['int64_field']))

        self.record.AddInt64('int64_field_2')
        self.record['int64_field_2'].From(64)
        self.assertEqual(64, self.record.int64_field_2)
        self.assertEqual(64, int(self.record['int64_field_2']))

        self.record.AddInt64('int64_field_3')
        self.record['int64_field_3'] = 64
        self.assertEqual(64, self.record.int64_field_3)
        self.assertEqual(64, int(self.record['int64_field_3']))

        self.record.AddInt64('int64_field_4')
        self.record.int64_field_4 = 64
        self.assertEqual(64, self.record.int64_field_4)
        self.assertEqual(64, int(self.record['int64_field_4']))

    def test_add_set_get_record_int32(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddInt32('int32_field', 32)
        self.assertEqual(32, self.record.int32_field)
        self.assertEqual(32, int(self.record['int32_field']))

        self.record.AddInt32('int32_field_2')
        self.record['int32_field_2'].From(32)
        self.assertEqual(32, self.record.int32_field_2)
        self.assertEqual(32, int(self.record['int32_field_2']))

        self.record.AddInt32('int32_field_3')
        self.record['int32_field_3'] = 32
        self.assertEqual(32, self.record.int32_field_3)
        self.assertEqual(32, int(self.record['int32_field_3']))

        self.record.AddInt32('int32_field_4')
        self.record.int32_field_4 = 32
        self.assertEqual(32, self.record.int32_field_4)
        self.assertEqual(32, int(self.record['int32_field_4']))

    def test_add_set_get_record_int16(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddInt16('int16_field', 16)
        self.assertEqual(16, self.record.int16_field)
        self.assertEqual(16, int(self.record['int16_field']))

        self.record.AddInt16('int16_field_2')
        self.record['int16_field_2'].From(16)
        self.assertEqual(16, self.record.int16_field_2)
        self.assertEqual(16, int(self.record['int16_field_2']))

        self.record.AddInt16('int16_field_3')
        self.record['int16_field_3'] = 16
        self.assertEqual(16, self.record.int16_field_3)
        self.assertEqual(16, int(self.record['int16_field_3']))

        self.record.AddInt16('int16_field_4')
        self.record.int16_field_4 = 16
        self.assertEqual(16, self.record.int16_field_4)
        self.assertEqual(16, int(self.record['int16_field_4']))

    def test_add_set_get_record_int8(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddInt8('int8_field', 8)
        self.assertEqual(8, self.record.int8_field)
        self.assertEqual(8, int(self.record['int8_field']))

        self.record.AddInt8('int8_field_2')
        self.record['int8_field_2'].From(8)
        self.assertEqual(8, self.record.int8_field_2)
        self.assertEqual(8, int(self.record['int8_field_2']))

        self.record.AddInt8('int8_field_3')
        self.record['int8_field_3'] = 8
        self.assertEqual(8, self.record.int8_field_3)
        self.assertEqual(8, int(self.record['int8_field_3']))

        self.record.AddInt8('int8_field_4')
        self.record.int8_field_4 = 8
        self.assertEqual(8, self.record.int8_field_4)
        self.assertEqual(8, int(self.record['int8_field_4']))

    def test_add_set_get_record_float(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddFloat('float_field', 33.33)
        self.assertIsInstance(self.record.float_field, float)
        self.assertAlmostEqual(33.33, float(self.record['float_field']), delta=1e-5)  # Обратно в питон преобразует с ошибкой,
        self.assertAlmostEqual(33.33, float(self.record.float_field), delta=1e-5)     # с большей десятичной частью.

        self.record.AddFloat('float_field_2')
        self.record['float_field_2'].From(33.33)
        self.assertAlmostEqual(33.33, float(self.record['float_field_2']), delta=1e-5)
        self.assertAlmostEqual(33.33, float(self.record.float_field_2), delta=1e-5)

        self.record.AddFloat('float_field_3')
        self.record['float_field_3'] = 33.33
        self.assertAlmostEqual(33.33, float(self.record['float_field_3']), delta=1e-5)
        self.assertAlmostEqual(33.33, float(self.record.float_field_3), delta=1e-5)

        self.record.AddFloat('float_field_4')
        self.record.float_field_4 = 33.33
        self.assertAlmostEqual(33.33, float(self.record['float_field_4']), delta=1e-5)
        self.assertAlmostEqual(33.33, float(self.record.float_field_4), delta=1e-5)

    def test_add_set_get_record_double(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddDouble('double_field', 7.777)
        self.assertIsInstance(self.record.double_field, float)
        self.assertEqual(7.777, float(self.record['double_field']))
        self.assertEqual(7.777, float(self.record.double_field))

        self.record.AddDouble('double_field_2')
        self.record['double_field_2'].From(7.777)
        self.assertAlmostEqual(7.777, float(self.record['double_field_2']), delta=0.001)  # Обратно в питон преобразует с ошибкой,
        self.assertAlmostEqual(7.777, float(self.record.double_field_2), delta=0.001)     # с большей десятичной частью.

        self.record.AddDouble('double_field_3')
        self.record['double_field_3'] = 7.777
        self.assertEqual(7.777, float(self.record['double_field_3']))
        self.assertEqual(7.777, float(self.record.double_field_3))

        self.record.AddDouble('double_field_4')
        self.record.double_field_4 = 7.777
        self.assertEqual(7.777, float(self.record['double_field_4']))
        self.assertEqual(7.777, float(self.record.double_field_4))

    def test_add_set_get_record_date(self):
        '''Автор: Краснов Д.В.'''
        temp_date = date.today()
        self.record.AddDate('date_field', temp_date)
        self.assertIsInstance(self.record.date_field, date)
        self.assertIsInstance(self.record['date_field'].ToDate(), date)
        self.assertEqual(self.record.date_field, temp_date)
        self.assertEqual(self.record['date_field'].ToDate(), temp_date)

        self.record.AddDate('date_field_2')
        self.record['date_field_2'].From(temp_date)
        self.assertEqual(self.record.date_field_2, temp_date)
        self.assertEqual(self.record['date_field_2'].ToDate(), temp_date)

        self.record.AddDate('date_field_3')
        self.record['date_field_3'] = temp_date
        self.assertEqual(self.record.date_field_3, temp_date)
        self.assertEqual(self.record['date_field_3'].ToDate(), temp_date)

        self.record.AddDate('date_field_4')
        self.record.date_field_4 = temp_date
        self.assertEqual(self.record.date_field_4, temp_date)
        self.assertEqual(self.record['date_field_4'].ToDate(), temp_date)

    def test_add_set_get_record_time(self):
        '''Автор: Краснов Д.В.'''
        temp_time = time(16,45,30,123000)
        self.record.AddTime('time_field', temp_time)
        self.assertIsInstance(self.record.time_field, time)
        self.assertIsInstance(self.record['time_field'].ToTime(), time)
        self.assertEqual(self.record.time_field, temp_time)
        self.assertEqual(self.record['time_field'].ToTime(), temp_time)

        self.record.AddTime('time_field_2')
        self.record['time_field_2'].From(temp_time)
        self.assertEqual(self.record.time_field_2, temp_time)
        self.assertEqual(self.record['time_field_2'].ToTime(), temp_time)

        self.record.AddTime('time_field_3')
        self.record['time_field_3'] = temp_time
        self.assertEqual(self.record.time_field_3, temp_time)
        self.assertEqual(self.record['time_field_3'].ToTime(), temp_time)

        self.record.AddTime('time_field_4')
        self.record.time_field_4 = temp_time
        self.assertEqual(self.record.time_field_4, temp_time)
        self.assertEqual(self.record['time_field_4'].ToTime(), temp_time)

    def test_add_set_get_record_datetime(self):
        '''Автор: Краснов Д.В.'''
        temp_datetime = datetime.datetime(2013, 5, 23, 17, 12, 23, 234000)
        self.record.AddDateTime('datetime_field', temp_datetime)
        self.assertIsInstance(self.record.datetime_field, datetime.datetime)
        self.assertIsInstance(self.record['datetime_field'].ToDateTime(), datetime.datetime)
        self.assertEqual(self.record.datetime_field, temp_datetime)
        self.assertEqual(self.record['datetime_field'].ToDateTime(), temp_datetime)

        self.record.AddDateTime('datetime_field_2')
        self.record['datetime_field_2'].From(temp_datetime)
        self.assertEqual(self.record.datetime_field_2, temp_datetime)
        self.assertEqual(self.record['datetime_field_2'].ToDateTime(), temp_datetime)

        self.record.AddDateTime('datetime_field_3')
        self.record['datetime_field_3'] = temp_datetime
        self.assertEqual(self.record.datetime_field_3, temp_datetime)
        self.assertEqual(self.record['datetime_field_3'].ToDateTime(), temp_datetime)

        self.record.AddDateTime('datetime_field_4')
        self.record.datetime_field_4 = temp_datetime
        self.assertEqual(self.record.datetime_field_4, temp_datetime)
        self.assertEqual(self.record['datetime_field_4'].ToDateTime(), temp_datetime)

    def test_add_set_get_record_flags(self):
        '''Автор: Краснов Д.В.'''
        d = {0: 'first_value', 1: 'second_value', 2: 'third_value'}
        flags_values = [True, False, None]
        self.record.AddFlags('flags_field', NamedIndicesFromDict(d))
        self.record['flags_field'].From(flags_values)
        self.assertEqual(self.record.flags_field, flags_values)
        self.assertEqual(self.record['flags_field'].ToList(), flags_values)

        self.record.AddFlags('flags_field_2', NamedIndicesFromDict(d))
        self.record['flags_field_2'] = flags_values
        self.assertEqual(self.record.flags_field_2, flags_values)
        self.assertEqual(self.record['flags_field_2'].ToList(), flags_values)

        self.record.AddFlags('flags_field_3', NamedIndicesFromDict(d))
        self.record.flags_field_3 = flags_values
        self.assertEqual(self.record.flags_field_3, flags_values)
        self.assertEqual(self.record['flags_field_3'].ToList(), flags_values)

    @unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < '3.6.0', reason=reason)
    def test_add_set_get_record_money(self):
        """Автор: Т.Шувалова. Тестирую Record.AddMoney("key", "value")"""
        set_value = self.record.AddMoney
        name, value = 'm1', Money('999.999')
        set_value(name, value)
        self.assertAlmostEqual(float(self.record["m1"]), float(value), delta=0.01)

    @unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < '3.6.0', reason=reason)
    def test_add_format_money(self):
        """Автор: Т.Шувалова. Тестирую IRecordFormat.AddMoney("key", "value")"""
        mon_form = CreateRecordFormat()
        mon_form.AddMoney('m1')
        mon_form.AddMoney('m2')
        mon_form.AddMoney('m3')
        mon_form.AddMoney('m4', 123)
        self.assertRaises(Exception, mon_form.AddMoney, 'm3')

    @unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < '3.5.2', reason=reason)
    def test_add_set_get_record_enum(self):
        '''Автор: Краснов Д.В.'''
        d = {0: 'first_value', 1: 'second_value', 2: 'third_value'}
        field_value = 1
        self.record.AddEnum('enum_field', NamedIndicesFromDict(d))
        self.record['enum_field'].From(field_value)
        self.assertEqual(self.record.enum_field, field_value)
        self.assertEqual(int(self.record['enum_field']), field_value)

        self.record.AddEnum('enum_field_2', NamedIndicesFromDict(d))
        self.record['enum_field_2'] = EnumInfo(field_value)
        self.assertEqual(self.record.enum_field_2, field_value)
        self.assertEqual(int(self.record['enum_field_2']), field_value)

        self.record.AddEnum('enum_field_3', NamedIndicesFromDict(d))
        self.record.enum_field_3 = EnumInfo(field_value)
        self.assertEqual(self.record.enum_field_3, field_value)
        self.assertEqual(int(self.record['enum_field_3']), field_value)

    def test_add_set_get_record_record(self):
        '''Автор: Краснов Д.В.'''
        inc_rec = CreateRecordPointer()
        field_text = 'поле для вложенной записи'
        inc_rec.AddString('string_field', field_text)
        self.record.AddRecord('record_field', inc_rec.Format(), inc_rec)
        self.assertIsInstance(self.record['record_field'].RefRecord(), Record)
        self.assertEqual(str(self.record['record_field'].RefRecord()['string_field']), field_text)
        self.assertEqual(self.record['record_field'].RefRecord().string_field, field_text)

        self.record['record_field'].RefRecord().AddBool('boolean_field', True)
        self.record['record_field'].RefRecord().boolean_field = False
        self.assertFalse(self.record['record_field'].RefRecord().boolean_field)

    def test_add_set_get_record_recordset(self):
        '''Автор: Краснов Д.В.'''
        temp_format = CreateRecordFormat()
        temp_format.AddString('str_field')
        temp_format.AddBool('bool_field')
        inc_recordset = CreateRecordSet(temp_format)
        for i in [0, 1]:
            inc_recordset.InsRow(i)
            inc_recordset[i].str_field = 'ИДЁМ НА ОБЕД'
            inc_recordset[i].bool_field = True
        self.record.AddRecordSet('recordset_field', inc_recordset.get().Format(), inc_recordset)

        self.assertIsInstance(self.record['recordset_field'].RefRecordSet(), RecordSet)
        self.assertEqual(self.record['recordset_field'].RefRecordSet()[0].str_field, 'ИДЁМ НА ОБЕД')
        self.assertTrue(bool(self.record['recordset_field'].RefRecordSet()[1]['bool_field']))

    @unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < '3.5.2', reason=reason)
    def test_add_set_get_record_link(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddLink('link_field', 'some_table', LinkInfo(123))
        self.assertEqual(self.record.link_field, 123)
        self.assertEqual(int(self.record['link_field']), 123)

        self.record.AddLink('link_field_2', 'some_table_2', LinkInfo(98))
        self.record['link_field_2'].From(65)
        self.assertEqual(self.record.link_field_2, 65)
        self.assertEqual(int(self.record['link_field_2']), 65)

        self.record.AddLink('link_field_3', 'some_table_3', LinkInfo(7))
        self.record['link_field_3'] = 3
        self.assertEqual(self.record.link_field_3, 3)
        self.assertEqual(int(self.record['link_field_3']), 3)

        self.record.AddLink('link_field_4', 'some_table_4', LinkInfo(7))
        self.record.link_field_4 = LinkInfo(3)
        self.assertEqual(self.record.link_field_4, 3)
        self.assertEqual(int(self.record['link_field_4']), 3)

    def test_add_set_get_record_hierarchy(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddHierarchy('hierarchy_field_1', Hierarchy(ObjectId('obid_name', 734), BranchType.LEAF))
        self.assertIsInstance(self.record['hierarchy_field_1'].RefHierarchy(), Hierarchy)

        self.record.AddHierarchy('hierarchy_field_2')
        self.record['hierarchy_field_2'].From(Hierarchy(ObjectId('obid_name', 734), BranchType.HIDDEN))
        self.assertIsInstance(self.record['hierarchy_field_1'].RefHierarchy(), Hierarchy)

        self.record.AddHierarchy('hierarchy_field_3')
        self.record['hierarchy_field_3'] = Hierarchy(ObjectId('obid_name', 734), BranchType.HIDDEN)
        self.assertIsInstance(self.record['hierarchy_field_1'].RefHierarchy(), Hierarchy)

        self.record.AddHierarchy('hierarchy_field_4')
        self.record.hierarchy_field_4 = Hierarchy(ObjectId('obid_name', 734), BranchType.NODE)
        self.assertIsInstance(self.record['hierarchy_field_1'].RefHierarchy(), Hierarchy)

    def test_add_set_get_record_rpcfile(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddRpcFile('rpcfile_field', RpcFile())

        self.record['rpcfile_field'].From(RpcFile())
        self.record['rpcfile_field'] = RpcFile()
        self.record.rpcfile_field = RpcFile()
        self.assertIsInstance(self.record['rpcfile_field'].RefRpcFile(), RpcFile)

    def test_add_set_get_record_uuid(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddUuid('uuid_field', uuid.uuid4())
        self.assertIsInstance(self.record.uuid_field, uuid.UUID)

        value = uuid.uuid4()
        self.record['uuid_field'].From(value)
        self.assertEqual(self.record.uuid_field, value)

        value = uuid.uuid4()
        self.record['uuid_field'] = value
        self.assertEqual(self.record.uuid_field, value)

        value = uuid.uuid4()
        self.record.uuid_field = value
        self.assertEqual(self.record.uuid_field, value)

    def test_add_set_get_record_sortinglist(self):
        '''Автор: Краснов Д.В.'''
        sl = SortingList()
        c = ColumnSortParameters()
        c.fieldName = 'column1'
        sl.push_back(c)
        self.record.AddSortingList('sortinglist_field', sl)

    def test_add_set_get_record_navigation(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddNavigation('navigation_field', Navigation(10, 1, False))

    def test_add_set_get_record_array_bool(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayBool('array_bool_1')
        self.record['array_bool_1'].From([None, None, None])
        self.assertEqual(self.record['array_bool_1'].ToList(),[None, None, None])

        self.record.AddArrayBool('array_bool_2')
        self.record['array_bool_2'] = [False, False, False]
        self.assertEqual(self.record['array_bool_2'].ToList(),[False, False, False])

        self.record.AddArrayBool('array_bool_3')
        self.record.array_bool_3 = [None, None, None]
        self.assertEqual(self.record['array_bool_3'].ToList(),[None, None, None])

    def test_add_set_get_record_array_string(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayString('array_string_1')
        self.record['array_string_1'].From(['first', 'second', 'third'])
        self.assertEqual(self.record['array_string_1'].ToList(),['first', 'second', 'third'])

        self.record.AddArrayString('array_string_2')
        self.record['array_string_2'] = ['first', 'second', 'third']
        self.assertEqual(self.record['array_string_2'].ToList(),['first', 'second', 'third'])

        self.record.AddArrayString('array_string_3')
        self.record.array_string_3 = ['first', 'second', 'third']
        self.assertEqual(self.record['array_string_3'].ToList(),['first', 'second', 'third'])

    def test_add_set_get_record_array_float(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayFloat('array_float_1')
        self.record['array_float_1'].From([3.33, 2.22, 7.77])
        for left, right in zip(self.record['array_float_1'].ToList(), [3.33, 2.22, 7.77]):
            self.assertAlmostEqual(left, right, delta=1e-5)

        self.record.AddArrayFloat('array_float_2')
        self.record['array_float_2'] = [3.33, 2.22, 7.77]
        for left, right in zip(self.record['array_float_2'].ToList(), [3.33, 2.22, 7.77]):
            self.assertAlmostEqual(left, right, delta=1e-5)

        self.record.AddArrayFloat('array_float_3')
        self.record.array_float_3 = [3.33, 2.22, 7.77]
        for left, right in zip(self.record['array_float_3'].ToList(), [3.33, 2.22, 7.77]):
            self.assertAlmostEqual(left, right, delta=1e-5)

    def test_add_set_get_record_array_double(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayDouble('array_double_1')
        self.record['array_double_1'].From([3.33, 2.22, 7.77])
        for left, right in zip(self.record['array_double_1'].ToList(), [3.33, 2.22, 7.77]):
            self.assertAlmostEqual(left, right, delta=1e-5)

        self.record.AddArrayDouble('array_double_2')
        self.record['array_double_2'] = [3.33, 2.22, 7.77]
        for left, right in zip(self.record['array_double_2'].ToList(), [3.33, 2.22, 7.77]):
            self.assertAlmostEqual(left, right, delta=1e-5)

        self.record.AddArrayDouble('array_double_3')
        self.record.array_double_3 = [3.33, 2.22, 7.77]
        for left, right in zip(self.record['array_double_3'].ToList(), [3.33, 2.22, 7.77]):
            self.assertAlmostEqual(left, right, delta=1e-5)

    def test_add_set_get_record_array_int64(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayInt64('array_int64_1')
        self.record['array_int64_1'].From([1,2,3,4,5])
        self.assertEqual(self.record['array_int64_1'].ToList(),[1,2,3,4,5])

        self.record.AddArrayInt64('array_int64_2')
        self.record['array_int64_2'] = [1,2,3,4,5]
        self.assertEqual(self.record['array_int64_2'].ToList(),[1,2,3,4,5])

        self.record.AddArrayInt64('array_int64_3')
        self.record.array_int64_3 = [1,2,3,4,5]
        self.assertEqual(self.record['array_int64_3'].ToList(),[1,2,3,4,5])

    def test_add_set_get_record_array_int32(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayInt32('array_int32_1')
        self.record['array_int32_1'].From([1,2,3,4,5])
        self.assertEqual(self.record['array_int32_1'].ToList(),[1,2,3,4,5])

        self.record.AddArrayInt32('array_int32_2')
        self.record['array_int32_2'] = [1,2,3,4,5]
        self.assertEqual(self.record['array_int32_2'].ToList(),[1,2,3,4,5])

        self.record.AddArrayInt32('array_int32_3')
        self.record.array_int32_3 = [1,2,3,4,5]
        self.assertEqual(self.record['array_int32_3'].ToList(),[1,2,3,4,5])

    def test_add_set_get_record_array_int16(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayInt16('array_int16_1')
        self.record['array_int16_1'].From([1,2,3,4,5])
        self.assertEqual(self.record['array_int16_1'].ToList(),[1,2,3,4,5])

        self.record.AddArrayInt16('array_int16_2')
        self.record['array_int16_2'] = [1,2,3,4,5]
        self.assertEqual(self.record['array_int16_2'].ToList(),[1,2,3,4,5])

        self.record.AddArrayInt16('array_int16_3')
        self.record.array_int16_3 = [1,2,3,4,5]
        self.assertEqual(self.record['array_int16_3'].ToList(),[1,2,3,4,5])

    def test_add_set_get_record_array_uuid(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayUuid('array_uuid_1')
        self.record['array_uuid_1'].From([uuid.uuid4() for i in range(4)])
        self.assertIsInstance(self.record['array_uuid_1'].ToList()[0], uuid.UUID)

        self.record.AddArrayUuid('array_uuid_2')
        self.record['array_uuid_2'] = [uuid.uuid4() for i in range(4)]
        self.assertIsInstance(self.record['array_uuid_2'].ToList()[0], uuid.UUID)

        self.record.AddArrayUuid('array_uuid_3')
        self.record.array_uuid_3 = [uuid.uuid4() for i in range(4)]
        self.assertIsInstance(self.record['array_uuid_3'].ToList()[0], uuid.UUID)

    def test_add_set_get_record_array_money(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddArrayMoney('array_money_1')
        self.record['array_money_1'].From([Money(1.22), Money(1.33)])
        for m in self.record.array_money_1:
            self.assertIsInstance(m, Money)

        self.record.AddArrayMoney('array_money_2')
        self.record['array_money_2'] = [Money(1.22), Money(1.33)]
        for m in self.record.array_money_2:
            self.assertIsInstance(m, Money)

        self.record.AddArrayMoney('array_money_3')
        self.record.array_money_3 = [Money(1.22), Money(1.33)]
        for m in self.record['array_money_3'].ToList():
            self.assertIsInstance(m, Money)

    def test_add_set_get_record_array_date(self):
        '''Автор: Краснов Д.В.'''
        temp_date = date.today()
        self.record.AddArrayDate('array_date_1')
        self.record['array_date_1'].From([temp_date, temp_date, temp_date])
        for d in self.record.array_date_1:
            self.assertIsInstance(d, date)

        self.record.AddArrayDate('array_date_2')
        self.record['array_date_2'] = [temp_date, temp_date, temp_date]
        for d in self.record['array_date_2'].ToList():
            self.assertEqual(d, temp_date)

        self.record.AddArrayDate('array_date_3')
        self.record.array_date_3 = [temp_date, temp_date, temp_date]
        for d in self.record['array_date_3'].ToList():
            self.assertEqual(d, temp_date)

    def test_add_set_get_record_array_time(self):
        '''Автор: Краснов Д.В.'''
        temp_time = time(16,45,30,123000)
        self.record.AddArrayTime('array_time_1')
        self.record['array_time_1'].From([temp_time, temp_time, temp_time])
        for t in self.record.array_time_1:
            self.assertIsInstance(t, time)

        self.record.AddArrayTime('array_time_2')
        self.record['array_time_2'] = [temp_time, temp_time, temp_time]
        for t in self.record.array_time_2:
            self.assertEqual(t, temp_time)

        self.record.AddArrayTime('array_time_3')
        self.record.array_time_3 = [temp_time, temp_time, temp_time]
        for t in self.record['array_time_3'].ToList():
            self.assertEqual(t, temp_time)

    def test_add_set_get_record_array_datetime(self):
        '''Автор: Краснов Д.В.'''
        temp_datetime = datetime.datetime(2013, 5, 23, 17, 12, 23, 234000)
        self.record.AddArrayDateTime('array_datetime_1')
        self.record['array_datetime_1'].From([temp_datetime, temp_datetime, temp_datetime])
        for dt in self.record.array_datetime_1:
            self.assertIsInstance(dt, datetime.datetime)

        self.record.AddArrayDateTime('array_datetime_2')
        self.record['array_datetime_2'] = [temp_datetime, temp_datetime, temp_datetime]
        for dt in self.record.array_datetime_2:
            self.assertEqual(dt, temp_datetime)

        self.record.AddArrayDateTime('array_datetime_3')
        self.record.array_datetime_3 = [temp_datetime, temp_datetime, temp_datetime]
        for dt in self.record['array_datetime_3'].ToList():
            self.assertEqual(dt, temp_datetime)

    def test_add_get_record_append(self):
        '''Автор: Краснов Д.В.'''
        rec = Record()
        self.record.AppendField(rec.AddBool('bool_field').Format())
        self.record.AppendField(rec.AddInt64('int64_field').Format())
        self.record.AppendField(rec.AddInt32('int32_field').Format())
        self.record.AppendField(rec.AddInt16('int16_field').Format())
        self.record.AppendField(rec.AddInt8('int8_field').Format())
        self.record.AppendField(rec.AddFloat('float_field').Format())
        self.record.AppendField(rec.AddDouble('double_field').Format())
        self.record.AppendField(rec.AddDate('date_field').Format())
        self.record.AppendField(rec.AddTime('time_field').Format())
        self.record.AppendField(rec.AddDateTime('datetime_field').Format())
        self.record.AppendField(rec.AddFlags('flags_field', NamedIndicesFromDict({1:'flag_1'})).Format())
        self.record.AppendField(rec.AddEnum('enum_field', NamedIndicesFromDict({1:'field_1'})).Format())
        self.record.AppendField(rec.AddRecord('record_field', CreateRecordFormat(), CreateRecordPointer()).Format())
        self.record.AppendField(rec.AddRecordSet('recordset_field', CreateRecordFormat(), CreateRecordSet(CreateRecordFormat())).Format())
        self.record.AppendField(rec.AddLink('link_field', 'some_table', LinkInfo(111)).Format())

        self.record.AppendField('_int64_field', FieldType.ftINT64, 0)
        self.record.AppendField('_double_field', FieldType.ftDOUBLE, 0)
        self.record.AppendField('_string_field', FieldType.ftSTRING, 0)
        self.record.AppendField('_record_field', FieldType.ftRECORD, 0)
        self.record.AppendField('_link_field', FieldType.ftLINK_HIER, 0)

        self.assertEqual(self.record['_int64_field'].Type(), FieldType.ftINT64)
        self.assertEqual(self.record['_double_field'].Type(), FieldType.ftDOUBLE)
        self.assertEqual(self.record['_string_field'].Type(), FieldType.ftSTRING)
        self.assertEqual(self.record['_record_field'].Type(), FieldType.ftRECORD)
        self.assertEqual(self.record['_link_field'].Type(), FieldType.ftLINK_HIER)

    def test_null_name_type_field_methods(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddString('string_field')

        self.assertTrue(self.record[0].IsNull())
        self.assertEqual(self.record[0].Name(), 'string_field')
        self.assertEqual(self.record[0].Type(), FieldType.ftSTRING)

    def test_obj_iteration_record(self):
        '''Автор: Краснов Д.В.'''
        self.record.Reserve(100)
        for i in range(100):
            self.record.AddString('string_field_'+str(i), 'значение_'+str(i))

        for i in self.record:
            self.assertIsNotNone(i)

    def test_index_iteration_record(self):
        '''Автор: Краснов Д.В.'''
        self.record.Reserve(100)
        for i in range(100):
            self.record.AddString('string_field_'+str(i), 'значение_'+str(i))

        for i in range(len(self.record)):
            self.assertIsNotNone(self.record[i])

        for i in range(self.record.Count()):
            self.assertIsNotNone(self.record[i])

    @unittest.skip('ошибка в работе метода record.Remove()')
    def test_remove_record(self):
        '''Автор: Краснов Д.В.'''
        count = 100
        self.record.Reserve(count)
        for i in range(count):
            self.record.AddString('string_field_'+str(i), 'значение_'+str(i))

        for i in range(count):
            if i < 50:
                self.record.Remove('string_field_'+str(i))
            else:
                self.record.Remove(i)
        self.assertEqual(len(self.record), 0)

    def test_get_record_field_name(self):
        '''Автор: Краснов Д.В.'''
        self.record.AddBool('bool', True)

        self.assertEqual(self.record.FieldName(0), 'bool')
