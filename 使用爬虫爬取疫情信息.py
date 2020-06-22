import requests,os
import re
import xlwt
import time
import json

class get_outbreak_info:

    def get_data_html(self):
            # 伪装成浏览器，防止网站反爬虫
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
            # 请求页面
            response = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0', headers=headers, timeout=3)
            # 中文重新编码
            response = str(response.content, 'utf-8')
            #返回了HTML数据
            return response
            
    def get_data_dictype(self):
            areas_type_dic_raw = re.findall('try { window.getAreaStat = (.*?)}catch\(e\)',self.get_data_html())
            areas_type_dic = json.loads(areas_type_dic_raw[0])
            #返回经过json转换过的字典化的数据
            return areas_type_dic
            
    def save_data_to_excle(self):
            #调用方法检查数据目录是否存在，不存在则创建数据文件夹
            self.make_dir()
            
            #数据写入行数记录
            count = 2
            
            # 打开工作簿，创建工作表
            newworkbook = xlwt.Workbook()
            worksheet = newworkbook.add_sheet('all_data')
            
            #写入数据列标签
            worksheet.write(1, 2, '省份名称')
            worksheet.write(1, 3, '省份简称或城市名称')
            worksheet.write(1, 4, '确诊人数')
            worksheet.write(1, 5, '疑似人数')
            worksheet.write(1, 6, '治愈人数')
            worksheet.write(1, 7, '死亡人数')
            worksheet.write(1, 8, '现存确诊')
            
            #用循环获取省级以及该省以下城市的数据
            for province_data in self.get_data_dictype():
                    provincename = province_data['provinceName']
                    provinceshortName = province_data['provinceShortName']
                    p_confirmedcount = province_data['confirmedCount']
                    p_suspectedcount = province_data['suspectedCount']
                    p_curedcount = province_data['curedCount']
                    p_deadcount = province_data['deadCount']
                    p_currentConfirmedCount = province_data['currentConfirmedCount']
                    
                    #在工作表里写入省级数据
                    worksheet.write(count, 2, provincename)
                    worksheet.write(count, 3, provinceshortName)
                    worksheet.write(count, 4, p_confirmedcount)
                    worksheet.write(count, 5, p_suspectedcount)
                    worksheet.write(count, 6, p_curedcount)
                    worksheet.write(count, 7, p_deadcount)
                    worksheet.write(count, 8, p_currentConfirmedCount)
                    
                    #此处为写入行数累加，province部分循环
                    count += 1
                    
                    #该部分获取某个省下某城市的数据
                    for citiy_data in province_data['cities']:
                            cityname = citiy_data['cityName']
                            c_confirmedcount = citiy_data['confirmedCount']
                            c_suspectedcount = citiy_data['suspectedCount']
                            c_curedcount = citiy_data['curedCount']
                            c_deadcount = citiy_data['deadCount']
                            c_currentConfirmedCount = citiy_data['currentConfirmedCount']
                            
                            #该部分在工作表里写入某城市的数据
                            worksheet.write(count, 3, cityname)
                            worksheet.write(count, 4, c_confirmedcount)
                            worksheet.write(count, 5, c_suspectedcount)
                            worksheet.write(count, 6, c_curedcount)
                            worksheet.write(count, 7, c_deadcount)
                            worksheet.write(count, 8, c_currentConfirmedCount)
                            
                            #此处为写入行数累加，cities部分循环
                            count += 1
                            
            current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            newworkbook.save('D:\实时疫情信息\实时采集v3.0-%s.xls' % (current_time))
            print('======数据爬取成功======')

    def make_dir(self):
            #检查并创建数据目录
            file_path = 'D:/实时疫情信息/'
            if not os.path.exists(file_path):
                    os.makedirs(file_path)
                    print('该文件夹不存在')
                    print('自动创建文件夹')
                    print('创建目录为%s'%(file_path))
            else:
                    print('数据保存在目录：%s' % (file_path))
            

    def exe_task(self):
            times = int(input('请输入执行采集次数：'))
            #round 方法保留一位小数
            interval_time = round(float(input('请输入每次执行间隔时间（分钟）：')),1)
            interval_time_min = interval_time * 60

            for i in range(times):
                    get_outbreak_info().save_data_to_excle()
                    time.sleep(interval_time_min)

    #执行完整采集任务

get_outbreak_info().exe_task()
