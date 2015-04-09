'# coding: utf8'
from os import path, remove
from demjson import encode
from lxml import etree
from math import floor
from time import mktime, strptime
from const_file import FILE_PATH, channel, CHANNELEPG_CURRENT_XML, lang

path.exists(FILE_PATH) and remove(FILE_PATH)
jsondict = {}
for ch in channel:
    currentEpgXml = CHANNELEPG_CURRENT_XML
    try:
        currentEpg = etree.parse(currentEpgXml)
    except:
        print("The XML is not valid: Couldn't get EPG")
    event_id = []
    start_time = []
    for chan in currentEpg.xpath('//programme[@channel="{0}"]'.format(ch)):
        stop_time = chan.attrib["start"].split(" ", 1)[0]
        start = str(int(floor(mktime(strptime(stop_time, "%Y%m%d%H%M%S")))))
        start_time.append(start)
        channel_name = chan.attrib["channel"]
        events = 0
        for sf in chan.getchildren():
            titles = sf.xpath('//title[@lang="{0}"]/text()'.format(lang))
            description = sf.xpath('//desc[@lang="{0}"]/text()'.format(lang))
            events += 1
            event_id.append(events)
        jsondict[channel_name] = []
        channel = jsondict[channel_name]
    for title, desc, evid, time in zip(titles, description,
                                       event_id, start_time):
        item_dict = {}
        item_dict['title'] = title
        item_dict['description'] = desc
        item_dict['eventId'] = int(evid)
        item_dict['time'] = int(time)
        channel.append(item_dict)

with open(FILE_PATH, 'w') as f:
    f.write(encode(jsondict, compactly=True, encoding='utf8'))
    f.flush()
