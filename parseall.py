import csv


"""
Loop through the rows of all.csv, created via download.py, and turn the raw forms into cleanly-structured data stored in processed.csv.
"""

headers = {
    'name': {'labels': ['TRAVELER NAME','TRAVELER'], 'pos': None, 'val': None, 'rows': [1,]},
    'descrip': {'labels': ['EVENT DESCRIPTION','DESCRIPTION'], 'pos': None, 'val': None, 'rows': [1,]},
    'start': {'labels': ['BEGINNING DATE   [MM/DD/YYYY]','BEGINNING DATE [MM/DD/YYYY]','BEGINNING DATE'], 'pos': None, 'val': None, 'rows': [1,]},
    'location': {'labels': ['LOCATION',"""LOCATION AND
TRAVEL DATES"""], 'pos': None, 'val': None, 'rows': [1,]},
    'dates': {'labels': ['DATES:','TRAVEL DATE(s)','DATES'], 'pos': None, 'val': None, 'rows': [3,]},
    'title': {'labels': ['TRAVELER TITLE','TITLE'], 'pos': None, 'val': None, 'rows': [3,]},
    'sponsor': {'labels': ['EVENT SPONSOR','SPONSOR'], 'pos': None, 'val': None, 'rows': [3,]},
    'end': {'labels': ['ENDING DATE   [MM/DD/YYYY]','ENDING DATE [MM/DD/YYYY]'], 'pos': None, 'val': None, 'rows': [3,]},
    
    'source': {'labels': ['BENEFIT SOURCE',], 'pos': None, 'val': None, 'rows': [1,]},
}


def getPos(i,row=-1):
    """
    The layout of the form changes, so keep track of where each column is dynamically
    """
    for header in headers.keys():
        if headers[header]['pos'] == i:
            if row==-1 or not headers[header]['rows']:
                return header
            if row in headers[header]['rows']:
                return header
    return None

def clearPos():
    """
    After finishing one person's record, output the values and clear them
    """
    row = [x['val'] for x in [headers['name'],headers['title'],headers['descrip'],headers['location'],headers['source'],headers['sponsor'],headers['start'],headers['end']]]
    for header in headers.keys():
        headers[header]['pos'] = None
        headers[header]['val'] = None
    
    if row[0]=='John Smith' and row[2]=='Conference on Asia-Pacific Relations': return None #is example
    if row == [None for x in row]: return None
        
    return row
    

    
  
def payments(line):
    """
    The last four columns' headers appear more irregularly, but they're always towards the end, so deal with them separately
    """
    while line[-1]=='': line.pop(-1)
    dollars = line[-1].replace('$','').strip()
    try:
        dollars = float(dollars)
    except:
        return None
    if dollars==0: return None
    if len(line)<8: return None
    i = -4
    while not line[i] or line[i].lower()=='x':
        i = i-1
    values = [x.strip() for x in [line[i].strip(),] + line[-3:]]
    return values    
    
        
    
state = None
state_line = 0

fout = csv.writer(open('processed.csv','w'))
fout.writerow( ['Sheet','url','agency','filed','start_period','end_period', \
    'name','title','descrip','location','source','sponsor','start','end', \
    'benefit', 'check', 'inkind', 'total'] )


fin = csv.reader(open('all.csv','r'))
for line in fin:
    i = 0
    for field in line:
        field = field.strip()
        for header in headers.keys():
            if field in headers[header]['labels']:
                if header=='name':
                    final = clearPos()
                    if final:
                        if not len(thesepayments): 
                            fout.writerow( line[1:7] + final + ['','','',''] )
                        for b in thesepayments:
                            fout.writerow( line[1:7] + final + b )
                    state_line = 1
                    thesepayments = []
                state = 'HEADERS'
                headers[header]['pos'] = i
        i = i+1

    #two columns' values are always shifted to the right compared to the header for some reason
    if state_line==2 and headers['location']['pos'] and not line[headers['location']['pos']]: 
        headers['location']['pos'] = headers['location']['pos'] + 1

    if state_line==4 and headers['dates']['pos'] and not line[headers['dates']['pos']]:
        headers['dates']['pos'] = headers['dates']['pos'] + 1


        
        
    if state=='LISTEN':    
        i = 0
        for field in line:
            field = field.strip()
            if getPos(i, state_line-1) and field:
                if not 'method' in headers[getPos(i, state_line-1)]:
                    headers[getPos(i, state_line-1)]['val'] = field

            i = i+1
 
            
    if state_line in [1,3]:            
        state = 'LISTEN'
    else:
        state = 'WAIT'

    if state_line>0:
        state_line = state_line+1
        
        if payments(line):
            thesepayments.append( payments(line) )
                    
    if state_line > 5:
        state_line = 0
        final = clearPos()
        if final:
            for b in thesepayments:
                fout.writerow( line[1:7] + final + b )
            if not len(thesepayments): 
                fout.writerow( line[1:7] + final + ['','','',''] )
            thesepayments = []

