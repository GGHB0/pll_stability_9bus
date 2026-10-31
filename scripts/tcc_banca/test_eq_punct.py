import xml.etree.ElementTree as ET

xml_snippet = '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:oMathPara><m:oMath><m:r><m:t>x=1</m:t></m:r><m:r><w:rPr><w:color w:val="FF0000"/></w:rPr><m:t>.</m:t></m:r></m:oMath></m:oMathPara></w:p>'
tree = ET.fromstring(xml_snippet)
print('Valid XML:', ET.tostring(tree).decode('utf-8'))

