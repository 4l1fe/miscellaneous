class Record:
    """ >>> rec = Record() # Объект rec будет использоваться во всех нижеописанных примерах."""

    def AddBool(self):
        """ >>> rec.AddBool('bool_field', False)
            <loader.IField object at 0x06A83570>
            >>> rec.bool_field
            False
            >>> bool(rec['bool_field'])
            False"""
        pass

    def AddDate(self):
        """ >>> import datetime
            >>> rec.AddDate('date_field', datetime.date.today())
            <loader.IField object at 0x06DA3FB8>
            >>> rec.date_field
            datetime.date(2013, 9, 30)
        """
        pass

    def AddDateTime(self):
        """ >>> import datetime
            >>> rec.AddDateTime('datetime_field', datetime.datetime.now())
            <loader.IField object at 0x06DA3F80>
            >>> rec.datetime_field
            datetime.datetime(2013, 9, 30, 14, 28, 4, 681000)
        """
        pass

    def AddDouble(self):
        """ >>> rec.AddDouble('double_field', 5.354)
            <loader.IField object at 0x06DA3FB8>
            >>> rec.double_field
            5.354
            >>> float(rec['double_field'])
            5.354"""
        pass

    def AddEnum(self):
        """ >>> d = {0: 'first_value', 1: 'second_value', 2: 'third_value'}
            >>> rec.AddEnum('enum_field', NamedIndicesFromDict(d))
            <loader.IField object at 0x07074570>
            >>> str(rec.enum_field)
            'None'"""
        pass

    def AddFlags(self):
        """ >>> d = {0: 'first_value', 1: 'second_value', 2: 'third_value'}
            >>> rec.AddFlags('flags_field', NamedIndicesFromDict(d))
            <loader.IField object at 0x07074618>
            >>> rec['flags_field'] = [True, False, None]
            >>> rec.flags_field
            [True, False, None]"""
        pass

    def AddFloat(self):
        """ >>> rec.AddFloat('float_field', 98.4)
            <loader.IField object at 0x07074688>
            >>> rec.float_field
            98.4000015258789
            >>> float(rec['float_field'])
            98.4000015258789"""
        pass

    def AddHierarchy(self):
        """ >>> hier = Hierarchy(ObjectId('name', 3), BranchType.NODE)
            >>> rec.AddHierarchy('hierarchy_field', hier)
            <loader.IField object at 0x07074768>
            >>> rec.hierarchy_field
            {Parent: {Key: 3, Name: "name"}, Type: NODE, Children: false}"""
        pass

    def AddInt16(self):
        """ >>> rec.AddInt16('int16_field', 5)
            <loader.IField object at 0x070746F8>
            >>> rec.int16_field
            5
            >>> int(rec['int16_field'])
            5"""
        pass

    def AddInt32(self):
        """ >>> rec.AddInt32('int32_field', 77)
            <loader.IField object at 0x06A83538>
            >>> rec.int32_field
            77
            >>> int(rec['int32_field'])
            77"""
        pass

    def AddInt64(self):
        """ >>> rec.AddInt64('int64_field', 8)
            <loader.IField object at 0x07074500>
            >>> rec.int64_field
            8
            >>> int(rec['int64_field'])
            8"""
        pass

    def AddInt8(self):
        """ >>> rec.AddInt8('int8_field', 4)
            <loader.IField object at 0x07074538>
            >>> rec.int8_field
            4
            >>> int(rec['int8_field'])
            4"""
        pass

    def AddLink(self):
        """ >>> rec.AddLink('link_field', 'some_table', LinkInfo(12))
            <loader.IField object at 0x06F51F10>
            >>> rec.link_field
            12
            >>> str(rec.link_field)
            '12'
            >>> str(rec['link_field'])
            '12'"""
        pass

    def AddMoney(self):
        """ >>> rec.AddMoney('money_field', Money('55.64'))
            <sbis.wrap.IField object at 0x033F6F48>
            >>> rec.money_field
            55.64
            >>> str(rec.money_field)
            '55.64'
            >>> str(rec['money_field'])
            '55.64'"""
        pass

    def AddNavigation(self):
        """ >>> rec.AddNavigation('navigation_field', Navigation(20, 1, True))
            <sbis.wrap.IField object at 0x0866C538>"""
        pass

    def AddRecord(self):
        """ >>> included_rec = CreateRecordPointer()
            >>> included_rec.AddBool('included_bool_field', True)
            <sbis.wrap.IField object at 0x07694880>
            >>> rec.AddRecord('included_record_field', included_rec.Format(), included_rec)
            <sbis.wrap.IField object at 0x07694810>
            >>> rec.included_record_field
            <sbis.wrap.Record object at 0x07694848>"""
        pass

    def AddRecordSet(self):
        """ >>> temp_format = CreateRecordFormat()
            >>> temp_format.AddString('rs_string_field')
            <sbis.wrap.IFldFormat object at 0x07704298>
            >>> temp_format.AddBool('rs_bool_field')
            <sbis.wrap.IFldFormat object at 0x07704228>
            >>> included_recordset = CreateRecordSet(temp_format)
            >>> for i in [0, 1]:
            ...     included_recordset.InsRow(i)
            ...     included_recordset[i].rs_string_field = 'armin van buren'
            ...     included_recordset[i].rs_bool_field = True
            ...
            True
            True
            >>> rec.AddRecordSet('included_recordset_field', included_recordset.get().Format(), included_recordset)
            <sbis.wrap.IField object at 0x07704420>"""
        pass

    def AddRpcFile(self):
        """ >>> rec.AddRpcFile('rpcfile_field', RpcFile())
            <sbis.wrap.IField object at 0x07704490>
            >>> rec.rpcfile_field
            <sbis.wrap.RpcFile object at 0x07704308>
            >>> rec['rpcfile_field']
            <sbis.wrap.IField object at 0x07704490>"""
        pass

    def AddSortingList(self):
        """ >>> sl = SortingList()
            >>> c = ColumnSortParameters()
            >>> c.fieldName = 'column1'
            >>> sl.push_back(c)
            >>> rec.AddSortingList('sortinglist_field', sl)
            <sbis.wrap.IField object at 0x07704340>
            >>> rec['sortinglist_field']
            <sbis.wrap.IField object at 0x077045E0>
        """
        pass

    def AddString(self):
        """ >>> rec.AddString('string_field', 'some_value')
            <loader.IField object at 0x06A83570>
            >>> rec.string_field
            'some_value'
            >>> str(rec['string_field'])
            'some_value'"""
        pass

    def AddTime(self):
        """ >>> time = datetime.datetime.now().time()
            >>> rec.AddTime('time_field', time)
            <sbis.wrap.IField object at 0x07694848>
            >>> rec.time_field
            datetime.time(16, 44, 53, 848390)"""
        pass

    def AddUuid(self):
        """ >>> rec.AddUuid('uuid_field', uuid.uuid4())
            <sbis.wrap.IField object at 0x07704308>
            >>> rec.uuid_field
            UUID('f785069f-ce34-4a9f-ba23-4174acec13d4')"""
        pass

    def AddArrayBool(self):
        """ >>> rec.AddArrayBool('array_bool_field')
            <sbis.wrap.IField object at 0x07704308>"""
        pass

    def AddArrayDate(self):
        """ >>> rec.AddArrayDate('array_date_field')
            <sbis.wrap.IField object at 0x07704420>"""
        pass

    def AddArrayDateTime(self):
        """ >>> rec.AddArrayDateTime('array_datetime_field')
            <sbis.wrap.IField object at 0x077045E0>"""
        pass

    def AddArrayDouble(self):
        """ >>> rec.AddArrayDouble('array_double_field')
            <sbis.wrap.IField object at 0x07704420>"""
        pass

    def AddArrayFloat(self):
        """ >>> rec.AddArrayFloat('array_float_field')
            <sbis.wrap.IField object at 0x07694848>"""
        pass

    def AddArrayInt16(self):
        """ >>> rec.AddArrayInt16('array_int16_field')
            <sbis.wrap.IField object at 0x077045E0>"""
        pass

    def AddArrayInt32(self):
        """ >>> rec.AddArrayInt32('array_int32_field')
            <sbis.wrap.IField object at 0x07694848>"""
        pass

    def AddArrayInt64(self):
        """ >>> rec.AddArrayInt64('array_int64_field')
            <sbis.wrap.IField object at 0x07704420>"""
        pass

    def AddArrayMoney(self):
        """ >>> rec.AddArrayMoney('array_money_field')
            <sbis.wrap.IField object at 0x03252F48>"""
        pass

    def AddArrayString(self):
        """ >>> rec.AddArrayString('array_string_field')
            <sbis.wrap.IField object at 0x04EFE500>"""
        pass

    def AddArrayTime(self):
        """ >>> rec.AddArrayTime('array_time_field')
            <sbis.wrap.IField object at 0x03252F48>"""
        pass

    def AddArrayUuid(self):
        """ >>> rec.AddArrayUuid('array_uuid_field')
            <sbis.wrap.IField object at 0x04EFE500>"""
        pass

    def AppendField(self):
        pass

    def CopyOwnFormat(self):
        pass

    def Count(self):
        """ >>> ec.Count()
            34"""
        pass

    def FieldName(self):
        """ >>> rec.FieldName(0)
            'bool_field'"""
        pass

    def Format(self):
        """ >>> frmt = rec.Format()
            >>> frmt
            <sbis.wrap.ConstIRecFormatSPtr object at 0x04F39230>"""
        pass

    def Get(self):
        """ >>> rec.Get('bool_field', None)
            False
            >>> rec.Get('invalid_field', 'default_value')
            'default_value'"""
        pass

    def Remove(self):
        """ >>> rec.Remove('bool_field')
            >>> rec.bool_field
            Traceback (most recent call last):
              File "<console>", line 1, in <module>
            AttributeError: 'NoneType' object has no attribute 'Record'"""
        pass

    def Reserve(self):
        """ >>> rec.Reserve(100)"""
        pass

    def TestField(self):
        """ >>> str(rec.TestField('invalid_field'))
            'None'
            >>> rec.TestField('array_string_field')
            <sbis.wrap.IField object at 0x04EFE500>"""
        pass

class IField:
    """Продолжение к примерам из класса Record"""

    def Format(self):
        """ >>> rec['string_field'].Format()
            <sbis.wrap.IFldFormat object at 0x074B4928>"""
        pass

    def From(self):
        pass

    def FromFalse(self):
        """ >>> rec['bool_field'].FromFalse()
            >>> rec.bool_field
            False"""
        pass

    def FromNull(self):
        """ >>> rec['bool_field'].FromNull()
            >>> rec.bool_field is None
            True"""
        pass

    def FromTrue(self):
        """ >>> rec['bool_field'].FromTrue()
            >>> rec.bool_field
            True"""
        pass

    def IsNull(self):
        """ >>> rec.AddInt16('null_int16_field')
            <sbis.wrap.IField object at 0x074B4928>
            >>> rec['null_int16_field'].IsNull()
            True"""
        pass

    def Name(self):
        """ >>> rec[0].Name()
            'bool_field'
            >>> for field in rec: print(field.Name())
            bool_field
            date_field
            datetime_field
            ..."""
        pass

    def RefFlags(self):
        """ >>> rec['flags_field'].RefFlags()
            <sbis.wrap.Flags object at 0x073758B8>
            >>> dir(rec['flags_field'].RefFlags())
            ['Flag', 'Set', 'SetFlag', '__class__', ...]"""
        pass

    def RefHierarchy(self):
        """ >>> rec['hierarchy_field'].RefHierarchy()
            {Parent: {Key: 3, Name: "name"}, Type: NODE, Children: false}
            >>> dir(rec['hierarchy_field'].RefHierarchy())
            ['Branch', 'BranchBool', 'HasChild', 'Parent', ...]"""
        pass

    def RefNavigation(self):
        """ >>> rec['navigation_field'].RefNavigation()
            <sbis.wrap.Navigation object at 0x07375960>
            >>> dir(rec['navigation_field'].RefNavigation())
            ['IsNext', 'IsNull', 'Page', 'RecsOnPage', 'SetPage', ...]"""
        pass

    def RefRecord(self):
        """ >>> rec['included_record_field'].RefRecord()
            <sbis.wrap.Record object at 0x07704298>
            >>> dir(rec['included_record_field'].RefRecord())
            ['AddArrayBool', 'AddArrayDate', 'AddArrayDateTime', 'AddArrayDouble', 'AddArrayFloat', 'AddArrayInt16',
            'AddArrayInt32', 'AddArrayInt64', 'AddArrayMoney', 'AddArrayString', 'AddArrayTime', 'AddArrayUuid',
            'AddBool', 'AddDate', 'AddDateTime', 'AddDouble', 'AddEnum', 'AddFlags', 'AddFloat', 'AddHierarchy',
            'AddInt16', 'AddInt32', 'AddInt64', 'AddInt8', 'AddLink', 'AddMoney', 'AddNavigation', 'AddRecord',
            'AddRecordSet', 'AddRpcFile', 'AddSortingList', 'AddString', 'AddTime', 'AddUuid', 'AppendField',
            'CopyOwnFormat', 'Count', 'FieldName', 'Format', 'Get', 'Remove', 'Reserve', 'TestField', ...]
            >>> rec['included_record_field'].RefRecord().included_bool_field
            True"""
        pass

    def RefRecordSPtr(self):
        pass

    def RefRecordSet(self):
        """ >>> rec['included_recordset_field'].RefRecordSet()[0].rs_string_field
            'armin van buren'
            >>> rec['included_recordset_field'].RefRecordSet()[1].rs_bool_field
            True
            >>> dir(rec['included_recordset_field'].RefRecordSet())
            ['AddColBinary', 'AddColBlobInfo', 'AddColBool', 'AddColDate', 'AddColDateTime', 'AddColDouble',
            'AddColFlags', 'AddColFlagsMask', 'AddColFloat', 'AddColHierarchy', 'AddColInt16', 'AddColInt32',
            'AddColInt64', 'AddColMoney', 'AddColObjectId', 'AddColRecord', 'AddColString', 'AddColTime',
            'AddColUuid', 'AddRow', 'Cursor', 'DelCol', 'DelRow', 'Empty', 'Format', 'GetBool', 'GetDouble',
            'GetFloat', 'GetInt16', 'GetInt32', 'GetInt64', 'GetInt8', 'GetRecord', 'GetRecordSet', 'GetString',
            'InsColBinary', 'InsColBlobInfo', 'InsColBool', 'InsColDate', 'InsColDateTime', 'InsColDouble',
            'InsColFlags', 'InsColFlagsMask', 'InsColFloat', 'InsColHierarchy', 'InsColInt16', 'InsColInt32',
            'InsColInt64', 'InsColMoney', 'InsColObjectId', 'InsColRecord', 'InsColString', 'InsColTime',
            'InsColUuid', 'InsRow', 'IsNull', 'Migrate', 'Size', 'SortRows', ...] """
        pass

    def RefRecordSetSPtr(self):
        pass

    def RefRpcFile(self):
        """ >>> rec['rpcfile_field'].RefRpcFile()
            <sbis.wrap.RpcFile object at 0x07442298>
            >>> dir(rec['rpcfile_field'].RefRpcFile())
            ['ContentDisposition', 'ContentType', 'Data', 'GetData', 'Id', 'Name', 'SetContentDisposition',
             'SetContentType', 'SetData', 'SetId', 'SetName', 'SetStream', 'Size', 'Stream', ...]"""
        pass

    def RefSortingList(self):
        """ >>> rec['sortinglist_field'].RefSortingList()
            <sbis.wrap.SortingList object at 0x07442A40>
            >>> dir(rec['sortinglist_field'].RefSortingList())
            [..., 'push_back', 'size']"""
        pass

    def RefString(self):
        """ >>> rec['string_field'].RefString()
            'some_value'"""
        pass

    def ToBytes(self):
        pass

    def ToDate(self):
        """ >>> rec['date_field'].ToDate()
            datetime.date(2013, 9, 30)"""
        pass

    def ToDateTime(self):
        """ >>> rec['datetime_field'].ToDateTime()
            datetime.datetime(2013, 9, 30, 14, 28, 4, 681000)"""
        pass

    def ToList(self):
        pass

    def ToTime(self):
        """ >>> rec['time_field'].ToTime()
            datetime.time(16, 44, 53, 848390)"""
        pass

    def Type(self):
        """ >>> rec['included_record_field'].Type()
            sbis.wrap.FieldType.ftRECORD
            >>> rec['time_field'].ToTime()
            datetime.time(16, 44, 53, 848390)
            >>> rec['string_field'].Type()
            sbis.wrap.FieldType.ftSTRING
            >>> rec['array_bool_field'].Type()
            sbis.wrap.FieldType.ftARRAY_BOOLEAN"""
        pass

class RecordSet:
    """ >>> rec_frmt = CreateRecordFormat()
        >>> rs = CreateRecordSet(rec_frmt)
        >>> rs.AddRow()
        True"""

    def AddColBinary(self):
        """ >>> rs.AddColBinary('binary_field')
            True
            >>> rs[0]['binary_field'].Type()
            sbis.wrap.FieldType.ftBINARY"""
        pass

    def AddColBlobInfo(self):
        """ >>> rs.AddColBlobInfo('blobinfo_field')
            True
            >>> rs[0]['blobinfo_field'].Type()
            sbis.wrap.FieldType.ftBLOB"""
        pass

    def AddColBool(self):
        """ >>> rs.AddColBool('bool_field')
            True
            >>> rs[0]['bool_field']
            <sbis.wrap.IField object at 0x07B7C260>"""
        pass

    def AddColDate(self):
        """ >>> rs.AddColDate('date_field')
            True
            >>> rs[0]['date_field']
            <sbis.wrap.IField object at 0x07B7C228>"""
        pass

    def AddColDateTime(self):
        """ >>> rs.AddColDateTime('datetime_field')
            True
            >>> rs[0]['datetime_field']
            <sbis.wrap.IField object at 0x07B7C308>"""
        pass

    def AddColDouble(self):
        """ >>> rs.AddColDouble('double_field')
            True
            >>> rs[0]['double_field']
            <sbis.wrap.IField object at 0x07B7C1F0>"""
        pass

    def AddColFlags(self):
        """ >>> rs.AddColFlags('flags_field')
            True
            >>> rs[0]['flags_field']
            <sbis.wrap.IField object at 0x07B7C340>"""
        pass

    def AddColFlagsMask(self):
        """ >>> rs.AddColFlagsMask('flagsmask_field')
            True
            >>> rs[0]['flagsmask_field']
            <sbis.wrap.IField object at 0x07B7C3B0>"""
        pass

    def AddColFloat(self):
        """ >>> rs.AddColFloat('float_field')
            True
            >>> rs[0]['float_field']
            <sbis.wrap.IField object at 0x07B7C490>"""
        pass

    def AddColHierarchy(self):
        """ >>> rs.AddColHierarchy('hierarchy_field')
            True
            >>> rs[0]['hierarchy_field']
            <sbis.wrap.IField object at 0x07B7C340>"""
        pass

    def AddColInt16(self):
        """ >>> rs.AddColInt16('int16_field')
            True
            >>> rs[0]['int16_field']
            <sbis.wrap.IField object at 0x07B7C500>"""
        pass

    def AddColInt32(self):
        """ >>> rs.AddColInt32('int32_field')
            True
            >>> rs[0]['int32_field']
            <sbis.wrap.IField object at 0x07B7C340> """
        pass

    def AddColInt64(self):
        """ >>> rs.AddColInt64('int64_field')
            True
            >>> rs[0]['int64_field']
            <sbis.wrap.IField object at 0x07B7C500> """
        pass

    def AddColMoney(self):
        """ >>> rs.AddColMoney('money_field')
            True
            >>> rs[0]['money_field']
            <sbis.wrap.IField object at 0x07B7C420> """
        pass

    def AddColObjectId(self):
        """ >>> rs.AddColObjectId('objectid_field')
            True
            >>> rs[0]['objectid_field']
            <sbis.wrap.IField object at 0x07B7C490>"""
        pass

    def AddColRecord(self):
        """ >>> rs.AddColRecord('record_field')
            True
            >>> rs[0]['record_field']
            <sbis.wrap.IField object at 0x07B7C490> """
        pass

    def AddColString(self):
        """ >>> rs.AddColString('string_field')
            True
            >>> rs[0]['string_field']
            <sbis.wrap.IField object at 0x07B7C490> """
        pass

    def AddColTime(self):
        """ >>> rs.AddColTime('time_field')
            True
            >>> rs[0]['time_field']
            <sbis.wrap.IField object at 0x07B7C340> """
        pass

    def AddColUuid(self):
        """ >>> rs.AddColUuid('uuid_field')
            True
            >>> rs[0]['uuid_field']
            <sbis.wrap.IField object at 0x07F24810> """
        pass

    def AddRow(self):
        """ >>> rec = Record()
            >>> rec.AddBool('rec_bool_field', True)
            <sbis.wrap.IField object at 0x07FA9260>
            >>> rs.AddRow(rec)
            True
            >>> rs[0].rec_bool_field
            Traceback (most recent call last):
              File "<console>", line 1, in <module>
            AttributeError: 'NoneType' object has no attribute 'Record'
            >>> rs[1].rec_bool_field
            True"""
        pass

    def Cursor(self):
        pass

    def DelCol(self):
        """ >>> rs.DelCol(0)
            True
            >>> rs[0][0].Name()
            'blobinfo_field'"""
        pass

    def DelRow(self):
        """>>> len(rs)
        2
        >>> rs.DelRow(1)
        True
        >>> len(rs)
        1"""
        pass

    def Empty(self):
        """ >>> rs.Empty()
            False"""
        pass

    def Format(self):
        """ >>> rs.Format()
            <sbis.wrap.ConstIRecFormatSPtr object at 0x07F21C70>"""
        pass

    def GetBool(self):
        """ >>> rs[0].bool_field = True
            >>> rs.GetBool(0, 1)
            True"""
        pass

    def GetDouble(self):
        """>>> rs[0].double_field = 7.21
        >>> rs.GetDouble(0, 4)
        7.21"""
        pass

    def GetFloat(self):
        """>>> rs[0].float_field = 3.764
        >>> rs.GetFloat(0, 7)
        3.7639999389648438"""
        pass

    def GetInt16(self):
        """>>> rs[0].int16_field = 16
        >>> rs.GetInt16(0, 9)
        16"""
        pass

    def GetInt32(self):
        """>>> rs[0].int32_field = 32
        >>> rs.GetInt32(0, 10)
        32"""
        pass

    def GetInt64(self):
        """>>> rs[0].int64_field = 64
        >>> rs.GetInt64(0, 11)
        64"""
        pass

    def GetInt8(self):
        pass

    def GetRecord(self):
        """>>> rs[0].record_field = CreateRecordPointer()
        >>> rs.GetRecord(0, 14)
        <sbis.wrap.Record object at 0x077F9298>"""
        pass

    def GetRecordSet(self):
        pass

    def GetString(self):
        """>>> rs[0].string_field = 'random'
        >>> rs.GetString(0, 15)
        'random'"""
        pass

    def InsColBinary(self):
        """>>> rs.InsColBinary(0, 'inserted_binary_field')
        True
        >>> rs[0][0].Name()
        'inserted_binary_field'"""
        pass

    def InsColBlobInfo(self):
        """>>> rs.InsColBlobInfo(0, 'inserted_blobinfo_field')
        True
        >>> rs[0][0].Name()
        'inserted_blobinfo_field'"""
        pass

    def InsColBool(self):
        """>>> rs.InsColBool(0, 'inserted_bool_field')
        True
        >>> rs[0][0].Name()
        'inserted_bool_field'"""
        pass

    def InsColDate(self):
        """>>> rs.InsColDate(0, 'inserted_date_field')
        True
        >>> rs[0][0].Name()
        'inserted_date_field'"""
        pass

    def InsColDateTime(self):
        """>>> rs.InsColDateTime(0, 'inserted_datetime_field')
        True
        >>> rs[0][0].Name()
        'inserted_datetime_field'"""
        pass

    def InsColDouble(self):
        """>>> rs.InsColDouble(0, 'inserted_double_field')
        True
        >>> rs[0][0].Name()
        'inserted_double_field'"""
        pass

    def InsColFlags(self):
        """>>> rs.InsColFlags(0, 'inserted_flags_field')
        True
        >>> rs[0][0].Name()
        'inserted_flags_field'"""
        pass

    def InsColFlagsMask(self):
        """>>> rs.InsColFlagsMask(0, 'inserted_flagsmask_field')
        True
        >>> rs[0][0].Name()
        'inserted_flagsmask_field'"""
        pass

    def InsColFloat(self):
        """>>> rs.InsColFloat(0, 'inserted_float_field')
        True
        >>> rs[0][0].Name()
        'inserted_float_field'"""
        pass

    def InsColHierarchy(self):
        """>>> rs.InsColHierarchy(0, 'inserted_hierarchy_field')
        True
        >>> rs[0][0].Name()
        'inserted_hierarchy_field'"""
        pass

    def InsColInt16(self):
        """>>> rs.InsColInt16(0, 'inserted_int16_field')
        True
        >>> rs[0][0].Name()
        'inserted_int16_field'"""
        pass

    def InsColInt32(self):
        """>>> rs.InsColInt32(0, 'inserted_int32_field')
        True
        >>> rs[0][0].Name()
        'inserted_int32_field'"""
        pass

    def InsColInt64(self):
        """>>> rs.InsColInt64(0, 'inserted_int64_field')
        True
        >>> rs[0][0].Name()
        'inserted_int64_field'"""
        pass

    def InsColMoney(self):
        """>>> rs.InsColMoney(0, 'inserted_money_field')
        True
        >>> rs[0][0].Name()
        'inserted_money_field'"""
        pass

    def InsColObjectId(self):
        """>>> rs.InsColObjectId(0, 'inserted_objectid_field')
        True
        >>> rs[0][0].Name()
        'inserted_objectid_field'"""
        pass

    def InsColRecord(self):
        """>>> rs.InsColRecord(0, 'inserted_record_field')
        True
        >>> rs[0][0].Name()
        'inserted_record_field'"""
        pass

    def InsColString(self):
        """>>> rs.InsColString(0, 'inserted_string_field')
        True
        >>> rs[0][0].Name()
        'inserted_string_field'"""
        pass

    def InsColTime(self):
        """>>> rs.InsColTime(0, 'inserted_time_field')
        True
        >>> rs[0][0].Name()
        'inserted_time_field'"""
        pass

    def InsColUuid(self):
        """>>> rs.InsColUuid(0, 'inserted_uuid_field')
        True
        >>> rs[0][0].Name()
        'inserted_uuid_field'"""
        pass

    def InsRow(self):
        """>>> rs.InsRow(0)
        True
        >>> len(rs)
        2"""
        pass

    def IsNull(self):
        """>>> rs.IsNull(0, 'bool_field')
        False
        >>> rs[0][20].Name()
        'bool_field'"""
        pass

    def Migrate(self):
        """>>> len(rs[0])
        37
        >>> new_frmt = CreateRecordFormat()
        new_frmt.AddString('string_field')
        new_frmt.AddBool('bool_field')
        new_frmt.AddInt8('int8_field')
        new_frmt.AddString('string2_field')
        new_frmt.AddBool('bool2_field')
        <sbis.wrap.IFldFormat object at 0x07997F80>
        <sbis.wrap.IFldFormat object at 0x07A9C260>
        <sbis.wrap.IFldFormat object at 0x07A9C2D0>
        <sbis.wrap.IFldFormat object at 0x07997FB8>
        <sbis.wrap.IFldFormat object at 0x07A9C298>
        >>> rs.Migrate(new_frmt)
        True
        >>> len(rs[0])
        5
        >>> for f in rs[0]:
        ...     print(f.Name())
        ...
        string_field
        bool_field
        int8_field
        string2_field
        bool2_field"""
        pass

    def Size(self):
        """>>> rs.Size()
        2"""
        pass

    def SortRows(self):
        pass

class IDatabase:
    """>>> idb = CreateDatabase("postgresql: host='localhost' port='5432' dbname='sbis3.0.trunk' user='postgres' password='postgres'")
        >>> idb
        <sbis.wrap.IDatabase object at 0x02DA6B90>"""

    def CreateStatement(self):
        """>>> stm = idb.CreateStatement()
            >>> stm
            <sbis.wrap.IStatement object at 0x074063E8>"""
        pass

    def CreateTransaction(self):
        """
        """
        pass

class IStatement:
    """>>> idb = CreateDatabase("postgresql: host='localhost' port='5432' dbname='sbis3.0.trunk' user='postgres' password='postgres'")
    >>> stm = idb.CreateStatement()"""

    def Exec(self):
        """>>> cur_ptr = stm.Exec('''select * from "Пользователь" ''')
            >>> cur = cur_ptr.get()
            >>> cur
            <sbis.wrap.ICursor object at 0x07406490>"""
        pass

    def SetParam(self):
        """>>> stm.SetParam(1, 5)
            >>> cur_ptr = stm.Exec('select * from "Пользователь" where "@Пользователь"=$1')
        """
        pass

class BLObject:
    """ >>> blobj = BLObject('РолиПользователя')"""

    def Copy(self):
        """ >>> copied_rec = blobj.Copy(1)
            >>> fname_value = [(f.Name(), str(f)) for f in copied_rec]
            >>> fname_value
            [('@РолиПользователей', '13'), ('Название', 'Пользователь'), ('Доступ', 'null'), ('Пользователь', '5'), ('ctid', '(0,13)')]"""
        pass

    def Create(self):
        """>>> new_rec = blobj.Create()
            >>> len(new_rec)
            4
            >>> fields = [f.Name() for f in new_rec]
            >>> fields
            ['@РолиПользователей', 'Название', 'Доступ', 'Пользователь']"""
        pass

    def Drop(self):
        """ >>> blobj.Drop(int(copied_rec['@РолиПользователей']))
            True
        """
        pass

    def Get(self):
        """ >>> rec = blobj.Get(1)
            >>> rec.Название
            'Пользователь'"""
        pass

    def Merge(self):
        pass

    def Name(self):
        """>>> blobj.Name()
            'РолиПользователя'
        """
        pass

    def RecInvoke(self):
        pass

    def Write(self):
        """>>> rec = Record(dict(Название="простенькое", Пользователь=777))
            >>> blobj.Write(rec)
            14"""
        pass

def SqlQuery():

    """>>> from sbis_root import *
        >>> rs = SqlQuery('''select * from "Пользователь" ''')
        >>> rs
        <sbis.wrap.RecordSetSPtr object at 0x049D8CF0>
        >>> len(rs)
        48
        >>> rs = SqlQuery('''select * from "Пользователь" where "Логин"=$1 ''', 'admin')
        >>> rs[0].Логин
        'admin'
        >>> rec = Record()
        >>> rec.AddInt64('1', 3)
        <sbis.wrap.IField object at 0x07FEEC70>
        >>> rs = SqlQuery('''select * from "Пользователь" where "@Пользователь"=$1 ''', rec)
        >>> rs[0].Имя
        'Вася'
        >>> len(rs[0])
        15
        >>> fmt = CreateRecordFormat()
        >>> fmt.AddString('Логин')
        >>> rs = SqlQuery('''select * from "Пользователь" where "@Пользователь"=$1 ''', rec, fmt)
        >>> len(rs[0])
        1
        >>> rs[0][0].Name()
        'Логин'
    """
    pass

#def empty_doc():
#    from itertools import chain
#    import sys
#    classes = [cls.__dict__.items() for cls_name, cls in sys.modules[__name__].__dict__.items() if 'class' in repr(cls)]
#    for k,v in chain(*classes):
#        if not v.__doc__:
#            print(k, v.__doc__, sep='===')
#
#empty_doc()
