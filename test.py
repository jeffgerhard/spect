# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 09:48:40 2016

@author: gerhardj
"""

import markdown as m
from tkinter.filedialog import askopenfilename


fname = askopenfilename(title='pick a md file',
                        initialdir='C:\\Users\\gerhardj\\Desktop\\')
md = m.Markdown(extensions=['meta', 'smarty'])

with open(fname, mode='r', encoding='utf-8') as f:
    text = f.read()

print(md.convert(text))
print(md.Meta)
#meta = md.Meta
#print(meta)