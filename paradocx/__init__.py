from paradocx.util import w
from paradocx.package import WordPackage

class Document(WordPackage):
	def paragraph(self, text=None, style=None):
		p = paragraph(text, style=style)
		self.start_part.append(p)
		return p

	def table(self, data=None):
		tbl = table(data)
		self.start_part.append(tbl)
		return tbl

	@property
	def paragraphs(self):
		return self.start_part.body.findall(w['p'])

	@property
	def data(self):
		return self.start_part.data

def run(text=None, bold=False, italic=False, font=None):
	rPr = w.rPr()
	if bold:
		rPr.append(w.b())
	if italic:
		rPr.append(w.i())
	if font:
		rFont = w.rFont()
		rFont.attrib[w['ascii']] = font
		rPr.append(rFont)
	r = w.r()
	if len(rPr):
		r.append(rPr)
	if text:
		r.append(w.t(unicode(text)))
	return r

def paragraph(text=None, style=None, pagebreak=None):
	p = w.p()
	subs = []
	pPr = w.pPr()
	if style:
		s = w.pStyle()
		s.attrib[w['val']] = style
		pPr.append(s)
	if pagebreak:
		pPr.append(
			w.sectPr()
		)
	if len(pPr):
		subs.append(pPr)
	if text:
		if isinstance(text, basestring):
			text = unicode(text)
			subs.append(
				w.r(
					w.t(text)
				)
			)
		elif hasattr(text, 'tag'):
			subs.append(text)
	p.extend(subs)
	return p

def table(data=None):
	tbl = w.tbl()
	data = data or []
	for cells in data:
		tbl.append(
			w.tr(
				*[w.tc(paragraph(value)) for value in cells]
			)
		)
	return tbl
	
