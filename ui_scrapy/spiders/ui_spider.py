import scrapy

class UISpider(scrapy.Spider):
	name = 'ui_designers'

	def start_requests(self):
		urls = ['http://i.ui.cn/ucenter/1.html']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if 'alert' not in response.body:
			# user exist
			userpad=response.css('div.user-pad')
			work, fans = userpad.css('ul.us-focus strong::text').extract()[:2]
			card = response.css('div.com-card-box')
			name = card.css('ul li.us-name span.n1::text').extract_first().strip()
			email = card.css('li.us-i-l')[1].css('span::text').extract_first('None').strip()
			weibo = card.css('li.us-i-l')[2].css('a::attr(href)').extract_first('None').strip()
			qq = card.css('li.us-i-r')[0].css('span::text').extract_first('None').strip()
			home_page = card.css('li.us-i-r')[1].css('a::text').extract_first('None').strip()
			wechat = card.css('li.us-i-r')[2].css('span::text').extract_first('None').strip()
			row = u','.join([name, fans, work, email, qq, wechat, weibo, home_page]).encode('utf-8').strip()
			# write data to a file
			filename = 'ui_designers.csv'
			with open(filename, 'a') as f:
				f.write(row + '\n')
		else:
			pass

		current_num = int(response.url.split('.')[-2].split('/')[-1])
		if current_num < 10:
			new_url = str(current_num+1) + '.html'
			next_url = response.urljoin(new_url)
			yield scrapy.Request(next_url, self.parse)
