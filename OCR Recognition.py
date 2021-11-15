#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import PDFObjectNotFound
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
base_path = "D:\plagfiles"
password = ""
extracted_text = ""
for file in os.listdir(base_path):
    if file.endswith(".pdf"):
        fp = open(base_path+file, "rb")
        parser = PDFParser(fp)
        document = PDFDocument(parser, password)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    extracted_text += lt_obj.get_text()


            txtfile = open(base_path+file[:-4]+".txt",'w')
            with open(base_path+file[:-4]+".txt", "wb") as my_log:
                my_log.write(extracted_text.encode("utf-8"))
                extracted_text = ""
            fp.close()


# In[ ]:
