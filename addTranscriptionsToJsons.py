import json,csv,sys,os
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from matplotlib import gridspec
import numpy as np

DEBUG=False

def fixBox(ann,group,imagename):
    points=ann['poly_points']
    image = mpimg.imread(os.path.join('groups',group,imagename+'.jpg'))
    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1)
    ax_im = plt.subplot(gs[0])
    ax_im.imshow(image,cmap='gray')
    box = patches.Polygon(np.array(points),linewidth=2,edgecolor='r',facecolor='none')
    ax_im.add_patch(box)
    plt.show()
    trans = input('trans? (¦): ')
    return ann, trans

with open(sys.argv[1]) as f:
    reader = csv.reader(f,delimiter=',',quotechar='"')
    head=None
    json_path=None
    cur_json_path=None
    for row in reader:
        if head is None:
            head = {v:i for i,v in enumerate(row)}
            continue
        
        csvId = row[head['id']]
        group,image,bbId = csvId.split('-')
        trans = row[head['Transcription']]

        json_path = os.path.join('groups',group,image+'.json')
        if json_path!=cur_json_path:
            if cur_json_path is not None:
                json_data['fieldBBs']=list(fieldsById.values())
                if DEBUG:
                    with open('test/{}.json'.format(image),'w') as out:
                        json.dump(json_data,out)
                else:
                    with open(cur_json_path,'w') as out:
                        json.dump(json_data,out)
            with open(json_path) as j:
                json_data = json.load(j)
            if 'transcriptions' not in json_data:
                json_data['transcriptions']={}
            fieldsById={}
            for fieldBB in json_data['fieldBBs']:
                fieldsById[fieldBB['id']]=fieldBB
            cur_json_path=json_path

        assert(not any([x in trans for x in "«»¿§"]))
        if bbId not in fieldsById:
            continue



        while "\\" in trans and "'" in trans:
            if "'\\s[" in trans and "]'" in trans:
                newtrans = trans.replace("'\\s[","«")
                newtrans=newtrans.replace("]'","»")
                #print('Fix strikethrough: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\?'" in trans:
                newtrans=trans.replace("'\\?'","¿")
                #print('Fix unknown: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\illegible'" in trans:
                newtrans=trans.replace("'\\illegible'","§")
                #print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\ilegible'" in trans:
                newtrans=trans.replace("'\\ilegible'","§")
                #print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\empty'" in trans:
                newtrans=trans.replace("'\\empty'","")
                assert(len(newtrans)==0)
                #print('Fix empty: {} -> {}'.format(trans,newtrans))
                trans=newtrans

            elif "\\s[" in trans and "]'" in trans:
                newtrans = trans.replace("\\s[","«")
                newtrans=newtrans.replace("]'","»")
                #print('Fix strikethrough: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\?'" in trans:
                newtrans=trans.replace("\\?'","¿")
                #print('Fix unknown: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\illegible'" in trans:
                newtrans=trans.replace("\\illegible'","§")
                #print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\ilegible'" in trans:
                newtrans=trans.replace("\\ilegible'","§")
                #print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\empty'" in trans:
                newtrans=trans.replace("\\empty'","")
                assert(len(newtrans)==0)
                #print('Fix empty: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\bad" in trans:
                print('BAD: {}'.format(csvId))
                fieldsById[bbId],newtrans=fixBox(fieldsById[bbId],group,image)
                trans=newtrans
            else:
                print('Unknown case: {}'.format(trans))
                trans = input('Correct: ')


        while "\\" in trans:
            if "\\s[" in trans and "]" in trans:
                newtrans = trans.replace("\\s[","«")
                newtrans=newtrans.replace("]","»")
                #print('Fix strikethrough: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\?" in trans:
                newtrans=trans.replace("\\?","¿")
                #print('Fix unknown: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\illegible" in trans:
                newtrans=trans.replace("\\illegible","§")
                #print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\empty" in trans:
                newtrans=trans.replace("\\empty","")
                assert(len(newtrans)==0)
                #print('Fix empty: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\bad" in trans:
                print('BAD: {}'.format(csvId))
                fieldsById[bbId],newtrans=fixBox(fieldsById[bbId],group,image)
                trans=newtrans
            else:
                print('Unknown case: {}'.format(trans))
                trans = input('Correct: ')
        
        if bbId in json_data['transcriptions'] and json_data['transcriptions'][bbId]!=trans:
            print('trans descrip: {} != {}'.format(prevTrans[bbId],trans))
            trans = input('Correct: ')
        json_data['transcriptions'][bbId]=trans


    json_data['fieldBBs']=list(fieldsById.values())
    if DEBUG:
        with open('test/{}.json'.format(image),'w') as out:
            json.dump(json_data,out)
    else:
        with open(cur_json_path,'w') as out:
            json.dump(json_data,out)
