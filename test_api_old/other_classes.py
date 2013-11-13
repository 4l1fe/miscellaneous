import unittest
import os

os.environ['SBIS_PYTHON_UNITTEST'] = '1'
from sbis_root import *

'''Автор: Краснов Д.В.'''


class ObectIdTests(unittest.TestCase):

    def test_epmty_constructor(self):
        '''Автор: Краснов Д.В.'''
        self.objectid = ObjectId()
        self.assertIsNone(self.objectid.Key)
        self.assertEqual(self.objectid.Name, '')

        setattr(self.objectid, 'Key', 12)
        self.assertEqual(self.objectid.Key, 12)

        setattr(self.objectid, 'Name', 'what is up')
        self.assertEqual(self.objectid.Name, 'what is up')

    def test_filled_constructor_1(self):
        '''Автор: Краснов Д.В.'''
        self.objectid = ObjectId('kick it', 13)
        self.assertEqual(self.objectid.Key, 13)
        self.assertEqual(self.objectid.Name, 'kick it')

    def test_filled_constructor_2(self):
        '''Автор: Краснов Д.В.'''
        self.objectid = ObjectId(2)
        self.assertEqual(self.objectid.Key, 2)
        self.assertEqual(self.objectid.Name, '')

class HierarchyTests(unittest.TestCase):

    def test_empty_constructor(self):
        '''Автор: Краснов Д.В.'''
        self.hierarchy = Hierarchy()
        self.assertIsNone(self.hierarchy.Parent.Key)
        self.assertEqual(self.hierarchy.Parent.Name, '')
        self.assertIsNone(self.hierarchy.BranchBool)
        self.assertEqual(self.hierarchy.Branch, BranchType.LEAF)
        self.assertFalse(self.hierarchy.HasChild)

    def test_add_set_get_hierarchy(self):
        '''Автор: Краснов Д.В.'''
        self.hierarchy = Hierarchy()
        self.hierarchy.Parent.Key = 123
        self.assertEqual(self.hierarchy.Parent.Key, 123)

        self.hierarchy.Parent.Name = 'water'
        self.assertEqual(self.hierarchy.Parent.Name, 'water')

        self.hierarchy.Branch = BranchType.NODE
        self.assertTrue(self.hierarchy.BranchBool)

        self.hierarchy.BranchBool = False
        self.assertEqual(self.hierarchy.Branch, BranchType.HIDDEN)

        self.assertFalse(self.hierarchy.HasChild)
        self.hierarchy.HasChild = None
        self.assertIsNone(self.hierarchy.HasChild)

    def test_filled_constructor_1(self):
        '''Автор: Краснов Д.В.'''
        self.hierarchy = Hierarchy(1)
        self.assertEqual(self.hierarchy.Parent.Key, 1)
        self.assertEqual(self.hierarchy.Parent.Name, '')
        self.assertIsNone(self.hierarchy.BranchBool)
        self.assertEqual(self.hierarchy.Branch, BranchType.LEAF)
        self.assertFalse(self.hierarchy.HasChild)

    def test_filled_constructor_2(self):
        '''Автор: Краснов Д.В.'''
        self.hierarchy = Hierarchy(ObjectId('hier_2', 2))
        self.assertEqual(self.hierarchy.Parent.Key, 2)
        self.assertEqual(self.hierarchy.Parent.Name, 'hier_2')
        self.assertIsNone(self.hierarchy.BranchBool)
        self.assertEqual(self.hierarchy.Branch, BranchType.LEAF)
        self.assertFalse(self.hierarchy.HasChild)

    def test_filled_constructor_3(self):
        '''Автор: Краснов Д.В.'''
        self.hierarchy = Hierarchy(3, BranchType.HIDDEN)
        self.assertEqual(self.hierarchy.Parent.Key, 3)
        self.assertEqual(self.hierarchy.Parent.Name, '')
        self.assertFalse(self.hierarchy.BranchBool)
        self.assertEqual(self.hierarchy.Branch, BranchType.HIDDEN)
        self.assertFalse(self.hierarchy.HasChild)

    def test_filled_constructor_4(self):
        '''Автор: Краснов Д.В.'''
        self.hierarchy = Hierarchy(ObjectId('hier_4', 4), BranchType.NODE)
        self.assertEqual(self.hierarchy.Parent.Key, 4)
        self.assertEqual(self.hierarchy.Parent.Name, 'hier_4')
        self.assertTrue(self.hierarchy.BranchBool)
        self.assertEqual(self.hierarchy.Branch, BranchType.NODE)
        self.assertFalse(self.hierarchy.HasChild)

class RpcFileTests(unittest.TestCase):

    def test_rpcfile_methods(self):
        '''Автор: Краснов Д.В.'''
        with open('some', 'bw') as file:
            file.write(b'bytedata')
        self.rpcfile = CreateRpcFile('some')
        self.assertEqual(self.rpcfile.Data(), b'bytedata')

        self.rpcfile.SetContentType('text/html')
        self.assertEqual(self.rpcfile.ContentType(), 'text/html')

        self.rpcfile.SetData(b'newbytedata')
        self.assertEqual(self.rpcfile.Data(), b'newbytedata')

        self.rpcfile.SetName('new_some')
        self.assertEqual(self.rpcfile.Name(), 'new_some')

        self.rpcfile.SetContentDisposition('new_disposition')
        self.assertEqual(self.rpcfile.ContentDisposition(), 'new_disposition')

        self.rpcfile.SetId('1234fg-yt6')
        self.assertEqual(self.rpcfile.Id(), '1234fg-yt6')

class SqlQueryTests(unittest.TestCase):

    def test_add_get_recordset(self):
        '''Автор: Краснов Д.В.'''
        self.recordset = SqlQuery('SELECT * FROM "ОписаниеБазыДанных"')
        self.assertGreater(self.recordset.Size(), 0)
        self.assertFalse(self.recordset.IsNull(0, 0))
        self.assertFalse(self.recordset.Empty())

class SqlQueryScalarTests(unittest.TestCase):

    def test_add_get_scalar(self):
        '''Автор: Краснов Д.В.'''
        self.scalar = SqlQueryScalar('SELECT 1 FROM "ОписаниеБазыДанных"')
        self.assertIsInstance(self.scalar, int)
        self.assertEqual(int(self.scalar), 1)

class EnumInfoTests(unittest.TestCase):

    def test_add_get_enuminfo(self):
        '''Автор: Краснов Д.В.'''
        self.enuminfo = EnumInfo(3)
        self.assertEqual(int(self.enuminfo), 3)

class LinkInfoTests(unittest.TestCase):

    def test_add_get_linkinfo(self):
        '''Автор: Краснов Д.В.'''
        self.enuminfo = LinkInfo(1)
        self.assertEqual(int(self.enuminfo), 1)

class NamedIndicesTests(unittest.TestCase):

    def test_add_get_iter_namedindices(self):
        '''Автор: Краснов Д.В.'''
        d = {0: 'first_val', 1: 'second_val'}
        self.namedind = NamedIndices(d)
        self.assertEqual(self.namedind['first_val'], 0)
        self.assertEqual(self.namedind[1], 'second_val')
        self.assertEqual(self.namedind.as_dict, d)
        for i in self.namedind:
            self.assertIsNotNone(i)

class MoneyTests(unittest.TestCase):

    def test_add_set_get_money(self):
        '''Автор: Краснов Д.В.'''
        self.money = Money(3.77)
        self.assertEqual(float(self.money), 3.77)

        self.money.From(7.36)
        self.assertEqual(float(self.money), 7.36)

        self.money.FromString('6.98')
        self.assertEqual(float(self.money), 6.98)

class SortingListTests(unittest.TestCase):

#    @unittest.skip('не проходит проверку при ошибках в других тестах!или вовсе падает при при выходе за границу индексов')
    def test_add_set_get_iter_sortinglist(self):
        '''Автор: Краснов Д.В.'''
        self.sortinglist = SortingList()
        c1 = ColumnSortParameters()
        c1.fieldName = 'sort_column_1'
        c1.order = SortOrder.soASCENDING
        c1.nullPolicy = NullSortPolicy.nspNULLS_FIRST
        c2 = ColumnSortParameters()
        c2.fieldName = 'sort_column_2'
        c2.order = SortOrder.soDESCENDING
        c2.nullPolicy = NullSortPolicy.nspNULLS_LAST
        self.sortinglist.push_back(c1)
        self.sortinglist.push_back(c2)

        self.assertEqual(self.sortinglist.size(), 2)
        self.assertEqual(self.sortinglist[0].fieldName, 'sort_column_1')
        self.assertEqual(self.sortinglist[0].order, SortOrder.soASCENDING)
        self.assertEqual(self.sortinglist[0].nullPolicy, NullSortPolicy.nspNULLS_FIRST)

        self.assertEqual(self.sortinglist[1].fieldName, 'sort_column_2')
        self.assertEqual(self.sortinglist[1].order, SortOrder.soDESCENDING)
        self.assertEqual(self.sortinglist[1].nullPolicy, NullSortPolicy.nspNULLS_LAST)

        for column in self.sortinglist:
            self.assertIsInstance(column, ColumnSortParameters)

class NavigationTests(unittest.TestCase):

    def test_add_set_get_iter_navigation(self):
        '''Автор: Краснов Д.В.'''
        self.navigation = Navigation(10, 1, True)

        self.assertEqual(self.navigation.Page(), 1)
        self.assertEqual(self.navigation.RecsOnPage(), 10)
        self.assertTrue(self.navigation.IsNext())
        self.navigation.SetPage(2)
        self.assertEqual(self.navigation.Page(), 2)
        self.assertEqual(self.navigation['Страница'], 2)
        self.assertTrue(self.navigation['ЕстьЕще'])
        self.assertEqual(self.navigation['РазмерСтраницы'], 10)

class IContextTests(unittest.TestCase):

    def test_add_set_get_icontext(self):
        '''Автор: Краснов Д.В.'''
        self.icontext = CreateEmptyContext()

        self.icontext.Set(0, 'val1')
        self.icontext.Set('k', 'val2')
        self.assertEqual(self.icontext.Get(0), 'val1')
        self.assertEqual(self.icontext.Get('k'), 'val2')

        rec_ptr = CreateRecordPointer()
        rec_ptr.AddBool('bool_field', True)
        self.icontext.SetRecord(0, rec_ptr)
        self.icontext.SetRecord('r', rec_ptr)
        self.assertEqual(self.icontext.GetRecord(0)[0].Name(), 'bool_field')
        self.assertTrue(bool(self.icontext.GetRecord('r')))

class SessionTests(unittest.TestCase):

    def test_add_set_get_session(self):
        '''Автор: Краснов Д.В.'''
        self.session = Session
        self.session.Set(0, '0000a6ce-0000aff9-00ba-65646d650fdc45bf')
        self.assertEqual(self.session.Get(0), '0000a6ce-0000aff9-00ba-65646d650fdc45bf')
        self.assertEqual(self.session.ID(), '0000a6ce-0000aff9-00ba-65646d650fdc45bf')
        self.assertIsInstance(self.session.Context(), IContext)
        self.assertEqual(self.session.ClientID(), 42702)
        self.assertEqual(self.session.UserID(), 45049)
        self.assertEqual(self.session.ObjectName(), '')
        self.assertEqual(self.session.MethodName(), '')
        self.assertEqual(self.session.TaskMethodName(), '')

class ConfigTests(unittest.TestCase):

    def test_add_set_get_config(self):
        '''Автор: Краснов Д.В.'''
        self.config = Config
        self.assertIsInstance(self.config.Instance().Get('БазаДанных'), str)

class TransactionTests(unittest.TestCase):

    def test_add_set_get_transaction(self):
        '''Автор: Краснов Д.В.'''
        self.transaction = CreateTransaction(TransactionLevel.SERIALIZABLE, TransactionMode.WRITE)
        self.transaction.CreateSavePoint('point')
        self.transaction.ReleaseSavePoint('point')
        self.transaction.RollbackToSavePoint('point')
        self.transaction.Break()
        self.assertTrue(self.transaction.IsBreak())

class IStatementTests(unittest.TestCase):


    def test_add_set_get_istatement(self):
        '''Автор: Краснов Д.В.'''
        self.st = CreateStatement()
        cur = self.st.Exec('select 1')
        cur.get().Next()
        rec = cur.get().Data()
        self.assertEqual(int(rec[0]), 1)

class EnumsTests(unittest.TestCase):

    def test_transaction_level(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(TransactionLevel.READ_UNCOMMITTED), 0)
        self.assertEqual(int(TransactionLevel.READ_COMMITTED), 1)
        self.assertEqual(int(TransactionLevel.REPEATABLE_READ), 2)
        self.assertEqual(int(TransactionLevel.SERIALIZABLE), 3)

    def test_transaction_mode(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(TransactionMode.READ), 0)
        self.assertEqual(int(TransactionMode.WRITE), 1)

    def test_resource_type(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(ResourceType.rtDECLARATIVE_SELECT), 0)
        self.assertEqual(int(ResourceType.rtSTANDART_SELECT), 1)
        self.assertEqual(int(ResourceType.rtSELECT), 2)
        self.assertEqual(int(ResourceType.rtGENERATED_METHOD), 3)
        self.assertEqual(int(ResourceType.rtFILE_READ_METHOD), 4)
        self.assertEqual(int(ResourceType.rtFILE_READ_LIST_METHOD), 5)
        self.assertEqual(int(ResourceType.rtFILE_WRITE_METHOD), 6)
        self.assertEqual(int(ResourceType.rtFILE_WRITE_AND_ATTACH_METHOD), 7)
        self.assertEqual(int(ResourceType.rtTABLE), 8)
        self.assertEqual(int(ResourceType.rtTRIGGER_FUNCTION), 9)
        self.assertEqual(int(ResourceType.rtAREA_OF_SIGHT_FUNCTION), 10)
        self.assertEqual(int(ResourceType.rtAREA_OF_SIGHT), 11)
        self.assertEqual(int(ResourceType.rtUSER_ACTION), 12)
        self.assertEqual(int(ResourceType.rtROLE), 13)
        self.assertEqual(int(ResourceType.rtCONVERTER_EXTENSION), 14)
        self.assertEqual(int(ResourceType.rtPROXY), 16)
        self.assertEqual(int(ResourceType.rtHTTP_REQUEST), 17)

    def test_procedure_type(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(ProcedureType.ptSTORED_PROC), 0)
        self.assertEqual(int(ProcedureType.ptNATIVE), 1)
        self.assertEqual(int(ProcedureType.ptSTUB), 2)
        self.assertEqual(int(ProcedureType.ptSQL), 3)
        self.assertEqual(int(ProcedureType.ptAUTO_GENERATEDPROXY), 4)
        self.assertEqual(int(ProcedureType.ptPYTHON), 5)

    def test_module_type(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(ModuleType.NOT_SPECIFIED), 0)
        self.assertEqual(int(ModuleType.DATABASE_SPECIFIC), 1)
        self.assertEqual(int(ModuleType.ACCESS_SPECIFIC), 2)

    def test_proxy_method_type(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(ProxyMethodType.pmtSTANDART), 0)
        self.assertEqual(int(ProxyMethodType.pmtSELECT), 1)
        self.assertEqual(int(ProxyMethodType.pmtCREATE), 2)
        self.assertEqual(int(ProxyMethodType.pmtHISTORY), 3)
        self.assertEqual(int(ProxyMethodType.pmtCOPY), 4)
        self.assertEqual(int(ProxyMethodType.pmtMERGE), 5)
        self.assertEqual(int(ProxyMethodType.pmtREAD), 6)
        self.assertEqual(int(ProxyMethodType.pmtWRITE), 7)
        self.assertEqual(int(ProxyMethodType.pmtDROP), 8)

    def test_field_type(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(FieldType.ftUNDEFINED), 0)
        self.assertEqual(int(FieldType.ftBOOLEAN), 1)
        self.assertEqual(int(FieldType.ftDBIDENTIFIER), 2)
        self.assertEqual(int(FieldType.ftINT8), 3)
        self.assertEqual(int(FieldType.ftINT16), 4)
        self.assertEqual(int(FieldType.ftINT32), 5)
        self.assertEqual(int(FieldType.ftINT64), 6)
        self.assertEqual(int(FieldType.ftFLOAT), 7)
        self.assertEqual(int(FieldType.ftDOUBLE), 8)
        self.assertEqual(int(FieldType.ftMONEY), 9)
        self.assertEqual(int(FieldType.ftTEXT), 10)
        self.assertEqual(int(FieldType.ftSTRING), 11)
        self.assertEqual(int(FieldType.ftFLAGS), 12)
        self.assertEqual(int(FieldType.ftFLAGSMASK), 13)
        self.assertEqual(int(FieldType.ftENUM), 14)
        self.assertEqual(int(FieldType.ftDATE), 15)
        self.assertEqual(int(FieldType.ftTIME), 16)
        self.assertEqual(int(FieldType.ftDATETIME), 17)
        self.assertEqual(int(FieldType.ftBINARY), 18)
        self.assertEqual(int(FieldType.ftBLOB), 19)
        self.assertEqual(int(FieldType.ftRECORD), 20)
        self.assertEqual(int(FieldType.ftRECORDSET), 21)
        self.assertEqual(int(FieldType.ftLINK_HIER), 22)
        self.assertEqual(int(FieldType.ftLINK_N_to_1), 23)
        self.assertEqual(int(FieldType.ftLINK_1_to_N), 24)
        self.assertEqual(int(FieldType.ftLINK_COND_MASTER), 25)
        self.assertEqual(int(FieldType.ftLINK_COND_SLAVE), 26)
        self.assertEqual(int(FieldType.ftLINK_UNCOND_MASTER), 27)
        self.assertEqual(int(FieldType.ftLINK_UNCOND_SLAVE), 28)
        self.assertEqual(int(FieldType.ftLINK_1_TO_1_MASTER), 29)
        self.assertEqual(int(FieldType.ftLINK_1_TO_1_SLAVE), 30)
        self.assertEqual(int(FieldType.ftLINK_ON_DEMAND_SLAVE), 31)
        self.assertEqual(int(FieldType.ftLINK_ON_DEMAND_MASTER), 32)
        self.assertEqual(int(FieldType.ftFIELD_FROM_TABLE_REF), 33)
        self.assertEqual(int(FieldType.ftUUID), 34)
        self.assertEqual(int(FieldType.ftXML), 35)
        self.assertEqual(int(FieldType.ftARRAY_INT64), 36)
        self.assertEqual(int(FieldType.ftARRAY_TEXT), 37)
        self.assertEqual(int(FieldType.ftARRAY_INT16), 38)
        self.assertEqual(int(FieldType.ftARRAY_INT32), 39)
        self.assertEqual(int(FieldType.ftARRAY_BOOLEAN), 40)
        self.assertEqual(int(FieldType.ftARRAY_MONEY), 41)
        self.assertEqual(int(FieldType.ftARRAY_UUID), 42)
        self.assertEqual(int(FieldType.ftARRAY_DATE), 43)
        self.assertEqual(int(FieldType.ftARRAY_TIME), 44)
        self.assertEqual(int(FieldType.ftARRAY_DATETIME), 45)
        self.assertEqual(int(FieldType.ftARRAY_FLOAT), 46)
        self.assertEqual(int(FieldType.ftARRAY_DOUBLE), 47)
        self.assertEqual(int(FieldType.ftIDENTIFIER), 48)
        self.assertEqual(int(FieldType.ftLINK_BY_VALUE), 49)
        self.assertEqual(int(FieldType.ftLINK_BY_VALUE_MASTER), 50)
        self.assertEqual(int(FieldType.ftRPC_FILE), 51)
        self.assertEqual(int(FieldType.ftSORTING), 52)
        self.assertEqual(int(FieldType.ftNAVIGATION), 53)
        self.assertEqual(int(FieldType.ftEND), 56)

    def test_flag_value(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(FlagValue.NULL), 0)
        self.assertEqual(int(FlagValue.FALSE), 1)
        self.assertEqual(int(FlagValue.TRUE), 2)

    def test_hierarchy_branch(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(HierarchyBranch.hbsLEAF), 0)
        self.assertEqual(int(HierarchyBranch.hbsBRANCH), 1)
        self.assertEqual(int(HierarchyBranch.hbsHIDDEN_BRANCH), 2)

    def tet_tribool_value(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(TriboolValue.false_value), 0)
        self.assertEqual(int(TriboolValue.true_value), 1)
        self.assertEqual(int(TriboolValue.indeterminate_value), 2)

    def test_branch_type(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(BranchType.LEAF), 0)
        self.assertEqual(int(BranchType.NODE), 1)
        self.assertEqual(int(BranchType.HIDDEN), 2)

    def test_format_options(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(FormatOptions.foDEFAULT), 0)
        self.assertEqual(int(FormatOptions.foVALUE_ONLY), 1)
        self.assertEqual(int(FormatOptions.foANY_TO_WRITE), 2)
        self.assertEqual(int(FormatOptions.foIDENTIFIER), 4)
        self.assertEqual(int(FormatOptions.foDISCERN_LEAFS), 8)
        self.assertEqual(int(FormatOptions.foREAD_ONLY), 16)
        self.assertEqual(int(FormatOptions.foCREATE_UNDEFINED), 32)
        self.assertEqual(int(FormatOptions.foCURRENT_DATETIME), 64)
        self.assertEqual(int(FormatOptions.foLEAFS_ONLY), 128)
        self.assertEqual(int(FormatOptions.foGENERATED_UUID), 256)
        self.assertEqual(int(FormatOptions.foUNSAFE_TEXT), 512)

    def test_null_sort_policy(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(NullSortPolicy.nspNULLS_FIRST), 0)
        self.assertEqual(int(NullSortPolicy.nspNULLS_LAST), 1)

    def test_sort_order(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(SortOrder.soASCENDING), 0)
        self.assertEqual(int(SortOrder.soDESCENDING), 1)

    def test_navigation_result_type(self):
        '''Автор: Краснов Д.В.'''
        self.assertEqual(int(NavigationResultType.nrNONE), 0)
        self.assertEqual(int(NavigationResultType.nrIS_NEXT), 1)
        self.assertEqual(int(NavigationResultType.nrREC_COUNT), 2)
