import os

os.environ['SBIS_PYTHON_UNITTEST'] = '1'
from sbis_root import *
import unittest


class IFieldRecordFormatAPITests(unittest.TestCase):
    reason = 'Тест для версии выше 3.5.2 включительно'

    # Вспомогательный метод.
    def assert_name_setname_clone(self):
        self.format[0].SetName('new_field_name')
        self.assertEqual(self.format[0].Name(), 'new_field_name')

        clone = self.format[0].Clone()
        self.assertEqual(clone.Name(), 'new_field_name')

        self.format['new_field_name'].SetName('other_field_name')
        self.assertEqual(self.format[0].Name(), 'other_field_name')

    def setUp(self):
        self.format = CreateRecordFormat()

    def test_add_set_get_format_bool(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddBool('bool_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_string(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddString('str_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_int64(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddInt64('int64_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_int32(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddInt32('int32_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_int16(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddInt16('int16_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_int8(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddInt8('int8_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_float(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddFloat('float_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_double(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddDouble('double_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_date(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddDate('date_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_time(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddTime('time_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_datetime(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddDateTime('datetime_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_flags(self):
        '''Автор: Краснов Д.В.'''
        d = {0: 'flag1', 1: 'flag2', 2: 'flag3'}
        self.format.AddFlags('flags_field', NamedIndicesFromDict(d), 0)
        self.assertEqual(self.format[0].Dictionary().as_dict, d)

        self.assert_name_setname_clone()

        self.format[0].SetDictionary(NamedIndicesFromDict(d))
        self.assertEqual(self.format[0].Dictionary().as_dict, d)
        self.assertEqual(self.format[0].NameOfIndex(0), d[0])
        self.assertEqual(self.format[0].IndexOfName('flag2'), 1)
        self.assertTrue(self.format[0].IsNamedIndex(0))
        self.assertFalse(self.format[0].IsNamedIndex(3))
        self.assertTrue(self.format[0].HasIndexName('flag1'))
        self.assertFalse(self.format[0].HasIndexName('flag4'))

    def test_add_set_get_format_enum(self):
        '''Автор: Краснов Д.В.'''
        d = {0: 'enum1', 1: 'enum2', 2: 'enum3'}
        self.format.AddEnum('enum_field', NamedIndicesFromDict(d), 0)
        self.assertEqual(self.format[0].Dictionary().as_dict, d)

        self.assert_name_setname_clone()

        self.format[0].SetDictionary(NamedIndicesFromDict(d))
        self.assertEqual(self.format[0].Dictionary().as_dict, d)
        self.assertEqual(self.format[0].NameOfIndex(0), d[0])
        self.assertEqual(self.format[0].IndexOfName('enum2'), 1)
        self.assertTrue(self.format[0].IsNamedIndex(0))
        self.assertFalse(self.format[0].IsNamedIndex(3))
        self.assertTrue(self.format[0].HasIndexName('enum1'))
        self.assertFalse(self.format[0].HasIndexName('enum4'))

    def test_add_set_get_format_record(self):
        '''Автор: Краснов Д.В.'''
        rec_format_ptr = CreateRecordFormat()
        self.format.AddRecord('record_field', rec_format_ptr)
        self.assertEqual(self.format[0].Name(), 'record_field')

        self.assert_name_setname_clone()

        nested_format_ptr = self.format[0].NestedRecFormat()
        nested_format = nested_format_ptr.get()
        nested_format.AddString('string_field')
        self.assertEqual(nested_format[0].Name(), 'string_field')

        own_nested_format_ptr = self.format[0].OwnNestedRecFormat()
        own_nested_format = own_nested_format_ptr.get()
        self.assertIsNone(own_nested_format)

    def test_add_set_get_format_recordset(self):
        '''Автор: Краснов Д.В.'''
        temp_format_ptr = CreateRecordFormat()
        temp_format = temp_format_ptr.get()
        temp_format.AddString('string_field')
        temp_format.AddBool('bool_field')
        self.format.AddRecordSet('recordset_field', temp_format_ptr)

        self.assert_name_setname_clone()

        nested_recset_ptr = self.format[0].NestedRecFormat()
        nested_recset = nested_recset_ptr.get()
        self.assertEqual(nested_recset[0].Name(), 'string_field')

        own_nested_format_ptr = self.format[0].OwnNestedRecFormat()
        own_nested_format = own_nested_format_ptr.get()
        self.assertIsNone(own_nested_format)

    def test_add_set_get_format_link(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddLink('link_field', 'some_table')

        self.assert_name_setname_clone()

        self.assertEqual(self.format[0].LinkedTable(), 'some_table')
        self.format[0].SetLinkedTable('new_table')
        self.assertEqual(self.format[0].LinkedTable(), 'new_table')

    def test_add_set_get_format_uuid(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddUuid('uuid_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_rpc_file(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddRpcFile('rpcfile_field')

        self.assert_name_setname_clone()

    @unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < '3.5.2', reason=reason)
    def test_add_set_get_format_sorting(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddSortingList('sorting_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_navigation(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddNavigation('navigation_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_bool(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayBool('array_bool_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_string(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayString('array_string_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_uuid(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayUuid('array_uuid_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_int16(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayInt16('array_int16_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_int32(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayInt32('array_int32_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_int64(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayInt64('array_int64_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_float(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayFloat('array_float_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_double(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayDouble('array_double_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_money(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayMoney('array_money_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_date(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayDate('array_date_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_time(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayTime('array_time_field')

        self.assert_name_setname_clone()

    def test_add_set_get_format_array_datetime(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddArrayDateTime('array_datetime_field')

        self.assert_name_setname_clone()

    def test_format_add_method(self):
        '''Автор: Краснов Д.В.'''
        self.format.Add('bool_field', FieldType.ftBOOLEAN, 0)
        self.format.Add('string_field', FieldType.ftSTRING, 0)
        self.format.Add('int64_field', FieldType.ftINT64, 0)
        self.format.Add('int32_field', FieldType.ftINT32, 0)
        self.format.Add('int16_field', FieldType.ftINT16, 0)
        self.format.Add('int8_field', FieldType.ftINT8, 0)
        self.format.Add('float_field', FieldType.ftFLOAT, 0)
        self.format.Add('double_field', FieldType.ftDOUBLE, 0)
        self.format.Add('date_field', FieldType.ftDATE, 0)
        self.format.Add('time_field', FieldType.ftTIME, 0)
        self.format.Add('datetime_field', FieldType.ftDATETIME, 0)
        self.format.Add('flags_field', FieldType.ftFLAGS, 0)
        self.format.Add('enum_field', FieldType.ftENUM, 0)
        self.format.Add('record_field', FieldType.ftRECORD, 0)
        self.format.Add('recordset_field', FieldType.ftRECORDSET, 0)
        self.format.Add('link_field', FieldType.ftLINK_HIER, 0)
        self.format.Add('uuid_field', FieldType.ftUUID, 0)
        self.format.Add('rpcfile_field', FieldType.ftRPC_FILE, 0)
        self.format.Add('sorting_field', FieldType.ftSORTING, 0)
        self.format.Add('navigation_field', FieldType.ftNAVIGATION, 0)
        self.format.AddArrayBool('array_bool_field', FieldType.ftARRAY_BOOLEAN)
        self.format.AddArrayString('array_string_field', FieldType.ftARRAY_TEXT)
        self.format.AddArrayUuid('array_uuid_field', FieldType.ftARRAY_UUID)
        self.format.AddArrayInt64('array_int64_field', FieldType.ftARRAY_INT64)
        self.format.AddArrayInt32('array_int32_field', FieldType.ftARRAY_INT32)
        self.format.AddArrayInt16('array_int16_field', FieldType.ftARRAY_INT16)
        self.format.AddArrayFloat('array_float_field', FieldType.ftARRAY_FLOAT)
        self.format.AddArrayDouble('array_double_field', FieldType.ftARRAY_DOUBLE)
        self.format.AddArrayMoney('array_money_field', FieldType.ftARRAY_MONEY)
        self.format.AddArrayDate('array_date_field', FieldType.ftARRAY_DATE)
        self.format.AddArrayTime('array_time_field', FieldType.ftARRAY_TIME)
        self.format.AddArrayDateTime('array_datetime_field', FieldType.ftARRAY_DATETIME)

    def test_index_iteration_format(self):
        '''Автор: Краснов Д.В.'''
        self.format.Reserve(100)
        for i in range(100):
            self.format.AddString('string_field_'+str(i))

        for i in range(len(self.format)):
            self.assertTrue(self.format[i])

        for i in range(self.format.Count()):
            self.assertTrue(self.format[i])

    @unittest.skip('ошибка в работе метода format.Remove()')
    def test_remove_format(self):
        '''Автор: Краснов Д.В.'''
        count = 100
        self.format.Reserve(count)
        for i in range(count):
            self.format.AddString('string_field_'+str(i))

        for i in range(count):
            if i < 50:
                self.format.Remove('string_field_'+str(i))
            else:
                self.format.Remove(i)
        self.assertEqual(len(self.format), 0)

    def test_other_format_methods(self):
        '''Автор: Краснов Д.В.'''
        self.format.AddBool('bool')
        self.format.AddString('string')
        self.format.AddInt64('int64')

        self.assertEqual(self.format.FieldName(0), 'bool')
        self.assertEqual(self.format.IndexByName('string'), 1)
        self.assertEqual(self.format.TypeOf(2), FieldType.ftINT64)
        self.assertEqual(self.format.TypeOf('bool'), FieldType.ftBOOLEAN)
        clone = self.format.Clone()
        self.assertEqual(len(self.format), len(clone))
