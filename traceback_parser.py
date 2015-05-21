#coding=utf-8
'''
Created on 2015年5月18日
python traceback parser
@author: hzwangzhiwei
'''
import json
import re


def str_is_empty(s):
    if s == None or s == '' or s.strip().lstrip().rstrip('') == '':
        return True
    return False

class TracebackParser(object):
    '''
    parser
    '''
    tb_is_trace = True
    
    tb_content = ''
    
    tb_header = 'Traceback (most recent call last):'
    tb_files = [] # file, line, method 设计的文件信息
    tb_type = '' # 类型: AttributeError
    tb_msg = '' #信息: 'NoneType' object has no attribute 'model'
    
    def __init__(self):
        '''
        Constructor
        '''
        #do nothing
        pass
    
    def _try_tb_file(self, line, header = 'Traceback (most recent call last):'):
        '''尝试作为影响文件进行解析，成功范围字典，失败放回False
        '''
#         line = 'File "D:\Work\h28\client_replace\client\scriptvatarmembers\EquipMember.py", line 287, in onEnhanceEquip'
        tb_files_re = 'File "(.*)"[,] line (\d*), in (.*)'
        re_pat = re.compile(tb_files_re)
        search_ret = re_pat.search(line)
        if search_ret:
            g = search_ret.groups()
            if g and len(g) == 3:
                return {'file' : g[0], 'line': g[1], 'method': g[2]}
        return False
    
    def _try_tb_type_msg(self, line):
        '''尝试作为trace类型和提示消息进行解析，成功范围True，同时设置对象属性，失败放回False
        '''
        tb_type_msg_re = '(.*): (.*)'
        re_pat = re.compile(tb_type_msg_re)
        search_ret = re_pat.search(line)
        
        if search_ret:
            g = search_ret.groups()
            if g and len(g) == 2:
                self.tb_type = g[0]
                self.tb_msg = g[1]
                return True
        return False
        
    def parse(self, content):
        self.tb_header = 'Traceback (most recent call last):'
        self.tb_files = [] # file, line, method 设计的文件信息
        self.tb_type = '' # 类型: AttributeError
        self.tb_msg = '' #信息: 'NoneType' object has no attribute 'model'
        self.tb_content = content
        tb_lines = self.tb_content.split('\n')
        
        is_first_line = True
        for line in tb_lines:
            
            line = line.strip().lstrip().rstrip()
            if str_is_empty(line):
                continue
            #包含tb_header，说明是一个正确的trace
            if is_first_line:
                if self.tb_header in line:
                    is_first_line = False
                    continue
                else:
                    #不是一个合法的trace
                    self.tb_is_trace = False
                    return False
            else:
                #解析非第一行
                #1. 尝试以影响文件的解析，解析成功在下一行
                tb_file = self._try_tb_file(line)
                if tb_file:
                    self.tb_files.append(tb_file)
                    continue
                #2. 解析不成功，尝试以错误类型解析，解析不成功在下一行
                self._try_tb_type_msg(line)
        
        return True
    
    def trace_code_info(self):
        if self.tb_is_trace:
            if self.tb_files and len(self.tb_files) > 0:
                return self.tb_files[len(self.tb_files) - 1]
        return ('', '', '')
    
    def trace_msg(self):
        return (self.tb_type, self.tb_type)
    
        
    def tostring(self):
        rst = ''
        rst += self.tb_header
        rst += '\n'
        for f in self.tb_files:
            rst +=  json.dumps(f, default = lambda o: o.__dict__)
            rst += '\n'
        rst +=  self.tb_type + ': ' + self.tb_msg
        return rst
    
    #唯一标示一个trace
    def to_md5(self):
        rst = ''
        try:
            if self.tb_is_trace:
                rst += (self.tb_type + '|' + self.tb_msg)
                if self.tb_files and len(self.tb_files) > 0:
                    f = self.tb_files[len(self.tb_files) - 1] #取最后一个
                    rst += ('|' + f['file'] + '|' + f['line'] + '|' + f['method'])
        except:
            rst = ''
            
        import hashlib
        m = hashlib.md5()   
        m.update(rst)
        return m.hexdigest().lower()
        
                
    
if __name__ == '__main__':
    content = '''
    Traceback (most recent call last):
    File "D:\Work\h28\client_replace\client\script\lib\client\GateClient.py", line 337, in entity_message
        >methodname:(str)onEnhanceEquip
        >_done:(NoneType)None
        >entitymsg:(class common.proto_python.common_pb2.EntityMessage)routes: ""
id: "UG\022\264\327\037\375$\
        >self:(class client.GateClient.GateClient)<client.GateClient.GateClient object at 
        >entity:(class network.rpcentity.ClientEntities.ClientAvatar)<network.rpcentity.ClientEntities.Client
        >_controller:(class mobilerpc.RpcChannel.MobileRpcController)<mobilerpc.RpcChannel.MobileRpcControlle
        >entityid:(class bson.objectid.ObjectId)554712b4d71ffd24fb0c7b27
        >need_reg_index:(bool)False
        >method:(instancemethod)<bound method ClientAvatar.call_rpc_meth
    File "D:\Work\h28\client_replace\client\script\lib\common\rpcdecorator.py", line 100, in call_rpc_method
        >self:(class network.rpcentity.ClientEntities.ClientAvatar)<network.rpcentity.ClientEntities.Client
        >args:(tuple)({u'res': 2, u'eid': u'55481f68d71ffd24f
        >rpctype:(int)3
        >rpcmethod:(class common.rpcdecorator.RpcMethod)<common.rpcdecorator.RpcMethod object at
    File "D:\Work\h28\client_replace\client\script\lib\common\rpcdecorator.py", line 86, in call
        >parameters:(dict){u'res': 2, u'eid': u'55481f68d71ffd24fb
        >self:(class common.rpcdecorator.RpcMethod)<common.rpcdecorator.RpcMethod object at
        >args:(list)[2, '55481f68d71ffd24fb0c7de4', {u'itemI
        >entity:(class network.rpcentity.ClientEntities.ClientAvatar)<network.rpcentity.ClientEntities.Client
        >arg:(dict){u'itemId': 125, u'star': 3, u'itemType'
        >argtype:(class common.RpcMethodArgs.Dict)ed(Dict)
        >placeholder:(NoneType)None
        >first:(bool)False
    File "D:\Work\h28\client_replace\client\script\avatarmembers\EquipMember.py", line 287, in onEnhanceEquip
        >res:(int)2
        >self:(class network.rpcentity.ClientEntities.ClientAvatar)<network.rpcentity.ClientEntities.Client
        >equipUid:(str)55481f68d71ffd24fb0c7de4
        >notifyType:(int)2
        >newEquipDict:(dict){u'itemId': 125, u'star': 3, u'itemType'
        >equip:(class com.Equip.Equip)<com.Equip.Equip object at 0x17251E50>
        >oldEquip:(class com.Equip.Equip)<com.Equip.Equip object at 0x2740E7D0>
    File "D:\Work\h28\client_replace\client\script\avatarmembers\EquipMember.py", line 401, in getEquipNotifyDict
        >newAttrDict:(dict){'basePhyStrAdditionVal': 3352.156471239
        >allAttrNameSet:(set)set(['basePhyStrAdditionVal', 'criRate',
        >oldAttrDict:(dict){'basePhyStrAdditionVal': 3047.414973854
        >self:(class network.rpcentity.ClientEntities.ClientAvatar)<network.rpcentity.ClientEntities.Client
        >notifyType:(int)2
        >notifyDict:(dict){'notifyType': 2, 'attrList': []}
        >chinese_attrName:(str)生命值
        >sortedAllAttrNames:(list)[]
    File "D:\Work\h28\client_replace\client\script\com\utils\helpers.py", line 2945, in getAttributeNameC2E
        >chinese_name:(str)生命值
KeyError: '\xe7\x94\x9f\xe5\x91\xbd\xe5\x80\xbc'
    '''
    tb_parser = TracebackParser()
    tb_parser.parse(content)
    print '============'
    print tb_parser.tostring()
    print '============'