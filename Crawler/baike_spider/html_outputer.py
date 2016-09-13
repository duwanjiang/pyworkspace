# coding:utf8
class HtmlOutputer(object):
    def __init__(self):
        self.datas = []


    def collect_data(self,data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        font = open('output.html','w')
        font.write('<html>')
        font.write('<body>')
        font.write('<table>')

        #ascii
        for data in self.datas:
            font.write('<tr>')
            font.write('<td>%s</td>' % data['url'])
            font.write('<td>%s</td>' % data['title'].encode('utf-8'))
            font.write('<td>%s</td>' % data['summary'].encode('utf-8'))
            font.write('</tr>')

        font.write('</table>')
        font.write('</body>')
        font.write('</html>')

        font.close()
