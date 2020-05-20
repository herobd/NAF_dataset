import json,csv,sys

with open(sys.argv[1]) as f:
    reader = csv.reader(f,delimiter=',',quotechar='"')
    head=None
    for row in reader:
        if head is None:
            head = {v:i for i,v in enumerate(row)}
            continue
        
        csvId = row[head['id']]
        group,image,bbId = csvId.split('-')
        trans = row[head['Transcription']]

        assert(not any([x in trans for x in "«»¿§"]))

        while "\\" in trans and "'" in trans:
            if "'\\s[" in trans and "]'" in trans:
                newtrans = trans.replace("'\\s[","«")
                newtrans=newtrans.replace("]'","»")
                print('Fix strikethrough: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\?'" in trans:
                newtrans=trans.replace("'\\?'","¿")
                print('Fix unknown: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\illegible'" in trans:
                newtrans=trans.replace("'\\illegible'","§")
                print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\ilegible'" in trans:
                newtrans=trans.replace("'\\ilegible'","§")
                print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "'\\empty'" in trans:
                newtrans=trans.replace("'\\empty'","")
                assert(len(newtrans)==0)
                print('Fix empty: {} -> {}'.format(trans,newtrans))
                trans=newtrans

            elif "\\s[" in trans and "]'" in trans:
                newtrans = trans.replace("\\s[","«")
                newtrans=newtrans.replace("]'","»")
                print('Fix strikethrough: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\?'" in trans:
                newtrans=trans.replace("\\?'","¿")
                print('Fix unknown: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\illegible'" in trans:
                newtrans=trans.replace("\\illegible'","§")
                print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\ilegible'" in trans:
                newtrans=trans.replace("\\ilegible'","§")
                print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\empty'" in trans:
                newtrans=trans.replace("\\empty'","")
                assert(len(newtrans)==0)
                print('Fix empty: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\bad" in trans:
                print('BAD: {}'.format(csvId))
                trans='¦BAD¦'
            else:
                print('Unknown case: {}'.format(trans))
                trans = input('Correct: ')


        while "\\" in trans:
            if "\\s[" in trans and "]" in trans:
                newtrans = trans.replace("\\s[","«")
                newtrans=newtrans.replace("]","»")
                print('Fix strikethrough: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\?" in trans:
                newtrans=trans.replace("\\?","¿")
                print('Fix unknown: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\illegible" in trans:
                newtrans=trans.replace("\\illegible","§")
                print('Fix illegible: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            elif "\\empty" in trans:
                newtrans=trans.replace("\\empty","")
                assert(len(newtrans)==0)
                print('Fix empty: {} -> {}'.format(trans,newtrans))
                trans=newtrans
            else:
                print('Unknown case: {}'.format(trans))
                trans = input('Correct: ')
