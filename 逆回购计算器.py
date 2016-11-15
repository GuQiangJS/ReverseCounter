import datetime
import re
from pathlib import Path
import os

print('深圳逆回购计算器');

codeList=('131810-R001','131811-R002','131800-R003','131809-R004','131801-R007','131802-R014','131803-R028','131805-R091','131806-R182');
dateList=(1,2,3,4,7,14,28,91,182);
feeList=(0.00001,0.00002,0.00003,0.00004,0.00005,0.0001,0.0002,0.0003,0.0003);
ReverseRepurchaseRecordsFileLocation="d:\\StockData\\ReverseRepurchase\\Record.{0}.csv";
ReverseRepurchaseRecordsFilePath="d:\\StockData\\ReverseRepurchase";

def getRecord():
        #编号
        inputCode='';
        #数量
        inputCount=0;  
        #收益率
        inputRate=0;
        #日期
        inputDate=datetime.date.today();

        listIndex=0;

        codeValidate=False;
        while(codeValidate is False):
                print("输入编号:");
                for code in codeList:
                        print(code[8:]+" : "+code);
                codeInput=input();
                index=0;
                while( index < len(codeList)):
                        if(codeList[index][8:]==codeInput):
                                inputCode=codeList[index];
                                listIndex=index;
                                codeValidate=True;
                                break;
                        index=index+1;
                if(codeValidate is False):
                        print("编号错误!");

        countValidate=False;
        while(countValidate is False):
                print("输入购买数量（Exp:10表示购买1000元）:");
                countInput=int(input());
                if(countInput>0):
                        countValidate=True;
                        inputCount=countInput*100;
                        break;
                else:
                        print("数量错误！");

        countDate=False;
        while(countDate is False):
                print("输入购买日期，格式为：yyyy-MM-dd (默认日期："+inputDate.isoformat()+")");
                dateInput=input();
                if(dateInput is ""):
                        break;
                else:
                        matchObj = re.match( "(\d{4})-(\d{1,2})-(\d{1,2})", dateInput);
                        if(matchObj):
                                inputDate=datetime.date(int(matchObj.group(1)), int(matchObj.group(2)), int(matchObj.group(3)))
                                countValidate=True;
                                break;
                        else:
                                print("日期错误！");

        print("输入比率：");
        inputRate=float(input());
                     
        print("数量="+inputCode);  
        print("日期期限="+str(dateList[listIndex]));
        print("税费="+str(feeList[listIndex]*100)+"%");   
        #print("InputCount="+str(inputCount));
        print("购买日期="+str(inputDate));  
        #print("InputRate="+str(inputRate));

        estimatedEarnings=round(inputCount*inputRate/100/360*dateList[listIndex],4);
        print("税前收益="+str(estimatedEarnings));
        processingFee=round(inputCount*feeList[listIndex],4);
        print("税费="+str(processingFee));
        print("-------------------------------------");

        return inputCode+","+str(inputCount)+","+str(inputRate)+","+str(inputDate)+","+str(round(estimatedEarnings,2))+","+str(round(processingFee,2))+","+str(round((estimatedEarnings-processingFee),2))


def appendFile(record,userName):
        if not os.path.isdir(ReverseRepurchaseRecordsFilePath):
                os.makedirs(ReverseRepurchaseRecordsFilePath);
        if(Path(ReverseRepurchaseRecordsFileLocation.format(userName)).exists() is False):
                f = open(ReverseRepurchaseRecordsFileLocation.format(userName), 'a+',newline='\n');
                f.write("Code,Count,Rate,Date,EstimatedEarnings,Fee,Earnings");
                f.write('\n');
                f.close();
                print("文件不存在，创建成功");
                print("-------------------------------------");
        f = open(ReverseRepurchaseRecordsFileLocation.format(userName), 'a+',newline='\n');
        f.write(record);
        f.write('\n');
        f.close();
        print("文件保存成功");
        print("-------------------------------------");

def getUser():
        while(True):
                print("输入用户名：");
                un=input();
                if(un!=""):
                        return un;
                        break;
                else:
                        print("用户名不能为空！");


while(True):
        record=getRecord();
        if(record is not ""):
                print("输入 'SAVE' 保存数据，直接输入 'Enter' 跳过保存");
                print("-------------------------------------");
                if("SAVE"==input().upper()):
                        appendFile(record,getUser().capitalize());
                else:
                        print("跳过保存文件");
                        print("-------------------------------------");
        
