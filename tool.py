# %%
import pandas as pd
import xml.etree.ElementTree as ET

cols = {'INSTRUMENT':'Components-Instruments',
            'LINE':'Components-Process Lines',
            'MECHANICAL':'Components-Mechanical',
            'VALVE':'Components-Valves',
            'VESSEL':'Components-Vessels',
            'NOZZLE':'Components-Nozzles',
            'MISC':'Components-Miscellaneous',
            'REDUCER':'Components-Reducers',
            }
colstuple = [(k,v) for k, v in cols.items()]
df = pd.DataFrame(colstuple, columns=['tblname','databasename'])

# %% only finding lines that are columns in tbl.
columns = []

f = open('Database.tbl')
data = f.readlines()
for line in data:
    if line.find(']') != -1:
        columns.append(line[1:-2])
print(columns)

# %% 
tables = []
for count, line in enumerate(data):
    if line.find(']') != -1:
        res = (count, line[1:-2])
        tables.append(res)
# %% lines associated to each tablename in the tbl, so it can .join left w.df
linetables = []
for count, line in enumerate(data):
    if line.find(']') != -1:
        res = (count, line[0:-1])
        linetables.append(res)


dffields = pd.DataFrame(columns=['tblname','field'])
a_dict = {}

# %%
for tablenum, tabletuple in enumerate(linetables):
    if tabletuple[1] == '[INSTRUMENT]':
        dffields = dffields.append({'tblname':'INSTRUMENT','field':'FUNCTION_'}, ignore_index=True)
        dffields = dffields.append({'tblname':'INSTRUMENT','field':'LOOP_'}, ignore_index=True)
        dffields = dffields.append({'tblname':'INSTRUMENT','field':'TAG_'}, ignore_index=True)
        continue
    elif tabletuple[1] != '[INSTRUMENT]':
        col = tabletuple[1]
        dffields = dffields.append({'tblname':col[1:-1],'field':'SIZE_'}, ignore_index=True)
        dffields = dffields.append({'tblname':col[1:-1],'field':'SPEC_'}, ignore_index=True)
        dffields = dffields.append({'tblname':col[1:-1],'field':'TAG_'}, ignore_index=True)


# %%
for tablenum, tabletuple in enumerate(linetables[0:-1]):
    for count, line in enumerate(data[linetables[tablenum][0]+1:linetables[tablenum+1][0]-1]):
        col = tabletuple[1]
        {'tblname':col[1:-1],'field':line[6:-1].rsplit(' ')[0]}
        dffields = dffields.append({'tblname':col[1:-1],'field':line[6:-1].rsplit(' ')[0]}, ignore_index=True)
for count, line in enumerate(data[linetables[-1][0]+1:]):
    col = linetables[-1][1]
    dffields = dffields.append({'tblname':col[1:-1],'field':line[6:-1].rsplit(' ')[0]}, ignore_index=True)


# %%
usertables = []
for count, table in enumerate(columns):
    if count > 7:
        usertables.append(table)
# %%
usertablelist = []
for count, table in enumerate(usertables):
    res = (table, 'User'+str(count)+'-'+str(table))
    usertablelist.append(res)
dfuser = pd.DataFrame(usertablelist, columns=['tblname','databasename'])
df = pd.concat([df, dfuser], ignore_index=True)

# %%
df = pd.merge(df, dffields, on ='tblname', how ='inner')
df['Id'] = ''

# %%
tree = ET.parse(".\\Configuration.xml")
root = tree.getroot()

# %%
for datatable in root.iter('DataTable'):
    for field in datatable.iter('Field'):
        df['Id'].loc[(df["databasename"] == datatable.attrib.get('Name')) & (df["field"] == field.attrib.get('Name'))] = field.attrib.get('Id')

# %% TODO - recreating the default views first, then adding keys from the fields.
for datatable in root.iter('DataTable'):
    for table in df['databasename'].unique():
        if datatable.attrib.get('Name') == table:
            for views in datatable.iter('Views'):
                view = ET.SubElement(views, 'View')
                view.set('Name', 'DAT_FILE_IMPORT')
                for vnum in views:
                    if vnum.attrib.get('Name') == 'DAT_FILE_IMPORT':
                        for count, row in enumerate(df['databasename']):
                            if row == table:
                                fieldno = ET.SubElement(vnum, 'Field')
                                fieldno.set('Name', df.iloc[count,2])
                                fieldno.text = df.iloc[count,3]


root.set('xmlns:xs','http://www.w3.org/2001/XMLSchema-instance')                  
tree.write('.\\output\\Configuration.xml', encoding='utf-8', method='xml', xml_declaration=True, short_empty_elements=False)
