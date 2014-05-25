#!/usr/bin/env python
# coding: utf-8
__author__ = 'kevin'
import xlwt


class writexls:
    def __init__(self):
        pass

    def writeToExcel(self,filename, fieldnames, rows):

        wb = xlwt.Workbook(encoding='UTF-8')
        ws = wb.add_sheet('表格',cell_overwrite_ok=True)

        #得到第0行,写入标题
        row = ws.row(0)
        listRow = self.convDict2SortedList(fieldnames)
        for j in range(len(listRow)):
            row.write(j, listRow[j])
            print listRow[j]

        #从第i行开始写
        i_row = 1
        for i in range(i_row, len(rows) + i_row):
            #得到工作表的第i行
            row = ws.row(i)
            #将字典行转换为经过key排序的list,保证不错行
            listRow = self.convDict2SortedList(rows[i - i_row])

            #逐个单元格写入
            for j in range(len(rows[i - i_row])):
                #如果转换为字符串后大于15的长度,是数字的话会被
                #损失精度,后面转换为0,这里用文本的方式写入
                if len(str(listRow[j])) > 15:
                    row.set_cell_text(j, listRow[j])
                else:
                    row.write(j, listRow[j])

        wb.save(filename)

    def convDict2SortedList(self,dictRow):

        listRow = []
        keys = dictRow.keys()
        keys.sort()
        for key in keys:
            listRow.append(dictRow[key])

        return listRow


    def formateData(self,colums,data):
        rows = []
        for dictData in data:
            apendDict = dict()
            for i in colums:
                apendDict[i] = dictData[i]
            rows.append(apendDict)
        return rows






