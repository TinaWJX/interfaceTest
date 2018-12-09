import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp

house_xls = common.get_xls("houseCase.xlsx", "tujia_cancelOrder")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*house_xls)
class CancelOrder(unittest.TestCase):
    def setParameters(self, case_name, method, token, oid, result, code, msg):
        """
        set params
        :param case_name:
        :param method: s
        :param token:
        :param oid:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        if str(oid) == "":
            oid_list = localReadConfig.get_order("tujia_oid").split(',')
            self.oid = oid_list[0]
            # print(str(oid_list) + '\n\n' + self.oid)
        else:
            self.oid = str(oid)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testCancelOrder(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml1('cancelOrder')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token
        if self.token == '0':
            token = localReadConfig.get_headers("token_v")
            header = {"token": str(token)}
            configHttp.set_headers(header)
        elif self.token == '1':
            pass

        # set headers
        # header = {"token": str(token)}
        # configHttp.set_headers(header)
        print("第二步：设置header(token等)")

        # set params
        data = {"partner_oid": self.oid}
        # data_json = json.dumps(data)
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数" + str(data))

        # test interface
        self.return_json = configHttp.postWithJson()
        # common.show_return_msg(self.return_json)
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            # email = common.get_value_from_return_json(self.info, 'member', 'email')
            self.assertEqual(self.info['result_code'], int(self.code))
            self.assertEqual(self.info['message'], self.msg)
            # self.assertEqual(email, self.email)

        if self.result == '1':
            self.assertEqual(self.info['result_code'], self.code)
            self.assertEqual(self.info['message'], self.msg)

    def tearDown(self):
        """

        :return:
        """
        info = self.info
        # if info['result_code'] == 0:
        #     # get user token
        #
        #     # price_rb = common.get_value_from_return_json(info, 'prices', 0)
        #     price_rb = common.get_group_from_return_json(info, 'total_price')
        #     # set user token to config file
        #     localReadConfig.set_price("total_price", str(price_rb))
        # else:
        #     pass
        self.log.build_case_line(self.case_name, str(self.info['result_code']), self.info['message'])
        print("测试结束，输出log完结\n\n")


