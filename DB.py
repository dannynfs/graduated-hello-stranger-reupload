"""
注意事項:
    1. 資料中請不要使用 ' 會影響 sql 語法
    2. 之後記得部分改成 POST (鈺修進度)
    3. 新增圖片後會儲存在 public/images/<場館名稱>/ 底下並命名為 <場館名稱_區域名稱.jpg>
    4. 裝置配對訊息之後會在 
    5. 場館名稱跟區域名稱不要全數字

路由內容:
    ★ /table/<表格名稱> => 查看目標表格內容 => GET
    ★ /table/BLE/<uuid> => 針對uuid 去查詢 BLE 裝置
    ★ /deviceInfo => 查看所有裝置狀態 => GET
    ★ /deviceInfo/<館>
    ★ /createVenue => 新增場館 => POST (備註1)
    ★ /deleteVenue => 刪除場館 => POST (備註2)
    ★ /login => 登入檢查 => POST (備註2)
    ★ /modifyBLE => 修正BLE內部內容  => POST (備註3)
    ★ /switchBLE => 一鍵開關 => POST (備註4)
    ★ /deleteBLE => 刪除特定 BLE => POST (備註5)
    ★ /deleteAll/<表格名稱> => 刪除該表格所有資料 => GET
    ★ /insertArea => 新增區域 => POST(備註6)
    ★ /deleteArea => 刪除區域 => POST(備註7)
    ★ /newDevice => 裝置和前端配對 UUID => 裝置: POST/ 前端: GET (備註8)
    ★ /showVenue => 顯示所有場館 => GET
    ★ /insertBLE => 設定裝置所配對到的資料 => POST (備註9)
    ★ /uploadPic => 上傳圖片 => POST (備註10)
    ★ /device/<UUID> => 回傳該UUID裝置之資訊 => get (裝置取得開關 + app端取得資料)
    ★ /distribute/<UUID> => 回傳該UUID硬體裝置分配到的TX、RX => get
    ★ /renewBattery/<UUID> => 硬體裝置更新電量 => POST (備註11)
    ★ /downloadPic/<uuid> => 下載該裝置上的照片 => GET
    ★ /downloadAud/<uuid> => 下載該裝置上的音檔 => GET


備註:
    1. 前端以 json 來 POST, 傳入場館名稱
    2. 前端以 json 來 POST, 傳入場館名稱
    2. 前端以 form 的 value 來 POST, 分別傳入帳號密碼
    3. 前端以 json 來 POST, 傳入 UUID, Message, Status, Note
    4. 前端以 json 來 POST, 傳入 Status
    5. 前端以 json 來 POST, 傳入 UUID
    6. 前端以 json 來 POST, 傳入 fileName, Venue, Area
    7. 前端以 json 來 POST, 傳入 MapNum
    8. 裝置以 json 來 POST, 傳入 UUID
    9. 前端以 json 來 POST, 傳入 UUID, Message, Venue, Area, Xaxis, Yaxis, Title
    10. 前端以 form 的方法來傳圖片
    11. 裝置以 json 來 POST, 傳入 UUID, Battery 欄位
"""
import sqlite3
dbContent = {
    'People': ['Email','Account','Password'],
    'BLE':['UUID','Message','MapNum','Xaxis','Yaxis','Battery','Status','Note','Title','Audio','Href','Tx','Rx','Nus','Pic','JsonLink','PicLink', 'AudLink','Visitor','RSSI'],
    'Map':['Number','Route','Venue','Area'],
    '場館內容':['Route','Venue','Area'],
    'PK':{
        'People':'Email',
        'BLE':'UUID',
        'Map':'Number'
    }
}

def show_data(table_name):                  #回傳表格內容
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute('Select * from {}'.format(table_name))
        conn.commit()
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        result = {}
        for row in range(0,len(records)):
            temp = {}
            for col in range(0, len(records[row])):
                if(table_name == 'BLE' or table_name == 'People' or table_name == 'Map'):
                    temp[dbContent[table_name][col]] = records[row][col]
                else:
                    temp[dbContent['場館內容'][col]] = records[row][col]
            result[row] = temp
        return result
    except sqlite3.OperationalError as e:
        return e

#新增一筆資料 (BLE 資料中的電量和狀態預設為 "0%" 和 "Turn Off"), (Map 和 Message 的 PK 有 AUTOINCREMENT)
def insert_data(table_name, content):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        if (table_name != "BLE"):
            ins = 'Insert into {} ('.format(table_name)
            if(table_name == 'People'):
                ins += 'Email,Account,Password) values ("{}","{}","{}"'.format(content['Email'],content['Account'],content['Password'])
            else:
                ins += 'Route,Venue,Area) values ("{}","{}","{}"'.format(content['Route'],content['Venue'],content['Area'])
            ins += ');'
        else:
            ins = "Insert into BLE ('UUID','Tx','Rx','Nus') Values ('{}','{}','{}','{}');".format(content['UUID'],content['Tx'],content['Rx'],content['Nus'])
        cursor.execute(ins)
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": 1,'result': '新增成功'}
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return {"success": 0, "result": str(e)}

def delete_data(table_name, pk):        #刪除一筆資料
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        if(table_name == 'BLE' or table_name == 'People' or table_name == 'Map'):
            ins = 'Delete from {} where {} = '.format(table_name,dbContent['PK'][table_name])
        else:
            ins = 'Delete from {} where Area = '.format(table_name)
        if(type(pk) == str):
            ins += "'{}';".format(pk)
        else:
            ins += '{};'.format(pk)
        cursor.execute(ins)
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": 1,'result': '刪除成功'}
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return {"success": 0, "result": str(e)}

def delete_all(table_name):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        ins = 'Delete from {};'.format(table_name)
        cursor.execute(ins)
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": 1,'result': '刪除成功'}
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return {"success": 0, "result": str(e)}

def modify_BLE(content):        #修正 BLE 資料
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        ins = "Update BLE set "
        for i in content:
            if(i == 'UUID'):
                continue
            else:
                if(type(content[i]) == str):
                    ins += "{} = '{}',".format(i,content[i])
                elif(content[i] == None):
                    ins += "{} = 'Null',".format(i)
                else:
                    ins += "{} = {},".format(i,content[i])
        ins = ins[:-1]
        ins += " where UUID = '{}';".format(content['UUID'])
        cursor.execute(ins)
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": 1,'result': '修改成功'}
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return {"success": 0, "result": str(e)}

def show_device_info(number):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        if(number != -1):
            cursor.execute('SELECT * from BLE INNER JOIN Map on BLE.MapNum = Map.Number where BLE.MapNum = {};'.format(number))
        else:
            cursor.execute('SELECT * from BLE INNER JOIN Map on BLE.MapNum = Map.Number;')
        conn.commit()
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        result = []
        for row in range(0,len(records)):
            temp = {}
            temp['UUID'] = records[row][0]
            temp['Message'] = records[row][1]
            temp['MapNum'] = records[row][2]
            temp['Xaxis'] = records[row][3]
            temp['Yaxis'] = records[row][4]
            temp['Battery'] = records[row][5]
            temp['Status'] = bool(records[row][6])
            temp['Note'] = records[row][7]
            temp['Title'] = records[row][8]
            temp['Audio'] = records[row][9]
            temp['Href'] = records[row][10]
            temp['Pic'] = records[row][14]
            temp['Visitor'] = records[row][18]
            temp['RSSI'] = records[row][19]
            temp['Route'] = records[row][len(records[row])-3]
            temp['Venue'] = records[row][len(records[row])-2]
            temp['Area'] = records[row][len(records[row])-1]
            result.append(temp)
        return result
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return e

def switch_BLE(content):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        ins = 'Update BLE set '
        ins += 'Status = {} where MapNum = "{}";'.format(content['Status'],content['MapNum'])
        cursor.execute(ins)
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": 1,'result': '修改成功'}
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return {"success": 0, "result": str(e)}

def show_venue():
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        result = []
        cursor.execute('Select * from sqlite_master;')
        conn.commit()
        records = cursor.fetchall()
        for i in range(0,len(records)):
            if(records[i][0] == 'index'):
                continue
            if(records[i][1] == 'People' or records[i][1] == 'Map' or records[i][1] == 'BLE' or records[i][1] == 'sqlite_sequence'):
                continue
            result.append(records[i][1])
        cursor.close()
        conn.close()
        return result
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return e

def create_venue(name):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        ins = "Create Table '{}' ('Route' TEXT UNIQUE, 'Venue' TEXT, 'Area' TEXT UNIQUE, PRIMARY KEY('Area'));".format(name)
        cursor.execute(ins)
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": 1,'result': '新增成功'}
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return {"success": 0, "result": str(e)}

def delete_venue(name):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        ins = "Drop Table {};".format(name)
        cursor.execute(ins)
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": 1,'result': '刪除成功'}
    except sqlite3.OperationalError as e:
        cursor.close()
        conn.close()
        return {"success": 0, "result": str(e)}

def deviceVisitor(UUID):
    number = 0
    temp = show_data('BLE')
    for i in temp:
        if UUID == temp[i]['UUID']:
            number = temp[i]['Visitor']
            break
    return number
