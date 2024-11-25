import pandas as pd
import PIthon
import ptattr
# this is a simple progam that demonstrates accessing pi data via the PI AFSDK and the common language runtime (CLR)
# python package (pythonnet). To run this make sure the AF SDK is installed on your computer. The installation is downloadable from
# AVEVA. It will also be installed with AVEVA Apps like the PI System Explorer. This example App also assumes you have
# WINS windows integrated security setup to automatically do the authentication to your PI Server. Note that the PI Server
# URL is hard coded below. Use any AVEVA App, like PI System Explorer to add the PI Server, if needed, to your known
# servers table (KST). The path to the OSIsoft assemblies has to be correct in PIthon.py.
# pip install pythonnet

def run_examples():
    piserverURL = 'localhost'
    PIthon.connect_to_Server(piserverURL)
    print(f'connected to {piserverURL}')

    tagname = 'sinusoid'
    snapshot = PIthon.get_tag_snapshot(tagname)
    print(f'{tagname} snapshot: {snapshot[0]}, {snapshot[1]}')

    ptSource = 'R'
    points = PIthon.get_tags_ptsource(ptSource)
    for pt in points:
        print(f'{pt.GetAttribute(ptattr.attrs[22])} {pt.GetAttribute(ptattr.attrs[6])}')
    points = PIthon.get_tags_ptsource(ptSource) # for some reason the points object is destroyed after iterating thruogh it, so get it again
    dataDictionary = PIthon.points_archive_report(points)
    # this is a dictionary of lists, each list  is the archive data for one of the tags
    # there may be a better strategy for converting the archive values to a dictionary; I started with the list approach
    for key,value in dataDictionary.items():
        print(key)
        if len(value) <= 0:
            print("no data")
            continue
        df = pd.DataFrame(value)
        print(df)







if __name__ == '__main__':
    print('Starting pithonExample')


    try:
        run_examples()
    except Exception as ex:
        print(f'PIthon Example Error {ex}')



    print('Completed pithonExamples')








