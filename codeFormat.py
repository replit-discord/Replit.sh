from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import requests

def hilite_me(code, lexer, options, style, linenos, divstyles):
	lexer = lexer or 'python'
	style = 'monokai'
	defstyles = 'overflow:auto;width:auto;'

	formatter = HtmlFormatter(style=style,
							  linenos=False,
							  noclasses=True,
							  cssclass='',
							  cssstyles=defstyles + divstyles,
							  prestyles='margin: 0')
	html = highlight(code, get_lexer_by_name(lexer, **options), formatter)
	if linenos:
		html = insert_line_numbers(html)
	html = html.replace("<div", "<body")
	html = html.replace("</div>", "</body>")
	return html

def get_default_style():
	return 'background: #101427; overflow:auto;width:auto;'

def insert_line_numbers(html):
	match = re.search('(<pre[^>]*>)(.*)(</pre>)', html, re.DOTALL)
	if not match: return html

	pre_open = match.group(1)
	pre = match.group(2)
	pre_close = match.group(3)

	html = html.replace(pre_close, '</pre></td></tr></table>')
	numbers = range(1, pre.count('\n') + 1)
	format = '%' + str(len(str(numbers[-1]))) + 'i'
	lines = '\n'.join(format % i for i in numbers)
	html = html.replace(pre_open, '<table><tr><td>' + pre_open + lines + '</pre></td><td>' + pre_open)
	return html

def getLang(url):
	r = requests.get(url)
	content = str(r.content)
	indexStart = content.index("Language:") + 9
	indexEnd = content.index('"', indexStart)
	language = content[indexStart:indexEnd]
	return language