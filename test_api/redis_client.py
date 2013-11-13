import unittest, sys, os
import sbis_root

@unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < "3.6.0", "Тест предназначен для версии платформы выше 3.6.0 включительно.")
class RedisClientTest(unittest.TestCase):

    def setUp(self):
        self.host = 'localhost'
        self.port = 6379
        self.dbindex = 0
        self.redis_client = sbis_root.RedisClient( "host='" + self.host + "', port=" + str(self.port) + ", dbindex=" + str(self.dbindex), False, False )
        #print( 'Connect to ' + self.host + ':' + str(self.port) )

    # def tearDown(self):
    #     self.redis_client = None
    #     print( 'Disonnect from ' + self.host + ':' + str(self.port) )

    def test_set_value(self):
        """Автор: Шувалова Т.Н."""
        set_value = self.redis_client.SetValue
        test_args = [
            ( "key", "1" ),
            ( "key", "[1,2,3]" ),
            ( "key:subkey", "1" ),
            ( "key:subkey:subsubkey", "1" ),
            ( "", "")
        ]
        for _tuple in test_args:
            key, value = _tuple
            self.assertTrue(set_value(key, value), "Can't set to key '" + key + "' value '" + value + "' given.")

    def test_set_value_ex(self):
        """Автор: Шувалова Т.Н."""
        set_value_ex = self.redis_client.SetValueEx
        test_args_good = [
            ( "key1", 1, "1" ),
            ( "key2", 999, "[1,2,3]" ),
            ( "", 999, "" )
        ]
        test_args_bad_false = [
            ( "key", 0, "[1,2,3]" )
        ]
        test_args_bad_raise = [
            ( Exception, "key1", -1, "1" ),
            ( Exception, "key2", 999999999999999999999, "[1,2,3]" ),
            ( Exception, "key3", 'not int', "[1,2,3]" ),
            ( Exception, "key4", 1, None ),
            ( Exception, 1, 999, "[1,2,3]" ),
            ( Exception, 'key5', 999, [1,2,3] )
        ]
        for _tuple in test_args_good:
            field, timer, value = _tuple
            self.assertTrue(set_value_ex(field, timer, value), "Can't set to key '" + value + "' value '" + value + "' for " + str(timer) + " seconds given.")
        for _tuple in test_args_bad_false:
            field, timer, value = _tuple
            self.assertFalse(set_value_ex(field, timer, value), "Error: was assigned '" + field + "' value '" + value + "' for " + str(timer) + " seconds given.")
        for _tuple in test_args_bad_raise:
            exception, field, timer, value = _tuple
            if not value:
                self.assertRaises(exception, set_value_ex, (field, timer))
            else:
                self.assertRaises(exception, set_value_ex, (field, timer, value))

    def test_ping(self):
        """Автор: Шувалова Т.Н."""
        ping = self.redis_client.Ping
        self.assertTrue(ping, "Can not ping localhost.")

    def test_set_value_if_not_exists(self):
        """Автор: Шувалова Т.Н."""
        set_value = self.redis_client.SetValue
        set_value_if_not_exists = self.redis_client.SetValueIfNotExists
        del_value = self.redis_client.DelValue
        test_args_good = [
            ( "qqq", "1" ),
            ( "www", "[1,2,3]" ),
            ( "eee", "abcdef" ),
            ( "rrr", "[1,2,3]zdfgdf{}{}zdfzdf///" )
        ]
        for _tuple in test_args_good:
            key, value = _tuple
            self.assertTrue(set_value(key, value), "init_Can't set to key '" + key + "' value '" + value + "' given.")
        for tuple_ in test_args_good:
            key, value = tuple_
            self.assertTrue(self.redis_client.DelValue(key), "Can't delete key '" + key )
        for tuple_ in test_args_good:
            key, value = tuple_
            self.assertTrue(set_value_if_not_exists(key, value), "test_Can't set to key '" + key + "' value '" + value + "' given.")
        for tuple_ in test_args_good:
          key, value = tuple_
          self.assertFalse(set_value_if_not_exists(key, value), "Was set to key '" + key + "' value '" + value + "' given but must not.")

    def test_set_values(self):
        """Автор: Шувалова Т.Н."""
        set_values = self.redis_client.SetValues
        test_args_good = [
            {"key1": "1", "key2": "[1,2,3]","key3": "abcdef","key4": "[1,2,3]zdfgdf{}{}zdfzdf///"},
            {"key1": "1", "key1": "[1,2,3]","key1": "abcdef","key1": "[1,2,3]zdfgdf{}{}zdfzdf///"},
            {}
            ]
        test_args_bad = []
        for tuple_ in test_args_good:
            self.assertTrue(set_values(tuple_), "Can't insert values: '" + str(tuple_) + "'")
        for tuple_ in test_args_bad:
            self.assertFalse(set_values(tuple_), "Bad value inserted: " + str(tuple_))
        for tuple_ in test_args_good:
            self.assertTrue(set_values(tuple_), "Can't repeat inserting values: '" + str(tuple_) + "'")

    def test_values(self):
        """Автор: Шувалова Т.Н."""
        values = self.redis_client.Values
        set_values = self.redis_client.SetValues
        test_args_set = [
            {"key1": "1", "key2": "[1,2,3]","key3": "abcdef","key4": "[1,2,3]zdfgdf{}{}zdfzdf///"},
            {"key5": "1", "key5": "[1,2,3]","key5": "abcdef","key5": "[1,2,3]zdfgdf{}{}zdfzdf///"}]
        test_args = [
            [{"key1": "", "key2": "","key3": "","key4": ""},{"key1": "1", "key2": "[1,2,3]","key3": "abcdef","key4": "[1,2,3]zdfgdf{}{}zdfzdf///"}],
            [{"key5": ""}, {"key5": "[1,2,3]zdfgdf{}{}zdfzdf///"}],
            [{"key99999": "1234567890"}, {"key99999": "1234567890"}]]
        for tuple_ in test_args_set:
            self.assertTrue(set_values(tuple_), "Can't insert values: '" + str(tuple_) + "'")
        for tuple_ in test_args:
            values(tuple_[0])
            self.assertDictEqual(tuple_[0], tuple_[1], "Values: '" + str(tuple_) + "' returned are wrong.")

    def test_del_value(self):
        """Автор: Шувалова Т.Н."""
        set_value = self.redis_client.SetValue
        del_value = self.redis_client.DelValue
        is_exists = self.redis_client.IsExists
        key, value = ("qqq", "val")
        set_value(key, value)
        self.assertTrue(is_exists(key), "Key '" + key + "' does not exist but must be.")
        self.assertTrue(del_value(key), "Can't delete key '" + key + "'.")
        self.assertFalse(is_exists(key), "Key '" + key + "' exists but must not.")
        self.assertFalse(del_value(key), "Deleted key '" + key + "' but it doesn't exist.")

    def test_set_expire(self):
        """Автор: Шувалова Т.Н."""
        set_expire = self.redis_client.SetExpire
        test_args_good = [
            ( "qqq", 1 ),
            ( "www", 2 ),
            ( "eee", 3 ),
            ( "rrr", 4 )
        ]
        test_args_neg_time = [
            ( "qqq", 10 ),
            ( "qqq", 0 ),
            ( "qqq", 3 )
        ]
        for tuple_ in test_args_good:
            key, value = tuple_
            self.redis_client.DelValue(key)
        for _tuple in test_args_good:
            key, value = _tuple
            self.assertFalse(set_expire(key, value), "Set expiration time to key '" + key + "' but key doesn't exist.")
            self.redis_client.SetValue(key, str(value))
        for tuple_ in test_args_good:
            key, value = tuple_
            self.assertTrue(set_expire(key, value), "Can't set to key '" + key + "' expiration '" + str(value)+ "' given.")

        #If timeout is 0 is deleted immediately
        self.redis_client.SetValue("qqq", "val")
        self.assertTrue(self.redis_client.IsExists("qqq"), "Key 'qqq' does not exist but must be.")
        key, value = test_args_neg_time[0]
        self.assertTrue(set_expire(key, value), "Can't set to key '" + key + "' expiration '" + str(value)+ "' given.")
        key, value = test_args_neg_time[1]
        self.assertTrue(set_expire(key, value), "Can't set to key '" + key + "' expiration '" + str(value)+ "' given.")
        key, value = test_args_neg_time[2]
        self.assertFalse(set_expire(key, value), "Set expiration time to key '" + key + "' but key doesn't exist.")
        self.assertFalse(self.redis_client.IsExists(key), "Key '" + key + "' but must be deleted.")

        #Timeout value overflow
        self.redis_client.SetValue("qqq", "val")
        self.assertRaises(Exception, set_expire, ("qqq", -1))
        self.assertRaises(Exception, set_expire, ("qqq", 999999999999999999999999999999999999999))

        #Reset timeout
        self.redis_client.SetValue("qqq", "val")
        key, value = ("qqq", 1)
        self.assertTrue(set_expire(key, value), "Can't set to key '" + key + "' expiration '" + str(value)+ "' given.")
        self.assertTrue(self.redis_client.SetValue(key, str(value)), "Can't set to key '" + key + "' expiration '" + str(value)+ "' given.")

    def test_r_push_list_value(self):
        """Автор: Шувалова Т.Н."""
        r_push_list_value = self.redis_client.RPushListValue
        test_args_good = [
            ( "list1", "1" ),
            ( "list1", "1" ),
            ( "list1", "2" ),
            ( "list1", "3" ),
            ( "list2", "[1,2,3]" ),
            ( "list1", "1" ),
            ( "list1", "1" ),
            ( "list1", "2" ),
            ( "list1", "3" ),
            ( "list3", "1" ),
            ( "list4", "sDASDASDSD1" ),
            ( "list4", "2ADFASDFASDF" ),
            ( "list4", "3hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh\\\=-0987654322" )
        ]
        test_args_bad = [
            ("", ""),
            ("", "123")
        ]
        for tuple_ in test_args_good:
            key, value = tuple_
            self.assertTrue(r_push_list_value(key, value), "Can't set to key '" + key + "' value '" + value + "' given.")
        for tuple_ in test_args_bad:
            key, value = tuple_
            self.assertFalse(r_push_list_value(key, value), "Bad value '" + key + "' is inserted with value " + value)
        for tuple_ in test_args_good:
            key, value = tuple_
            self.assertTrue(r_push_list_value(key, value), "Can't repeat inserting value '" + key + "' with value " + value)

    def test_keys(self):
        """Автор: Шувалова Т.Н."""
        set_value = self.redis_client.SetValue
        set_values = self.redis_client.SetValues
        keys = self.redis_client.Keys
        test_args = [ ( "abc", "1" ),
                      ( "_abc", "1" ),
                      ( "_abc_", "1" ),
                      ( "abc_", "1" ),
                      ( "aabc", "1" ),
                      ( "aaabc", "1" ),
                      ( "abccc", "1" ),
                      ( "bca", "1" ),
                      ( "a", "1" ),
                      ( "b", "1" ),
                      ( "c", "1" ),
                      ( "very_very_very_very_long_key_that_anybody_can_not_repeat_or_insert_key_like_this_nice_guy", "1" )]
        masks_res_approx = [ ( "abc", 1),
                      ( "?abc", 2),
                      ( "*abc", 4 ),
                      ( "abc?", 1),
                      ( "abc*", 3 ),
                      ( "?abc?", 1),
                      ( "*abc*", 7 ),
                      ( "*a*", 9),
                      ( "b", 1 ),
                      ( "c", 1),
                      ( "*", 11),
                      ( "?", 3 )]
        masks_res_border = [( "this_fool_key_can't_exist_it_doesn't have_sense_just_to_test_empty_result!", 0 ),
                             ( "very_very_very_very_long_key_that_anybody_can_not_repeat_or_insert_key_like_this_nice_guy", 1 ),
                            ( "very_very_very_very_long_key_that_anybody_can_not_repeat_or_insert_key_like_this_nice_guy*", 1 ),
                            ( "*very_very_very_very_long_key_that_anybody_can_not_repeat_or_insert_key_like_this_nice_guy", 1 ),
                            ( "?very_very_very_very_long_key_that_anybody_can_not_repeat_or_insert_key_like_this_nice_guy", 0 )]
        for params in test_args:
            key, value = params
            self.assertTrue(set_value(key, value), "Can't set to key '" + key + "' value '" + value + "' given.")
        self.assertTrue(set_values(dict(test_args)), "Can't set keys '" + str(dict(test_args)))
        for params in masks_res_approx:
            mask, equals_to = params
            self.assertTrue(len(keys(mask)) >= equals_to, "Keys list with mask '" + mask + "' must contain at least " + str(equals_to) + " elements, but it does not.")
        for params in masks_res_border:
            mask, equals_to = params
            self.assertEquals(len(keys(mask)), equals_to, "Keys list with mask '" + mask + "' must contain " + str(equals_to) + " elements, but it does not.")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RedisClientTest)
    #suite = unittest.TestLoader().loadTestsFromTestCase(RCTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # rc = sbis_root.RedisClient( "host='" + 'localhost' + "', port=" + '6379' + ", dbindex=" + '0', False )
    # print(str(rc.Ping())+'*******************************')
