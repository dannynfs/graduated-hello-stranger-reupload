from importlib.resources import path
from logging import exception
from socket import SHUT_RD
import uuid
import shutil
from flask import Flask, redirect,render_template, url_for,request,jsonify,send_file
from flask_cors import CORS
import DB,json
import os

app = Flask(__name__)
CORS(app)
@app.route("/")             #切換 URL
def Home():
    return 'Home Page'

@app.route("/table/BLE/<uuid>")
def search(uuid):
    content = DB.show_data('BLE')
    data = {}
    for i in content:
        if(content[i]['UUID'] == str(uuid)):
            data = content[i]       
    try:
        return jsonify(data)
    except TypeError as e:
        return str(e)

@app.route("/table/<name>")
def table(name):
    content = DB.show_data(name)
    try:
        return jsonify(content)
    except TypeError as e:
        return str(e)

@app.route("/deleteAll/<name>")
def deleteAll(name):
    result = DB.delete_all(name)
    if(result['success']):
        return jsonify(result)
    else:
        return jsonify(result)

@app.route("/deviceInfo/<name>")
def device(name):
    content = DB.show_device_info(name)
    try:
        return jsonify(content)
    except TypeError as e:
        return str(e)

@app.route("/deviceInfo")
def allDevice():
    content = DB.show_device_info(-1)
    try:
        return jsonify(content)
    except TypeError as e:
        return str(content)

@app.route("/login",methods=["POST"])
def login():
    if(request.method == 'POST'):
        account = request.form.get('Account')
        password = request.form.get('Password')
        data = DB.show_data('People')
        for i in data:
            if((data[i]['Account'] == account) and data[i]['Password'] == password):
                return 'Success'
        return 'Failed'
    else:
        '訪問頁面方法錯誤'

@app.route("/modifyBLE",methods=["POST"])
def modifyBLE():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    result = DB.modify_BLE(temp)
    if(result['success']):
        return jsonify(result)
    else:
        return jsonify(result)

@app.route("/switchBLE",methods=["POST"])
def switchBLE():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    result = DB.switch_BLE(temp)
    if(result['success']):
        return jsonify(result)
    else:
        return jsonify(result)

@app.route("/deleteBLE",methods=["POST"])
def deleteBLE():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        os.remove(basedir + '/public/audios/' + temp['Venue'] + '/' + temp['Area'] + '/' + temp['Title'] + '.mp3')
    except:
        pass
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        os.remove(basedir + '/public/pics/' + temp['Venue'] + '/' + temp['Area'] + '/' + temp['Title'] + '.jpg')
    except:
        pass
    result = DB.delete_data("BLE",temp['UUID'])
    if(result['success']):
        return jsonify(result)
    else:
        return jsonify(result)

@app.route("/createVenue",methods=["POST"])
def createVenue():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    venueName = temp['Venue']

    basedir = os.path.abspath(os.path.dirname(__file__))
    targetdir = os.path.join(basedir,'public/audios')      # 建立 audios 資料夾
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)

    targetdir = os.path.join(targetdir,venueName)
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)
    
    targetdir = os.path.join(basedir,'public/pics')      # 建立 pics 資料夾
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)
    targetdir = os.path.join(targetdir,venueName)
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)

    targetdir = os.path.join(basedir,'public/images')      # 建立 image 資料夾
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)
    targetdir = os.path.join(targetdir,venueName)
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)

    result = DB.create_venue(temp['Venue'])
    if(result['success']):
        return jsonify(result)
    else:
        return jsonify(result)

@app.route("/deleteVenue",methods=["POST"])
def deleteVenue():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    shutil.rmtree(basedir + '/public/images/' + temp['Venue'])   # 刪除 //images//場館 檔案夾
    shutil.rmtree(basedir + '/public/audios/' + temp['Venue'])   # 刪除 //audios//場館 檔案夾
    shutil.rmtree(basedir + '/public/pics/' + temp['Venue'])   # 刪除 //pics//場館 檔案夾

    result = DB.delete_venue(temp['Venue'])                         # 刪除 Venue 的 table
    if(result['success']):
        data = DB.show_data('Map')
        for i in data:
            if(data[i]['Venue'] == temp['Venue']):
                result = DB.delete_data('Map',data[i]['Number'])    # 刪除 Map 內部資料
                device = DB.show_data('BLE')
                for j in device:
                    if(device[j]['MapNum'] == data[i]['Number']):
                        result = DB.delete_data('BLE',device[j]['UUID'])
                        if (not result['success']):
                            return jsonify({'success': 0, 'result': 'Fail to Delete BLE Data'})
                if(not result['success']):
                    return jsonify({'success': 0, 'result': 'Fail to Delete Map Content.'})
        return jsonify({'success': 1, 'result': 'Success to Delete Content.'})
    else:
        return jsonify({'success': 0, 'result':'Fail to Delete Venue'})

@app.route("/insertArea",methods=["POST"])
def insertArea():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    basedir = os.path.abspath(os.path.dirname(__file__))

    targetdir = os.path.join(basedir,'public/audios/' + str(temp['Venue']) + '/' + str(temp['Area']))
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)
    
    targetdir = os.path.join(basedir,'public/pics/' + str(temp['Venue']) + '/' + str(temp['Area']))
    exist = os.path.exists(targetdir)
    if(exist == False):
        os.mkdir(targetdir)

    temp['Route'] = basedir + "/" + temp['fileName']
    del temp['fileName']
    result = DB.insert_data(temp['Venue'],temp) 
    if(result['success']):
        result = DB.insert_data("Map",temp)
        if(result['success']):
            return jsonify(result)
        else:
            return jsonify(result)
    else:
        return jsonify(result)

@app.route("/deleteArea",methods=["POST"])
def deleteArea():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    content = DB.show_data("Map")
    venue = ''
    area = ''
    for i in range(0,len(content)):
        if (content[i]['Number'] == temp['MapNum']):
            venue = content[i]['Venue']
            area = content[i]['Area']
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    fileName = str(venue) + '_' + str(area) + '.jpg'
    targetdir = os.path.join(basedir,'public/images/' + str(venue) + '/' + fileName )
    os.remove(targetdir)                                                # 刪除 images 檔案夾內部圖片
    shutil.rmtree(basedir + '/public/audios/'+ str(venue) + '/' + str(area))    # 刪除 audios/venue/區域 資料夾
    shutil.rmtree(basedir + '/public/pics/'+ str(venue) + '/' + str(area))    # 刪除 pics/venue/區域 資料夾

    result = DB.delete_data("Map",temp["MapNum"])                       # 刪除 Map 內部資料
    if(result['success']):
        result = DB.delete_data(venue,area)                             # 刪除 Venue 內部資料
        if(result['success']):
            device = DB.show_data('BLE')
            for i in device:
                if(device[i]['MapNum'] == temp['MapNum']):
                    result = DB.delete_data('BLE',device[i]['UUID'])    # 刪除 BLE 內部資料
                    if(not result['success']):
                        return jsonify({'success':0, 'result': 'Fail to Delete BLE Data'})
            return jsonify({'success': 1, 'result':'Success to Delete Data'})
        else:
            return jsonify({'success': 0, 'result':'Fail to Delete Venue Data'})
    else:
        return jsonify({'success': 0, 'result':'Fail to Delete Map Data'})

@app.route("/showVenue")
def showVenue():
    result = DB.show_venue()
    temp = { "場館": result }
    return jsonify(temp)

@app.route("/newDevice",methods=["POST","GET"])
def newDevice():
    data = {}
    if (request.method == 'POST'):        
        data = str(request.data,encoding="UTF-8")
        temp = json.loads(data)
        data = { "UUID": temp['UUID'],'Tx':temp['tx'],'Rx':temp['rx'],'Nus':temp['nus'] }
        result = DB.insert_data("BLE", data)
        #content = {"UUID": id,'tx':tx,'rx':rx,'nus':nus}
        if(result['success']):
            return jsonify(result)
        else:
            return jsonify(result)
    elif (request.method == 'GET'):
        free = []
        busy = []
        data = DB.show_data('BLE')
        for i in data:
            if (data[i]['MapNum'] == None):
                free.append(data[i]['UUID'])
            else:
                busy.append(data[i]['UUID'])
        data = { "free": free, "busy": busy }
        return jsonify(data)

@app.route("/insertBLE",methods=["POST"])
def insertBLE():
    data = str(request.data,encoding="UTF-8")
    temp = json.loads(data)
    data = DB.show_data('Map')
    MapNum = -1
    for i in data:
        if (data[i]['Venue'] == temp['Venue'] and data[i]['Area'] == temp['Area']):
            MapNum = data[i]['Number']
            break
    if (temp['Audio'] == 1):
        basedir = os.path.abspath(os.path.dirname(__file__))
        targetdir = os.path.join(basedir,'public/audios/' + temp['Venue'] + '/' + temp['Area'] + '/' + temp['Title'] + '.mp3')
        temp['Audio'] = targetdir
        temp['AudLink'] = request.base_url[0:-10] + '/downloadAud/' + temp['UUID']
        # 新增temp['Aud Download']
    else:
        del temp['Audio']
    
    if (temp['Pic'] == 1):
        basedir = os.path.abspath(os.path.dirname(__file__))
        targetdir = os.path.join(basedir,'public/pics/' + temp['Venue'] + '/' + temp['Area'] + '/' + temp['Title'] + '.jpg')
        temp['Pic'] = targetdir
        temp['PicLink'] = request.base_url[0:-10] + '/downloadPic/' + temp['UUID']
        # 新增temp['Pic Download']
    else:
        del temp['Pic']
    
    del temp['Venue']
    del temp['Area']
    temp['MapNum'] = MapNum
    result = DB.modify_BLE(temp)
    if(result['success']):
        return jsonify(result)
    else:
        return jsonify(result)

@app.route("/uploadPic",methods=["POST"])
def uploadPic():
    try:
        img = request.files.get('file')
        format = img.filename[img.filename.index('.'):]
        basedir = os.path.abspath(os.path.dirname(__file__))
        venueName = img.filename.split('_')[0]
        targetdir = os.path.join(basedir,'public/images/' + venueName)
        if format in ('.jpg','.png','.jpeg','.HEIC','.jfif','.gif'):
            dir = targetdir + '/' + img.filename.replace(format,'.jpg')
            img.save(dir)
            result = {'success': 1, 'result': 'Upload Successfully'}
        else:
            result = {'success': 0, 'result': 'Type Wrong'}
    except Exception as e:
        result = {'success': 0, 'result': 'Upload Failed'}
    return jsonify(result)

@app.route("/uploadAud",methods=["POST"])
def uploadAud():
    try:
        aud = request.files.get('file')
        format = aud.filename[aud.filename.index('.'):]
        basedir = os.path.abspath(os.path.dirname(__file__))
        venueName = aud.filename.split('_')[0]
        areaName = aud.filename.split('_')[1]
        targetdir = os.path.join(basedir,'public/audios/' + venueName + '/' + areaName)
        if format in ('.mp3'):
            dir = targetdir + '/' + aud.filename.split('_')[2]
            aud.save(dir)
            result = {'success': 1, 'result': 'Upload Successfully'}
        else:
            result = {'success': 0, 'result': 'Type Wrong'}
    except Exception as e:
        result = {'success': 0, 'result': 'Upload Failed'}
    return jsonify(result)

@app.route("/uploadDevicePic",methods=["POST"])
def uploadDevicePic():
    try:
        pic = request.files.get('file')
        format = pic.filename[pic.filename.index('.'):]
        basedir = os.path.abspath(os.path.dirname(__file__))
        venueName = pic.filename.split('_')[0]
        areaName = pic.filename.split('_')[1]
        targetdir = os.path.join(basedir,'public/pics/' + venueName + '/' + areaName)
        if format in ('.jpg'):
            dir = targetdir + '/' + pic.filename.split('_')[2]
            pic.save(dir)
            result = {'success': 1, 'result': 'Upload Successfully'}
        else:
            result = {'success': 0, 'result': 'Type Wrong'}
    except Exception as e:
        result = {'success': 0, 'result': 'Upload Failed'}
    return jsonify(result)

@app.route("/devices/<UUID>/config.json")
def deviceContent(UUID):
    people = DB.deviceVisitor(UUID)
    people = people + 1
    result = DB.modify_BLE({'UUID':UUID, 'Visitor':people})
    if result['success'] == 0:
        return result['result']
    data = DB.show_data("BLE")
    for i in data:
        if data[i]['UUID'] == UUID:
            content = {
                "type" : "A",
                "uniqueId": data[i]['UUID'],
                "service": data[i]['Nus'],
                "tx": data[i]['Tx'],
                "rx": data[i]['Rx'],
                "photoRef": data[i]['PicLink'],
                "audioRef": data[i]['AudLink'],
                "title": data[i]['Title'],
                "content": data[i]['Message'],
                "href": data[i]['Href'],
                "visitor": data[i]['Visitor']
            }
            for j in content:
                if(content[j] == None):
                    content[j] = ""
            return jsonify(content)
    return "There's no specific device data in the database!!"

@app.route("/distribute/<id>")
def distributeUUID(id):
    tx = str(uuid.uuid1())
    rx = str(uuid.uuid1())
    nus = str(uuid.uuid1())
    content = {"UUID": id,'tx':tx,'rx':rx,'nus':nus}
    result = DB.modify_BLE(content)
    if(result['success']):
        return jsonify(content)
    else:
        return jsonify(result)

@app.route("/renewBattery",methods=['POST'])
def renewBattery():
    data = str(request.data,encoding="UTF-8")
    content = json.loads(data)
    result = DB.modify_BLE(content)
    if(result['success']):
        return jsonify(content)
    else:
        return jsonify(result)

@app.route("/fetchDownloadURL",methods=["POST"])
def fetchDownloadURL():
    data = str(request.data,encoding="UTF-8")
    content = json.loads(data)
    result = DB.modify_BLE(content)
    if(result['success']):
        return jsonify(result)
    else:
        return jsonify(result)

@app.route("/downloadPic/<uuid>")
def downloadPic(uuid):
    try:
        data = DB.show_device_info(-1)
        picRoute = ""
        for i in data:
            if(i['UUID'] == uuid):
                picRoute = i['Pic']
                break
        return send_file(picRoute,as_attachment=False)
    except exception as e:
        return 'Failed to Download Pic.\nReason: ' + str(e)

@app.route("/downloadAud/<uuid>")
def downloadAud(uuid):
    try:
        data = DB.show_device_info(-1)
        audRoute = ""
        for i in data:
            if(i['UUID'] == uuid):
                audRoute = i['Audio']
                break
        return send_file(audRoute,as_attachment=False)
    except exception as e:
        return 'Failed to Download Pic.\nReason: ' + str(e)

@app.route("/localURL")
def loacalURL():
    url = request.base_url
    return url[0:-9]

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)