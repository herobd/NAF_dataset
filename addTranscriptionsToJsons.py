import json,csv,sys,os
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from matplotlib import gridspec
import numpy as np

DEBUG=True
if DEBUG:
    print('DEBUG')

def fixBox(ann,group,imagename):
    #points=ann['poly_points']
    #image = mpimg.imread(os.path.join('groups',group,imagename+'.jpg'))
    #fig = plt.figure()
    #gs = gridspec.GridSpec(1, 1)
    #ax_im = plt.subplot(gs[0])
    #ax_im.imshow(image,cmap='gray')
    #box = patches.Polygon(np.array(points),linewidth=2,edgecolor='r',facecolor='none')
    #ax_im.add_patch(box)
    #plt.show()
    trans = input('trans? (¦): ')
    return ann, trans

with open(sys.argv[1]) as f:
    head=None
    json_path=None
    cur_json_path=None
    data=[]
    if sys.argv[1].endswith('.csv'):
        reader = csv.reader(f,delimiter=',',quotechar='"')
        for ri,row in enumerate(reader):
            if head is None:
                head = {v:i for i,v in enumerate(row)}
                continue
            
            csvId = row[head['id']] if 'id' in head else row[head['ID']]
            trans = row[head['Transcription']]

            empty = 'FALSE'!=row[head['empty']] if 'empty' in head else False
            bad_crop = 'FALSE'!=row[head['bad crop']] if 'bad crop' in head else False
            illegible = 'FALSE'!=row[head['illegible']] if 'illegible' in head else False

        data.append((csvId,trans,empty,bad_crop,illegible,row[head['image']]))
    elif sys.argv[1].endswith('.json'):
        instances = json.load(f)
        for i in instances:
            if 'id' in i and 'gt' in i:
                data.append((i['id'],i['gt'],False,False,False,i['context_image']))
            elif 'gt' in i and 'matches' in i:
                for csv_id in i['matches']:
                    data.append((csv_id,i['gt'],False,False,False,i['image']))

    for csvId,trans,empty,bad_crop,illegible,image_name in data:
        print(csvId)
        group,image,bbId = csvId.split('-')
        json_path = os.path.join('groups',group,image+'.json')
        if json_path!=cur_json_path:
            if cur_json_path is not None:
                #json_data['fieldBBs']=list(fieldsById.values())
                if DEBUG:
                    print('write {}'.format(cur_image))
                    with open('test/{}.json'.format(cur_image),'w') as out:
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
            textById={}
            for textBB in json_data['textBBs']:
                textById[textBB['id']]=textBB
            cur_json_path=json_path
            cur_image=image

        assert(not any([x in trans for x in "«»¿§"]))
        if bbId not in fieldsById and bbId not in textById:
            import pdb;pdb.set_trace()
            continue

        if len(trans)==0:
            if illegible:
                trans = "§"
            elif empty:
                pass
            elif bad_crop:
                print('!!!')
                print('bad_crop: {} {}'.format(csvId,image_name))
                fieldsById[bbId],newtrans=fixBox(fieldsById[bbId],group,image)
                trans=newtrans
        elif illegible:
            print('{} marked as illegible, but trans is : {}'.format(csvId,trans))
        elif empty:
            print('{} marked as empty, but has trans: {}'.format(csvId,trans))
            trans = input('Correct: ')
        elif bad_crop:
            print('bad_crop: {} {}'.format(csvId,image_name))
            print(' but had trans: {}'.format(trans))
            fieldsById[bbId],newtrans=fixBox(fieldsById[bbId],group,image)
            trans=newtrans


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
            elif "S\\[" in trans and "]" in trans:
                newtrans = trans.replace("S\\[","«")
                newtrans=newtrans.replace("]","»")
                #print('Fix strikethrough: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "s\\[" in trans and "]" in trans:
                newtrans = trans.replace("s\\[","«")
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
            print('Different transcription. Prev: {} != New: {}'.format(json_data['transcriptions'][bbId],trans))
            if json_data['transcriptions'][bbId]!='' and trans!='':
                new_trans = input('Enter correct (leave blank to accept new): ')
                if new_trans!='':
                    trans=new_trans
            else:
                trans = input('Enter correct: ')

        json_data['transcriptions'][bbId]=trans
        #print('{} : {}'.format(bbId,trans))


    #json_data['fieldBBs']=list(fieldsById.values())
    if DEBUG:
        with open('test/{}.json'.format(image),'w') as out:
            json.dump(json_data,out)
    else:
        with open(cur_json_path,'w') as out:
            json.dump(json_data,out)
