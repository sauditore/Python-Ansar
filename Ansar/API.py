from suds.client import Client


class AnsarAPI(object):
    def __init__(self, username, password):
        sp = Client('https://fanava.shaparak.ir/merchantwebservice/jax/merchantAuth?wsdl')
        login_request = sp.factory.builder.build('login').loginRequest
        login_request.username = username
        login_request.password = password
        self.sid = sp.service.login(login_request)
        self.sp = sp

    def reverse_transaction(self, amount, ref_num, rev_num):
        if not self.sid:
            return None
        context = self.build_context()
        revers_request = self.sp.factory.builder.build('reverseTransaction.reverseRequest')
        revers_request.amount = amount
        revers_request.mainTransactionRefNum = ref_num
        revers_request.reverseTransactionResNum = rev_num
        try:
            print revers_request
            print self.sp.service.reverseTransaction(context, revers_request)
            return True
        except Exception as e:
            print e.message
            return False

    def logout(self):
        context = self.build_context()
        try:
            self.sp.service.logout(context)
            return True
        except Exception as e:
            print e.message
            return False

    def build_context(self):
        con = self.sp.factory.builder.build('wsContext')
        entry = self.sp.factory.create('wsContext.data.entry')
        entry.key = 'SESSION_ID'
        entry.value = self.sid
        con.data.entry.append(entry)
        return con

    def verify(self, ref_num):
        verify_request = self.sp.factory.create('verifyTransaction.verifyRequest')
        verify_request.refNumList.append(ref_num)
        try:
            res = self.sp.service.verifyTransaction(self.build_context(), verify_request)
            if hasattr(res, 'verifyResponseResults'):
                v_res = res.verifyResponseResults
                if len(v_res) > 0:
                    if hasattr(v_res[0], 'amount'):
                        return True, (v_res[0].amount, v_res[0].refNum)
                return False, None
        except Exception as e:
            print e.message
            return None

    def settlement(self):
        context = self.build_context()
        try:
            self.sp.service.merchantSettlementRequest(context)
            return True
        except Exception as e:
            print e.message
            return False
