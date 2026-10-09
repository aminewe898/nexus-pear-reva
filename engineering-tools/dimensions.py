from pypdf import PdfReader
for n in ['buttons','inductor','gh','efuse','nor']:
 r=PdfReader('work/'+n+'.pdf')
 for i,p in enumerate(r.pages):
  t=p.extract_text() or ''
  if (n=='buttons' and 'B3F-1000,' in t) or (n=='inductor' and 'Product Dimensions' in t):print(n,i,t[-4500:])
