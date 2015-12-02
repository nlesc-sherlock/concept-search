#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################

# Convert the Enron Mails to a Document Corpus in JSON

import json
import sys
import os

def convertToDC(inputDir):
    data_dir = os.path.join(inputDir, 'enron_mail_clean')
    dump_dir = os.path.join(inputDir, 'enron_email_clean_json')
    
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    
    for person in os.listdir(data_dir):
        with open(os.path.join(dump_dir, person), 'w') as out_file:
            document_dir = os.path.join(data_dir, person, 'all_documents')
            for doc in os.listdir(document_dir):
                with open(os.path.join(document_dir, doc), 'r') as f:
                    text = f.read()
                a = { 'index' : { '_index' : 'enron', '_type' : 'email', '_id': '{}/{}'.format(person, doc)} }
                out_file.write(json.dumps(a))
                out_file.write('\n')
        
                d = {'text': text}
                out_file.write(json.dumps(d))
                out_file.write('\n')
            
if __name__ == '__main__':
    convertToDC(sys.argv[1])
