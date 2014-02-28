xml = """<?xml version="1.0" encoding="WINDOWS-1251"?>
<repository orx_version="1.71">

  <object name="Облака">
    <select access_mode="0" is_service="0" last_changed="lobastovis" name="Облака.Список" responsible="lobastovis" returns="TABLE" type="SQL">
      <return name="ИдентификаторОблака">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Облака</table>
          <column>ИдентификаторОблака</column>
        </format>
      </return>
      <return name="Сайт">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Облака</table>
          <column>Сайт</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT cl."ИдентификаторОблака", cl."Сайт" FROM "Облака" as cl;</body>
      </definition>
    </select>
  </object>

  <object insert_on_create="0" name="ОповещенияПользователей" read_only="0">
    <source name="ИнформационноеСообщение"/>
    <generate_method name="ОповещенияПользователей.Clone"/>
    <generate_method name="ОповещенияПользователей.Create"/>
    <generate_method name="ОповещенияПользователей.History"/>
    <generate_method name="ОповещенияПользователей.Merge"/>
    <generate_method name="ОповещенияПользователей.Read"/>
    <generate_method name="ОповещенияПользователей.Remove"/>
    <generate_method name="ОповещенияПользователей.Write"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.ДобавитьМгновенноеСообщение" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="user">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <parameter name="msg">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>INSERT INTO "ДжабберСообщения" ("Пользователь", "Сообщение") VALUES (:user, :msg)</body>
      </definition>
    </select>
    <select access_mode="0" is_proxy="0" is_service="0" name="ОповещенияПользователей.ДобавитьУведомление" returns="SCALAR" type="NATIVE">
      <parameter name="ИнфСообщение">
        <format>
          <type>RECREFERENCE</type>
          <free>1</free>
        </format>
      </parameter>
      <return name="___SBIS_SCALAR_RETURN___">
        <format>
          <type>BOOLEAN</type>
        </format>
      </return>
    </select>
    <generate_method name="ОповещенияПользователей.Записать"/>
    <generate_method name="ОповещенияПользователей.История"/>
    <generate_method name="ОповещенияПользователей.Копировать"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.НайтиЗаявкуПользователя" responsible="lobastovis" returns="TABLE" type="SQL">
      <parameter name="ИнфСообщение">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <return name="Примечание">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>Примечание</column>
        </format>
      </return>
      <return name="Тип">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>Тип</column>
        </format>
      </return>
      <return name="Действие">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>Действие</column>
        </format>
      </return>
      <return name="КаналОтправки">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>КаналОтправки</column>
        </format>
      </return>
      <return name="ОтправительНазвание">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>ОтправительНазвание</column>
        </format>
      </return>
      <return name="ТипДокумента">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>ТипДокумента</column>
        </format>
      </return>
      <return name="КолвоПопыток">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>КолвоПопыток</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT inf."Примечание", inf."Тип", inf."Действие", inf."КаналОтправки", inf."ОтправительНазвание", inf."ТипДокумента", inf."КолвоПопыток"
   FROM "ИнформационноеСообщение" inf
   WHERE inf."@ИнформационноеСообщение" = :ИнфСообщение;</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.НайтиЗаявкуПользователя" responsible="lobastovis" returns="TABLE" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <parameter name="ИдКлиента">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <parameter name="ИдЧастноеЛицо">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <parameter name="КаналОтправки">
        <format>
          <type>INTEGER</type>
        </format>
      </parameter>
      <return name="ИД">
        <format>
          <type>INT64</type>
          <pk>1</pk>
        </format>
      </return>
      <return name="КолвоПопыток">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>КолвоПопыток</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT inf."@ИнформационноеСообщение", inf."КолвоПопыток"
   FROM "ИнформационноеСообщение" AS inf
   WHERE ((inf."Пользователь" = :Пользователь OR (inf."ИдКлиента" = :ИдКлиента AND inf."ИдЧастноеЛицо" = :ИдЧастноеЛицо)) AND inf."КаналОтправки" = :КаналОтправки)
   LIMIT 1;</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" name="ОповещенияПользователей.ОбновитьСписок" returns="NONE" type="SQL">
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ИнформационноеСообщение" SET "Конец" = null WHERE ("Конец" is NOT NULL AND "Начало" &lt; now())</body>
      </definition>
    </select>
    <generate_method name="ОповещенияПользователей.Объединить"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.ОтложитьНачало" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="Пк">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ИнформационноеСообщение"
   SET "Начало" = now() + '1 minute'
   WHERE "@ИнформационноеСообщение" = :Пк</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.ПолучитьНастройкиПользователя" responsible="lobastovis" returns="TABLE" type="SQL">
      <parameter name="Польз">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <parameter name="Ид1">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <parameter name="Ид2">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <return name="@ПрофильКомпании">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>@ПрофильКомпании</column>
        </format>
      </return>
      <return name="email">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>email</column>
        </format>
      </return>
      <return name="Телефон">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>Телефон</column>
        </format>
      </return>
      <return name="ИнтервалУведомленийEmail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ИнтервалУведомленийEmail</column>
        </format>
      </return>
      <return name="ИнтервалУведомленийSms">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ИнтервалУведомленийSms</column>
        </format>
      </return>
      <return name="СЧаса">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>СЧаса</column>
        </format>
      </return>
      <return name="ПоЧас">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ПоЧас</column>
        </format>
      </return>
      <return name="ЧасовойПояс">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ЧасовойПояс</column>
        </format>
      </return>
      <return name="ПоследнееУведомлениеEmail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ПоследнееУведомлениеEmail</column>
        </format>
      </return>
      <return name="ПоследнееУведомлениеSms">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ПоследнееУведомлениеSms</column>
        </format>
      </return>
      <return name="Название">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>Название</column>
        </format>
      </return>
      <return name="Jabber">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>Jabber</column>
        </format>
      </return>
      <return name="ТелефонПодтвержден">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ТелефонПодтвержден</column>
        </format>
      </return>
      <return name="ПоследняяАктивность">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ПоследняяАктивность</column>
        </format>
      </return>
      <return name="Пользователь">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>Пользователь</column>
        </format>
      </return>
      <return name="ИдКлиента">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ИдКлиента</column>
        </format>
      </return>
      <return name="ИдЧастноеЛицо">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>ИдЧастноеЛицо</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT pk."@ПрофильКомпании", pk."email", pk."Телефон", pk."ИнтервалУведомленийEmail", pk."ИнтервалУведомленийSms", pk."СЧаса",
       pk."ПоЧас", pk."ЧасовойПояс", pk."ПоследнееУведомлениеEmail", pk."ПоследнееУведомлениеSms", pk."Название", pk."Jabber",
       pk."ТелефонПодтвержден", pk."ПоследняяАктивность", pk."Пользователь", pk."ИдКлиента", pk."ИдЧастноеЛицо"
FROM "ПрофильКомпании" as pk
WHERE ( pk."Пользователь" = :Польз OR ( pk."ИдКлиента" = :Ид1 AND pk."ИдЧастноеЛицо" = :Ид2))
LIMIT 1</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.ПослатьМгновенныеСообщения" responsible="Лобастов И.С." returns="NONE" type="PYTHON">
      <definition>
        <language>PYTHON</language>
        <body>from logging import handlers
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import logging
from time import gmtime, strftime
import time
import queue

handler = logging.handlers.TimedRotatingFileHandler("logs\\jabber_log",when="midnight")
handler.suffix = '_%Y%m%d.log'
frm = logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
handler.setFormatter(frm)
logger = logging.getLogger('send_messages')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#Проинициализируем все необходимые переменные
TRY_TO_CONNECT_TIMES = 300

server = ConfigGet( "НастройкиДжабберСервера.Сервер" )
port = int(ConfigGet( "НастройкиДжабберСервера.Порт" ))
jid = ConfigGet( "НастройкиДжабберСервера.Логин" )
password = ConfigGet( "НастройкиДжабберСервера.Пароль" )

class JabberClient( ClientXMPP ):
   __msg_queue = None
   __to_del = None

   def __init__( self, jid, password ):
      logger.info( u'Инициализируем экземпляр класса "JabberClient"' )
      super().__init__( jid, password )
      self.add_event_handler("session_start", self.start, threaded=True)
      self.add_event_handler("disconnected", self.disconnected)
      self.register_plugin('xep_0030') # Service Discovery
      self.register_plugin('xep_0199') # XMPP Ping
      #self.reconnect = False

   def start( self, event ):
      logger.info( u'Начало вызова медота start' )
      self.__msg_queue = queue.Queue()
      self.send_presence()
      try:
         self.get_roster(timeout=1)
      except IqError as err:
         logger.error(u'Ошибка при вызове метода get_roster')
         logger.error(err.iq['error']['condition'])
         self.disconnect()
      except IqTimeout:
         logger.error(u'Сервер слишком долго не отвечает')
         self.disconnect()

      while True:
         try:
            mes = self.__msg_queue.get(block=False, timeout=0.05)
            logger.info( u'Непосредственно вызов send_message' )
            self.send_message( mto=mes[0], mbody=mes[1], mtype='chat' )
            logger.info( u'После вызова send_message' )
         except queue.Empty:
            #Очередь опустела - надо взять порцию новых данных
            if self.__to_del is not None and len(self.__to_del) &gt; 0:
               #Надо удалить обработанные записи
               sql = '''DELETE FROM	"ДжабберСообщения" WHERE "@ДжабберСообщения" = ANY(ARRAY[{to_del}])'''.format(to_del=self.__to_del)
               SqlQuery(sql)
               self.__to_del = None
            logger.info( u'Очередь на отправку сообщений пуста: возьмем порцию новых данных' )
            sql = '''SELECT
                     	"@ДжабберСообщения" id
                     , "Пользователь" user_id
                     , "Сообщение" msg
                     FROM
                     	"ДжабберСообщения" '''
            msg_list_ptr = SqlQuery(sql)
            if msg_list_ptr is not None and not msg_list_ptr.get().Empty():
               self.__to_del = ''
               msg_list_rs = msg_list_ptr.get()
               for rec in msg_list_rs:
                  self.__to_del += str(rec["id"]) + ','
                  item = [str(rec["user_id"]), str(rec["msg"])]
                  self.__msg_queue.put(item)
               self.__to_del = self.__to_del[:-1]
            time.sleep(1)
            continue
         except Exception as e:
            err_text = 'Необработанная ошибка: ' + str(e)
            logger.error( err_text )
            time.sleep(1)
      logger.info( u'Вышли из цикла отправки сообщений!' )
      self.disconnect(wait=True)

   def disconnected( self, event ):
      logger.info( u'Попали в событие отключения' )
      self.__msg_queue = None
      self.__msg_queue = queue.Queue()
      self.__to_del = None

if server is not None and port is not None and jid is not None and password is not None:
   client = JabberClient( jid, password )
   logger.info( u'Готовимся подключиться к серверу (поток отправки сообщений)' )
   for counter in range( TRY_TO_CONNECT_TIMES  ):
      if client.connect(address=(server,port), reattempt=False):
         client.process(block=True)
         break
      else:
         war = 'Попытка подключения №{counter} не удалась'.format(counter=counter+1)
         logger.warning( war )
         time.sleep(3)
else:
   logger.error(u'Ошибка при вызове метода "ПослатьМгновенныеСообщения": в конфигурации отсутствуют обязательные настройки')
return</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="lobastovis" name="ОповещенияПользователей.ПроставитьДатуВремяПоследнейПосылки" responsible="lobastovis" returns="NONE" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <parameter name="ТипОтправки">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>DO $$
DECLARE
   sent_type text := :ТипОтправки;
   usr text := :Пользователь;
   sql text :='';
BEGIN
   sql = 'UPDATE "ПрофильКомпании"
            SET "ПоследнееУведомление' || sent_type || '" = now()
            WHERE "Пользователь" = ''' || usr || '''';
   EXECUTE sql;
END $$</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.ПроставитьНачало" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="Пк">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <parameter name="Начало">
        <format>
          <type>DATETIME</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ИнформационноеСообщение"
   SET "Начало" = :Начало
   WHERE "@ИнформационноеСообщение" = :Пк</body>
      </definition>
    </select>
    <generate_method name="ОповещенияПользователей.Прочитать"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.СброситьКолвоПопытокИПеревестиНачало" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="Пк">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ИнформационноеСообщение"
   SET "Начало" = now(), "КолвоПопыток" = 0
   WHERE "@ИнформационноеСообщение" = :Пк</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="lobastovis" name="ОповещенияПользователей.СброситьСчетчик" responsible="lobastovis" returns="NONE" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <parameter name="Тип">
        <format>
          <type>INTEGER</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ИнформационноеСообщение"
SET    "Количество" = 0
WHERE  "Раздел"     =
       ( SELECT "@ИнформационноеСообщение"
       FROM    "ИнформационноеСообщение"
       WHERE   "Пользователь" = :Пользователь
       AND     "Раздел" IS NULL
       )
AND    "Jabber" = true
AND    "Тип"    = :Тип;</body>
      </definition>
    </select>
    <generate_method name="ОповещенияПользователей.Создать"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.Список" responsible="Лобастов И.С." returns="TABLE" type="STORED">
      <return name="Пользователь">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>Пользователь</column>
        </format>
      </return>
      <return name="@ИнформационноеСообщение">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>@ИнформационноеСообщение</column>
        </format>
      </return>
      <return name="КаналОтправки">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ИнформационноеСообщение</table>
          <column>КаналОтправки</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>BEGIN
  -- В ЭТОЙ ХРАНИМКЕ ИСПОЛЬЗУЮТСЯ advisory lock'и!!!
  SET enable_seqscan = 'off';
  SET enable_bitmapscan = 'off';
  RETURN QUERY(
    SELECT inf."Пользователь", inf."@ИнформационноеСообщение", inf."КаналОтправки"
    FROM "ИнформационноеСообщение" inf
    WHERE
      inf."Конец" is NULL AND
      pg_try_advisory_lock( tableoid::INTEGER, inf."@ИнформационноеСообщение"::INTEGER )
    ORDER BY
      "Начало"
    LIMIT 10
  );
  RESET enable_seqscan;
  RESET enable_bitmapscan;
END;</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.УвеличитьСчетчикОтправки" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="Пк">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ИнформационноеСообщение"
   SET "Начало" = now() + '1 week', "КолвоПопыток" = "КолвоПопыток" + 1
   WHERE "@ИнформационноеСообщение" = :Пк</body>
      </definition>
    </select>
    <generate_method name="ОповещенияПользователей.Удалить"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ОповещенияПользователей.УдалитьЗаявку" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="ИнфСообщение">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>DELETE FROM "ИнформационноеСообщение" inf WHERE inf."@ИнформационноеСообщение" = :ИнфСообщение;</body>
      </definition>
    </select>
  </object>

  <object insert_on_create="0" name="ПрофильКомпании" read_only="0">
    <source name="ПрофильКомпании"/>
    <generate_method name="ПрофильКомпании.Clone"/>
    <generate_method name="ПрофильКомпании.Create"/>
    <generate_method name="ПрофильКомпании.History"/>
    <generate_method name="ПрофильКомпании.Merge"/>
    <generate_method name="ПрофильКомпании.Read"/>
    <generate_method name="ПрофильКомпании.Remove"/>
    <generate_method name="ПрофильКомпании.Write"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.Деактивировать" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ПрофильКомпании" SET "ИнтервалУведомленийEmail" = 0, "ИнтервалУведомленийSms" = 0, "Jabber" = false WHERE "Пользователь" = :Пользователь;</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ДобавитьИПодключитьДжаббер" responsible="lobastovis" returns="SCALAR" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <return name="___SBIS_SCALAR_RETURN___">
        <format>
          <type>BOOLEAN</type>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>DO $$
DECLARE
   pos integer;
   usr_pos integer;
   usr text := :Пользователь;
BEGIN
   IF ( usr &lt;&gt; '' ) THEN
      INSERT INTO "ПодключитьДжаббер" ("Пользователь") VALUES (usr);
      SELECT "@ПрофильКомпании" INTO usr_pos FROM "ПрофильКомпании" WHERE "Пользователь" = usr LIMIT 1;
      IF ( usr_pos is NULL ) THEN
         INSERT INTO "ПрофильКомпании" ("Пользователь", "Jabber") VALUES (usr, true);
      ELSE
         UPDATE "ПрофильКомпании" SET "Jabber" = true WHERE "Пользователь" = usr;
      END IF;
      PERFORM set_config('sbis3.jabber_res', 'true', true);
   ELSE
      PERFORM set_config('sbis3.jabber_res', 'false', true);
   END IF;
END $$;
SELECT current_setting('sbis3.jabber_res')::boolean;</body>
      </definition>
    </select>
    <select access_mode="0" is_proxy="0" is_service="0" name="ПрофильКомпании.ДобавитьНастройкиПользователя" returns="SCALAR" type="NATIVE">
      <parameter name="Настройки">
        <format>
          <type>RECREFERENCE</type>
          <free>1</free>
        </format>
      </parameter>
      <return name="___SBIS_SCALAR_RETURN___">
        <format>
          <type>BOOLEAN</type>
        </format>
      </return>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ДобавитьПустыеНастройкиПользователя" responsible="lobastovis" returns="SCALAR" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <parameter name="ИдКлиента">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <parameter name="ИдЧастноеЛицо">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <return name="___SBIS_SCALAR_RETURN___">
        <format>
          <type>BOOLEAN</type>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>DO $$
DECLARE
   pos integer;
   usr_pos integer;
   usr text := :Пользователь;
   client integer := :ИдКлиента;
   face integer := :ИдЧастноеЛицо;
BEGIN
   IF ( usr &lt;&gt; '' ) THEN
      SELECT "@ПрофильКомпании" INTO usr_pos FROM "ПрофильКомпании" WHERE ("Пользователь" = usr) LIMIT 1;
      IF ( usr_pos is NULL ) THEN
         IF ( client &lt; 0 OR face &lt; 0 ) THEN
            INSERT INTO "ПрофильКомпании" ("Пользователь") VALUES (usr) RETURNING "@ПрофильКомпании" into pos;
         ELSE
            INSERT INTO "ПрофильКомпании" ("Пользователь", "ИдКлиента", "ИдЧастноеЛицо") VALUES (usr, client, face) RETURNING "@ПрофильКомпании" into pos;
         END IF;
         IF (pos IS NOT NULL) THEN
            PERFORM set_config('sbis3.addprofile_res', 'true', true);
         ELSE
            PERFORM set_config('sbis3.addprofile_res', 'false', true);
         END IF;
      ELSE
         PERFORM set_config('sbis3.addprofile_res', 'false', true);
      END IF;
   ELSE
      PERFORM set_config('sbis3.addprofile_res', 'false', true);
   END IF;
END $$;
SELECT current_setting('sbis3.addprofile_res')::boolean;</body>
      </definition>
    </select>
    <generate_method name="ПрофильКомпании.Записать"/>
    <generate_method name="ПрофильКомпании.История"/>
    <generate_method name="ПрофильКомпании.Копировать"/>
    <select access_mode="0" is_service="0" last_changed="lobastovis" name="ПрофильКомпании.НайтиПользоваетляПоИд" responsible="lobastovis" returns="TABLE" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <return name="@ПрофильКомпании">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ПрофильКомпании</table>
          <column>@ПрофильКомпании</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT pk."@ПрофильКомпании" FROM "ПрофильКомпании" as pk WHERE pk."Пользователь" = :Пользователь LIMIT 1</body>
      </definition>
    </select>
    <generate_method name="ПрофильКомпании.Объединить"/>
    <select access_mode="0" is_proxy="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ПереподключитьДжаббер" responsible="Лобастов И.С." returns="SCALAR" type="NATIVE">
      <parameter name="Пользователи">
        <format>
          <type>TEXT[]</type>
        </format>
      </parameter>
      <return name="___SBIS_SCALAR_RETURN___">
        <format>
          <type>BOOLEAN</type>
        </format>
      </return>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ПереподключитьДжабберВсем" responsible="Лобастов И.С." returns="NONE" type="PYTHON">
      <definition>
        <language>PYTHON</language>
        <body>MAX_SIZE = 5000
sql = '''SELECT
         	"Пользователь" id
         FROM
         	"ПрофильКомпании"
         WHERE
         	"Jabber" '''
user_list_ptr = SqlQuery(sql)
if user_list_ptr is not None and not user_list_ptr.get().Empty():
   user_list_rs = user_list_ptr.get()
   ul = []
   for rec in user_list_rs:
      ul.append(str(rec["id"]))
   #Теперь будем брать партиями по MAX_SIZE записей и переподключать
   num_of_repeat = divmod(len(ul),MAX_SIZE)
   for k in range (num_of_repeat[0]):
      tmp_ul = []
      for i in range (k*MAX_SIZE, (k+1)*MAX_SIZE):
         tmp_ul.append(ul[i])
      ПрофильКомпании.ПереподключитьДжаббер(tmp_ul)
   tmp_ul = []
   for i in range (num_of_repeat[0]*MAX_SIZE, num_of_repeat[0]*MAX_SIZE+num_of_repeat[1]):
      tmp_ul.append(ul[i])
   ПрофильКомпании.ПереподключитьДжаббер(tmp_ul)
return</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.Подключить" responsible="lobastovis" returns="SCALAR" type="PYTHON">
      <parameter name="Параметры">
        <format>
          <type>RECREFERENCE</type>
          <free>1</free>
        </format>
      </parameter>
      <return name="___SBIS_SCALAR_RETURN___">
        <format>
          <type>BOOLEAN</type>
        </format>
      </return>
      <definition>
        <language>PYTHON</language>
        <body>import logging
import sleekxmpp
import time
import hashlib
from sleekxmpp.exceptions import IqError, IqTimeout
class AutoRegister:
   __client = None
   __TRY_TO_CONNECT_TIMES = 3
   class JabberClient(sleekxmpp.ClientXMPP):
      def __init__(self, jid, password):
         super().__init__( jid, password )
         self.add_event_handler("session_start", self.start, threaded=True)
         self.add_event_handler("register", self.register, threaded=True)

      def start( self, event ):
         self.send_presence()
         self.get_roster()
         self.disconnect(wait=True)

      def register(self, iq):
         resp = self.Iq()
         for log in self.login:
            m = hashlib.md5()
            m.update(log.encode('utf-8'))
            reg_pass = m.hexdigest()
            reg_pass = reg_pass[0:12]
            resp['type'] = 'set'
            resp['register']['username'] = log
            resp['register']['password'] = reg_pass

            try:
               resp.send(now=True)
               logging.info("Новый пользователь успешно зарегистрирован, логин: %s!" % log)
            except IqError as e:
               logging.error("Не удалось зарегистрировать пользователя: %s" % e.iq['error']['text'])
            except IqTimeout:
               logging.error("Jabber сервер не отвечает")
         self.disconnect(wait=True)

   @staticmethod
   def reg( jid, password, server, port, login ):
      if AutoRegister.__client is None:
         AutoRegister.__client = AutoRegister.JabberClient( jid, password )
         AutoRegister.__client.register_plugin('xep_0077') # In-band Registration
         AutoRegister.__client.register_plugin('xep_0030') # Service Discovery
         AutoRegister.__client.register_plugin('xep_0199') # XMPP Ping
      AutoRegister.__client['xep_0077'].force_registration = True
      AutoRegister.__client.login = login
      connected = False
      for counter in range( AutoRegister.__TRY_TO_CONNECT_TIMES  ):
         if AutoRegister.__client.connect(address=(server,port), reattempt=False):
             connected = True
             break
         else:
             time.sleep(0.5)
      if connected:
         AutoRegister.__client.process(block=True)
      else:
         raise Error( 'Не удалось подключиться к Jabber серверу', 'Проверьте запущен ли сервер' )
      return True
return AutoRegister.reg(str(Параметры["admin"]), str(Параметры["pass"]), str(Параметры["server"]), int(Параметры["port"]), Параметры["reg_login"].ToList())</body>
      </definition>
    </select>
    <select access_mode="0" is_proxy="0" is_service="0" last_changed="lobastovis" name="ПрофильКомпании.ПодключитьДжаббер" responsible="lobastovis" returns="SCALAR" type="NATIVE">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <return name="___SBIS_SCALAR_RETURN___">
        <format>
          <type>BOOLEAN</type>
        </format>
      </return>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ПотокРегистрации" responsible="Лобастов И.С." returns="NONE" type="PYTHON">
      <definition>
        <language>PYTHON</language>
        <body>from logging import handlers
import logging
import sleekxmpp
import time
import hashlib
import queue
from sleekxmpp.exceptions import IqError, IqTimeout
from time import gmtime, strftime

handler = logging.handlers.TimedRotatingFileHandler("logs\\jabber_reg_log",when="midnight")
handler.suffix = '_%Y%m%d.log'
frm = logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
handler.setFormatter(frm)
logger = logging.getLogger('registration')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#Проинициализируем все необходимые переменные
TRY_TO_CONNECT_TIMES = 300

server = ConfigGet( "НастройкиДжабберСервера.Сервер" )
port = int(ConfigGet( "НастройкиДжабберСервера.Порт" ))
jid = ConfigGet( "НастройкиДжабберСервера.Логин" )
password = ConfigGet( "НастройкиДжабберСервера.Пароль" )

class RegJabberClient(sleekxmpp.ClientXMPP):
   __reg_queue = None
   __to_del = None

   def __init__(self, jid, password):
      super().__init__( jid, password )
      self.add_event_handler("session_start", self.start, threaded=True)
      self.add_event_handler("register", self.register, threaded=True)
      self.add_event_handler("disconnected", self.disconnected)
      self.register_plugin('xep_0077') # In-band Registration
      self.register_plugin('xep_0030') # Service Discovery
      self.register_plugin('xep_0199') # XMPP Ping
      self['xep_0077'].force_registration = True

   def start( self, event ):
      logger.info( u'Начало вызова медота start' )
      self.send_presence()
      try:
         self.get_roster(timeout=1)
      except IqError as err:
         logger.error(u'Ошибка при вызове метода get_roster')
         logger.error(err.iq['error']['condition'])
         self.disconnect()
      except IqTimeout:
         logger.error(u'Сервер слишком долго не отвечает')
         self.disconnect()
      self.disconnect(wait=True)

   def register(self, iq):
      resp = self.Iq()
      self.__reg_queue = queue.Queue()
      while True:
         try:
            log = self.__reg_queue.get(block=False, timeout=0.05)
            m = hashlib.md5()
            m.update(log.encode('utf-8'))
            reg_pass = m.hexdigest()
            reg_pass = reg_pass[0:12]
            resp['type'] = 'set'
            resp['register']['username'] = log
            resp['register']['password'] = reg_pass
            try:
               resp.send(now=True)
               logger.info("Новый пользователь успешно зарегистрирован, логин: %s!" % log)
            except IqError as e:
               logger.error("Не удалось зарегистрировать пользователя: %s" % e.iq['error']['text'])
            except IqTimeout:
               logger.error("Jabber сервер не отвечает")
         except queue.Empty:
            #Очередь опустела - надо взять порцию новых данных
            if self.__to_del is not None and len(self.__to_del) &gt; 0:
               #Надо удалить обработанные записи
               sql = '''DELETE FROM	"ПодключитьДжаббер" WHERE "@ПодключитьДжаббер" = ANY(ARRAY[{to_del}])'''.format(to_del=self.__to_del)
               SqlQuery(sql)
               self.__to_del = None
            logger.info( u'Очередь на регистрацию пуста: возьмем порцию новых данных' )
            sql = '''SELECT
                     	"@ПодключитьДжаббер" id
                     , "Пользователь" user_id
                     FROM
                     	"ПодключитьДжаббер" '''
            reg_list_ptr = SqlQuery(sql)
            if reg_list_ptr is not None and not reg_list_ptr.get().Empty():
               self.__to_del = ''
               reg_list_rs = reg_list_ptr.get()
               for rec in reg_list_rs:
                  self.__to_del += str(rec["id"]) + ','
                  self.__reg_queue.put(str(rec["user_id"]))
               self.__to_del = self.__to_del[:-1]
            time.sleep(1)
            continue
         except Exception as e:
            err_text = 'Необработанная ошибка: ' + str(e)
            logger.error( err_text )
            time.sleep(1)
      logger.info( u'Вышли из цикла регистрации!' )
      self.disconnect(wait=True)

   def disconnected( self, event ):
      logger.info( u'Попали в событие отключения' )
      self.__reg_queue = None
      self.__reg_queue = queue.Queue()
      self.__to_del = None

if server is not None and port is not None and jid is not None and password is not None:
   client = RegJabberClient( jid, password )
   logger.info( u'Готовимся подключиться к серверу (поток регистрации)' )
   for counter in range( TRY_TO_CONNECT_TIMES  ):
      if client.connect(address=(server,port), reattempt=False):
         client.process(block=True)
         break
      else:
         war = 'Попытка подключения №{counter} не удалась'.format(counter=counter+1)
         logger.warning( war )
         time.sleep(3)
else:
   logger.error(u'Ошибка при вызове метода "ПотокРегистрации": в конфигурации отсутствуют обязательные настройки')
return</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ПрописатьИдентификатор" responsible="Лобастов И.С." returns="NONE" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <parameter name="ИдКлиента">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <parameter name="ИдЧастноеЛицо">
        <format>
          <type>INT64</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ПрофильКомпании"
   SET "ИдКлиента" = :ИдКлиента, "ИдЧастноеЛицо" = :ИдЧастноеЛицо
   WHERE "Пользователь" = :Пользователь;</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ПроставитьАктивность" responsible="Лобастов И.С." returns="NONE" type="PYTHON">
      <parameter name="СписокПользователей">
        <format>
          <type>RECORDSET</type>
        </format>
      </parameter>
      <definition>
        <language>PYTHON</language>
        <body>i = 0
while i &lt; СписокПользователей.Size():
   user = int(СписокПользователей[i]["Пользователь"])
   if user &gt; 0:
      if not СписокПользователей[i]["ПоследнийВход"].IsNull():
         dt = СписокПользователей[i]["ПоследнийВход"].ToDateTime()
         sql = '''UPDATE "ПрофильКомпании"
                  SET "ПоследняяАктивность" = '{dt}'
                  WHERE "ИдПользователь" = {user}
               '''.format(dt=dt, user=user)
         SqlQuery(sql)
   i += 1
return</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ПрофильКомпании.ПроставитьПопыткуОтправки" responsible="lobastovis" returns="NONE" type="SQL">
      <parameter name="Пользователь">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>UPDATE "ПрофильКомпании" SET "ПопыткаПоследнейОтправки" = now() WHERE "Пользователь" = :Пользователь;</body>
      </definition>
    </select>
    <generate_method name="ПрофильКомпании.Прочитать"/>
    <generate_method name="ПрофильКомпании.Создать"/>
    <generate_method name="ПрофильКомпании.Удалить"/>
  </object>

  <object insert_on_create="0" name="Статистика" read_only="0">
    <source name="Статистика"/>
    <generate_method name="Статистика.Clone"/>
    <generate_method name="Статистика.Create"/>
    <generate_method name="Статистика.History"/>
    <generate_method name="Статистика.Merge"/>
    <generate_method name="Статистика.Read"/>
    <generate_method name="Статистика.Remove"/>
    <generate_method name="Статистика.Write"/>
    <select access_mode="0" is_service="0" last_changed="lobastovis" name="Статистика.Вся" responsible="lobastovis" returns="TABLE" type="STORED">
      <parameter name="Дней">
        <format>
          <type>INTEGER</type>
        </format>
      </parameter>
      <return name="Дата">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>Дата</column>
        </format>
      </return>
      <return name="EmailSuccess">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>EmailSuccess</column>
        </format>
      </return>
      <return name="EmailFail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>EmailFail</column>
        </format>
      </return>
      <return name="SmsSuccess">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>SmsSuccess</column>
        </format>
      </return>
      <return name="SmsFail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>SmsFail</column>
        </format>
      </return>
      <return name="JabberSuccess">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>JabberSuccess</column>
        </format>
      </return>
      <return name="JabberFail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>JabberFail</column>
        </format>
      </return>
      <return name="ВсегоКлиентов">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>ВсегоКлиентов</column>
        </format>
      </return>
      <return name="Активные">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>Активные</column>
        </format>
      </return>
      <return name="Неактивные">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>Неактивные</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>DECLARE
   vsego integer;
   kol integer := $1;
   sql text := '';
BEGIN
   SELECT count(*) FROM "Статистика" INTO vsego;
   IF kol IS NOT NULL AND kol &lt; vsego AND kol &gt; 0 THEN
      sql = 'SELECT st."Дата", st."EmailSuccess", st."EmailFail", st."SmsSuccess", st."SmsFail", st."JabberSuccess", st."JabberFail", st."ВсегоКлиентов", st."Активные", st."Неактивные" FROM "Статистика" st ORDER BY st."Дата" LIMIT ' || kol || ' OFFSET ' || (vsego-kol) || ';';
   ELSE
      sql = 'SELECT st."Дата", st."EmailSuccess", st."EmailFail", st."SmsSuccess", st."SmsFail", st."JabberSuccess", st."JabberFail", st."ВсегоКлиентов", st."Активные", st."Неактивные" FROM "Статистика" st ORDER BY st."Дата";';
   END IF;
   RETURN QUERY EXECUTE sql;
END;</body>
      </definition>
    </select>
    <generate_method name="Статистика.Записать"/>
    <generate_method name="Статистика.История"/>
    <generate_method name="Статистика.Копировать"/>
    <select access_mode="0" is_service="0" name="Статистика.ОбновитьПоле" returns="NONE" type="SQL">
      <parameter name="Поле">
        <format>
          <type>TEXT</type>
        </format>
      </parameter>
      <definition>
        <language>PLPGSQL</language>
        <body>DO $$
DECLARE
	pos integer;
	field text := :Поле;
	sql text :='';
BEGIN
	SELECT "Статистика"."@Статистика" INTO pos FROM "Статистика" WHERE ("Статистика"."Дата" = current_date);
	IF (pos IS NOT NULL) THEN
		sql = 'UPDATE "Статистика" SET "' || field || '" = "' || field || '"+1 WHERE "@Статистика" = ' || pos || ';';
	ELSE
		sql = 'INSERT INTO "Статистика" ("' || field || '") VALUES (1);';
	END IF;
	EXECUTE sql;
END $$;</body>
      </definition>
    </select>
    <generate_method name="Статистика.Объединить"/>
    <select access_mode="0" is_service="0" name="Статистика.ПересчитатьСтатистику" returns="NONE" type="SQL">
      <definition>
        <language>PLPGSQL</language>
        <body>DO $$
DECLARE
	all_c integer;
	active integer;
	passive integer;
	pos integer;
	dt timestamp;
BEGIN
	SELECT "Статистика"."@Статистика", "Статистика"."ПоследнееОбновление" INTO pos, dt FROM "Статистика" WHERE ("Статистика"."Дата" = current_date);
	IF ((pos IS NULL) OR (dt &lt; now() - INTERVAL '30 minutes')) THEN
		SELECT count(*) INTO all_c FROM "ПрофильКомпании";
		SELECT count(*) INTO active FROM "ПрофильКомпании" WHERE ( "ПоследнееУведомлениеEmail" IS NOT NULL AND date("ПоследнееУведомлениеEmail") = CURRENT_DATE);
		SELECT count(*) INTO passive FROM "ПрофильКомпании" WHERE (("ПопыткаПоследнейОтправки" IS NOT NULL AND date("ПопыткаПоследнейОтправки") = CURRENT_DATE)
			AND (CASE WHEN (date("ПоследнееУведомлениеEmail") IS NOT NULL) THEN (date("ПоследнееУведомлениеEmail") &lt;&gt; CURRENT_DATE) ELSE TRUE END));
		IF (pos IS NOT NULL) THEN
			UPDATE "Статистика" SET "ВсегоКлиентов" = all_c, "Активные" = active, "Неактивные" = passive, "ПоследнееОбновление" = now() WHERE "@Статистика" = pos;
		ELSE
			INSERT INTO "Статистика" ("ВсегоКлиентов", "Активные", "Неактивные") VALUES (all_c, active, passive);
		END IF;
	END IF;
END $$;</body>
      </definition>
    </select>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="Статистика.ПолучитьЗаДату" responsible="lobastovis" returns="TABLE" type="SQL">
      <parameter name="ДатаВход">
        <format>
          <type>DATE</type>
        </format>
      </parameter>
      <return name="Дата">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>Дата</column>
        </format>
      </return>
      <return name="EmailSuccess">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>EmailSuccess</column>
        </format>
      </return>
      <return name="EmailFail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>EmailFail</column>
        </format>
      </return>
      <return name="SmsSuccess">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>SmsSuccess</column>
        </format>
      </return>
      <return name="SmsFail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>SmsFail</column>
        </format>
      </return>
      <return name="JabberSuccess">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>JabberSuccess</column>
        </format>
      </return>
      <return name="JabberFail">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>JabberFail</column>
        </format>
      </return>
      <return name="ВсегоКлиентов">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>ВсегоКлиентов</column>
        </format>
      </return>
      <return name="Активные">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>Активные</column>
        </format>
      </return>
      <return name="Неактивные">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>Неактивные</column>
        </format>
      </return>
      <return name="ПоследнееОбновление">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>Статистика</table>
          <column>ПоследнееОбновление</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT
   "Дата"
,  "EmailSuccess"
,  "EmailFail"
,  "SmsSuccess"
,  "SmsFail"
,  "JabberSuccess"
,  "JabberFail"
,  "ВсегоКлиентов"
,  "Активные"
,  "Неактивные"
,  "ПоследнееОбновление"
FROM
   "Статистика"
WHERE
   "Дата" = :ДатаВход
LIMIT 1;</body>
      </definition>
    </select>
    <generate_method name="Статистика.Прочитать"/>
    <generate_method name="Статистика.Создать"/>
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="Статистика.ТекущееСостояние" responsible="Лобастов И.С." returns="RECORD" type="SQL">
      <return name="КлиентовВОчереди">
        <format>
          <type>INTEGER</type>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT count(*) FROM "ИнформационноеСообщение" inf WHERE inf."Начало" &lt; now();</body>
      </definition>
    </select>
    <generate_method name="Статистика.Удалить"/>
  </object>

  <object name="ШаблоныПисем">
    <select access_mode="0" is_service="0" last_changed="Лобастов И.С." name="ШаблоныПисем.Список" responsible="lobastovis" returns="TABLE" type="SQL">
      <return name="Шаблон">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ШаблоныПисем</table>
          <column>Шаблон</column>
        </format>
      </return>
      <return name="ТипОтправки">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ШаблоныПисем</table>
          <column>ТипОтправки</column>
        </format>
      </return>
      <return name="ТипОтвета">
        <format>
          <type>FIELDFROMTABLE</type>
          <table>ШаблоныПисем</table>
          <column>ТипОтвета</column>
        </format>
      </return>
      <definition>
        <language>PLPGSQL</language>
        <body>SELECT templ."Шаблон", templ."ТипОтправки", templ."ТипОтвета" FROM "ШаблоныПисем" as templ;</body>
      </definition>
    </select>
  </object>

</repository>
"""
