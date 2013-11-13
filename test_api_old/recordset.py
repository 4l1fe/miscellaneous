import os

os.environ['SBIS_PYTHON_UNITTEST'] = '1'
from sbis_root import *
import unittest
import datetime
from datetime import time


class RecordSetAPITests(unittest.TestCase):
    reason = 'Тест для версии выше 3.5.2 включительно'

    def setUp(self):
        temp_format = CreateRecordFormat()
        temp_format.AddString('string_field')
        temp_format.AddBool('bool_field')
        temp_format.AddInt8('int8_field')
        temp_format.AddInt16('int16_field')
        temp_format.AddInt32('int32_field')
        temp_format.AddInt64('int64_field')
        temp_format.AddFloat('float_field')
        temp_format.AddDouble('double_field')
        temp_format.AddRecord('record_field', CreateRecordFormat())
        temp_format.AddRecordSet('recordset_field', CreateRecordFormat())
        
        self.recordset = CreateRecordSet(temp_format)

    def test_set_get_recordset_string_val(self):
        '''Автор: Краснов Д.В.'''
        for i in range(2):
            self.recordset.InsRow(i)
            self.recordset[i]['string_field'] = 'value_'+str(i)

        self.assertEqual(self.recordset.GetString(0, 0), 'value_0')
        self.assertEqual(self.recordset.GetString(1, 'string_field'), 'value_1')

    def test_set_get_recordset_bool_val(self):
        '''Автор: Краснов Д.В.'''
        for i, val in enumerate([True, False, None]):
            self.recordset.InsRow(i)
            self.recordset[i]['bool_field'] = val

        self.assertTrue(self.recordset.GetBool(0, 1))
        self.assertFalse(self.recordset.GetBool(1, 1))
        self.assertIsNone(self.recordset[2].bool_field)

    def test_set_get_recordset_int8_val(self):
        '''Автор: Краснов Д.В.'''
        for i in range(2):
            self.recordset.InsRow(i)
            self.recordset[i]['int8_field'] = i

        self.assertEqual(self.recordset.GetInt8(0, 2), 0)
        self.assertEqual(self.recordset.GetInt8(1, 'int8_field'), 1)

    def test_set_get_recordset_int16_val(self):
        '''Автор: Краснов Д.В.'''
        for i in range(2):
            self.recordset.InsRow(i)
            self.recordset[i]['int16_field'] = i

        self.assertEqual(self.recordset.GetInt16(0, 3), 0)
        self.assertEqual(self.recordset.GetInt16(1, 'int16_field'), 1)

    def test_set_get_recordset_int32_val(self):
        '''Автор: Краснов Д.В.'''
        for i in range(2):
            self.recordset.InsRow(i)
            self.recordset[i]['int32_field'] = i

        self.assertEqual(self.recordset.GetInt32(0, 4), 0)
        self.assertEqual(self.recordset.GetInt32(1, 'int32_field'), 1)

    def test_set_get_recordset_int64_val(self):
        '''Автор: Краснов Д.В.'''
        for i in range(2):
            self.recordset.InsRow(i)
            self.recordset[i]['int64_field'] = i

        self.assertEqual(self.recordset.GetInt64(0, 5), 0)
        self.assertEqual(self.recordset.GetInt64(1, 'int64_field'), 1)

    def test_set_get_recordset_float_val(self):
        '''Автор: Краснов Д.В.'''
        for i in range(2):
            self.recordset.InsRow(i)
            self.recordset[i]['float_field'] = (i+1)*3.3

        self.assertAlmostEqual(self.recordset.GetFloat(0, 6), 3.3, delta=1e-5)
        self.assertAlmostEqual(self.recordset.GetFloat(1, 'float_field'), 6.6, delta=1e-5)

    def test_set_get_recordset_double_val(self):
        '''Автор: Краснов Д.В.'''
        for i in range(2):
            self.recordset.InsRow(i)
            self.recordset[i]['double_field'] = (i+1)*3.3

        self.assertEqual(self.recordset.GetDouble(0, 7), 3.3)
        self.assertEqual(self.recordset.GetDouble(1, 'double_field'), 6.6)

    def test_set_get_recordset_record_val(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset[0]['record_field'] = CreateRecordPointer()
        self.recordset[0]['record_field'].RefRecord().AddString('string_field', 'inc_value')

        self.assertEqual(str(self.recordset.GetRecord(0, 8)['string_field']), 'inc_value')
        self.assertEqual(self.recordset.GetRecord(0, 'record_field').string_field, 'inc_value')

    def test_set_get_recordset_recordset_val(self):
        '''Автор: Краснов Д.В.'''
        inc_format = CreateRecordFormat()
        inc_format.AddBool('bool_field')
        inc_format.AddInt64('int64_field')
        self.recordset.InsRow(0)
        self.recordset[0]['recordset_field'] = CreateRecordSet(inc_format)
        self.recordset[0]['recordset_field'].RefRecordSet().InsRow(0)
        self.recordset[0]['recordset_field'].RefRecordSet()[0]['bool_field'] = True
        self.recordset[0]['recordset_field'].RefRecordSet()[0].int64_field = 73

        self.assertTrue(bool(self.recordset.GetRecordSet(0, 9)[0]['bool_field']))
        self.assertEqual(self.recordset.GetRecordSet(0, 'recordset_field')[0].int64_field, 73)

    def test_add_recordset_nested_record_field_val(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset[0]['record_field'] = CreateRecordPointer()
        self.recordset[0]['record_field'].RefRecord().AddString('string_field', 'inc_value')

    def test_add_recordset_nested_recordset_record_field_val(self):
        '''Автор: Краснов Д.В.'''
        inc_format = CreateRecordFormat()
        self.recordset.InsRow(0)
        self.recordset[0]['recordset_field'] = CreateRecordSet(inc_format)
        self.recordset[0]['recordset_field'].RefRecordSet().InsRow(0)

    def test_add_recordset_col_bool(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColBool('additional_bool_field', 0)
        self.recordset[0].additional_bool_field = True
        self.assertTrue(self.recordset[0].additional_bool_field)

    def test_add_recordset_col_int16(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColInt16('additional_int16_field', 0)
        self.recordset[0].additional_int16_field = 16
        self.assertEqual(self.recordset[0].additional_int16_field, 16)

    def test_add_recordset_col_int32(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColInt32('additional_int32_field', 0)
        self.recordset[0].additional_int32_field = 32
        self.assertEqual(self.recordset[0].additional_int32_field, 32)

    def test_add_recordset_col_int64(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColInt64('additional_int64_field', 0)
        self.recordset[0].additional_int64_field = 64
        self.assertEqual(self.recordset[0].additional_int64_field, 64)

    def test_add_recordset_col_string(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColString('additional_string_field', 0)
        self.recordset[0].additional_string_field = 'some_string'
        self.assertEqual(self.recordset[0].additional_string_field, 'some_string')

    def test_add_recordset_col_float(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColFloat('additional_float_field', 0)
        self.recordset[0].additional_float_field = 44.33
        self.assertAlmostEqual(44.33, float(self.recordset[0].additional_float_field), delta=1e-5)

    def test_add_recordset_col_double(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColDouble('additional_double_field', 0)
        self.recordset[0].additional_double_field = 44.55
        self.assertAlmostEqual(44.55, float(self.recordset[0].additional_double_field), delta=1e-5)

    def test_add_recordset_col_record(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColRecord('additional_record_field', 0)
        self.recordset[0].additional_record_field = CreateRecordPointer()
        self.assertIsInstance(self.recordset[0].additional_record_field, Record)

    def test_add_recordset_col_datetime(self):
        '''Автор: Краснов Д.В.'''
        temp_datetime = datetime.datetime(2013, 7, 26, 12, 39, 23, 111000)
        self.recordset.InsRow(0)
        self.recordset.AddColDateTime('additional_datetime_field', 0)
        self.recordset[0].additional_datetime_field = temp_datetime
        self.assertEqual(self.recordset[0].additional_datetime_field, temp_datetime)

    def test_add_recordset_col_time(self):
        '''Автор: Краснов Д.В.'''
        temp_time = time(12,45,20,123000)
        self.recordset.InsRow(0)
        self.recordset.AddColTime('additional_time_field', 0)
        self.recordset[0].additional_time_field = temp_time
        self.assertEqual(self.recordset[0].additional_time_field, temp_time)

    @unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < '3.5.2', reason=reason)
    def test_add_recordset_col_hierarchy(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        self.recordset.AddColHierarchy('additional_hierarchy_field', 0)
        self.recordset[0].additional_hierarchy_field = Hierarchy()
        self.assertEqual(self.recordset[0].additional_hierarchy_field.Branch, BranchType.LEAF)

    def test_ins_recordset_col_bool(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 3
        self.recordset.InsColBool(index, 'ins_bool_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_bool_field')

    def test_ins_recordset_col_int16(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 4
        self.recordset.InsColInt16(index, 'ins_int16_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_int16_field')

    def test_ins_recordset_col_int32(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 0
        self.recordset.InsColInt32(index, 'ins_int32_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_int32_field')

    def test_ins_recordset_col_int64(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 1
        self.recordset.InsColInt16(index, 'ins_int64_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_int64_field')

    def test_ins_recordset_col_string(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 3
        self.recordset.InsColBool(index, 'ins_string_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_string_field')

    def test_ins_recordset_col_float(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 2
        self.recordset.InsColFloat(index, 'ins_float_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_float_field')

    def test_ins_recordset_col_double(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 3
        self.recordset.InsColDouble(index, 'ins_double_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_double_field')

    def test_ins_recordset_col_record(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 3
        self.recordset.InsColRecord(index, 'ins_record_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_record_field')

    def test_ins_recordset_col_datetime(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 3
        self.recordset.InsColDateTime(index, 'ins_datetime_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_datetime_field')

    def test_ins_recordset_col_time(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 3
        self.recordset.InsColTime(index, 'ins_time_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_time_field')

    def test_ins_recordset_col_hierarchy(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.InsRow(0)
        index = 3
        self.recordset.InsColHierarchy(index, 'ins_hierarchy_field', 0)
        self.assertEqual(self.recordset[0][index].Name(), 'ins_hierarchy_field')

    def test_add_recordset_row(self):
        '''Автор: Краснов Д.В.'''
        init_len = len(self.recordset)
        self.recordset.AddRow()
        self.assertEqual(init_len+1, len(self.recordset))

    def test_add_recordset_row_2(self):
        '''Автор: Краснов Д.В.'''
        init_len = len(self.recordset)
        rec = Record()
        rec.AddString('string_field', 'text')
        self.recordset.AddRow(rec)
        self.assertEqual(init_len+1, len(self.recordset))

    def test_migrate_recordset_format(self):
        '''Автор: Краснов Д.В.'''
        self.recordset.AddRow()
        self.recordset[0].string_field = 'some_text'
        self.recordset[0].bool_field = True
        self.recordset[0].int8_field = 8
        new_frmt = CreateRecordFormat()
        new_frmt.AddString('string_field')
        new_frmt.AddBool('bool_field')
        new_frmt.AddInt8('int8_field')
        new_frmt.AddString('string2_field')
        new_frmt.AddBool('bool2_field')
        self.recordset.Migrate(new_frmt)
        self.assertEqual(len(self.recordset[0]), 5)
        self.assertEqual(self.recordset[0].string_field, 'some_text')
        self.assertTrue(self.recordset[0].bool_field)
        self.assertEqual(self.recordset[0].int8_field, 8)

    def test_other_recordset_methods(self):
        '''Автор: Краснов Д.В.'''
        for i in range(50):
            self.recordset.InsRow(i)

        self.assertEqual(self.recordset.Size(), 50)
        self.assertEqual(len(self.recordset), 50)
        self.assertFalse(self.recordset.Empty())
        self.assertTrue(self.recordset.IsNull(0, 2))
        self.assertTrue(self.recordset.IsNull(1, 'float_field'))
        init_len = len(self.recordset[0])
        self.recordset.DelCol(0)
        self.assertEqual(init_len-1, len(self.recordset[0]))

        self.recordset.DelRow(49)
        with self.assertRaises(Error):  # RuntimeError: Выход за границы набора данных.
            rec = self.recordset[49]           # Запрошена строка 49, всего строк 49

    def test_iteration_recordset(self):
        '''Автор: Краснов Д.В.'''
        for i in range(100):
            self.recordset.InsRow(i)
            self.recordset[i]['bool_field'].FromTrue()

        for i in range(len(self.recordset)):
            self.assertTrue(self.recordset[i].bool_field)

        for record in self.recordset:
            self.assertTrue(record.bool_field)
