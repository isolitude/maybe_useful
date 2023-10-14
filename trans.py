import json
import xml.etree.ElementTree as ET
import glob

def getjson(path):
    with open(path,encoding='utf-8') as f:
        cont=json.load(f)
    num=cont.__len__()
    print('total number is',num)
    return num,cont

def keycheck(cont,key):
    for i in cont:
        if key in i:
            ans=i[key]
            break
    return ans
    
def setxml(num,cont):
    data=ET.Element('i')
    chatserver=ET.SubElement(data,'chatserver')
    chatserver.text="chat.bilibili.com"
    chatid=ET.SubElement(data,'chatid')
    chatid.text="1229748602"
    mission=ET.SubElement(data,'mission')
    mission.text="0"
    maxlimit=ET.SubElement(data,'maxlimit')
    maxlimit.text=str(num)
    state=ET.SubElement(data,'state')
    state.text="0"
    real_name=ET.SubElement(data,'real_name')
    real_name.text="0"
    source=ET.SubElement(data,'source')
    source.text="k-v"
    for t in range(num):
        i=cont[t]
        p=ET.SubElement(data,'d')
        try:
            ans=str(i['progress']/1000)+','+str(i['mode'])+','+str(i['fontsize'])+','+str(i['color'])+','+str(i['ctime'])+',0,'+i['midHash']+','+i['idStr']
        except KeyError as Argument:
            #去你妈的异常处理，
            print(Argument)
            i[Argument.args[0]]=keycheck(cont,Argument.args[0])
            print()
            ans=str(i['progress']/1000)+','+str(i['mode'])+','+str(i['fontsize'])+','+str(i['color'])+','+str(i['ctime'])+',0,'+i['midHash']+','+i['idStr']
        p.set('p',ans)
        p.text=i['content']
    return data


def jsontoxml(path):
    num,cont=getjson(path)
    tree=ET.ElementTree("tree")
    tree._setroot(setxml(num,cont))
    ET.indent(tree, '  ')
    tree.write(path[:-5]+".xml", encoding = "UTF-8", xml_declaration = True)  


if __name__=='__main__':
    path=glob.glob('*.json')
    for i in path:
        jsontoxml(i)