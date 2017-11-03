import scrapy


class MySpider(scrapy.Spider):
	name='myspider'
	url_prefix = 'https://stackoverflow.com'
	start_urls = ['https://stackoverflow.com/questions/tagged/unity3d?page=1&sort=votes&pagesize=50']
	url_template = 'https://stackoverflow.com/questions/tagged/unity3d?page=%s&sort=votes&pagesize=50'
	index = 1
	results = []
	def parse(self, response):
		for question in response.css('.question-summary'):
			yield {
			'title':question.css('.summary h3 a ::text').extract_first(),
			'excerpt':question.css('.summary div.excerpt ::text').extract_first(),
			'start_date':question.css('.summary div.started span::attr(title)').extract_first(),
			'views':question.css('.statscontainer div.views::attr(title)').extract_first().split(' ')[0],
			'answers':question.css('.statscontainer div.status strong::text').extract_first(),
			'votes':question.css('.statscontainer div.votes strong::text').extract_first(),
			'url':self.url_prefix + question.css('.summary h3 a::attr(href)').extract_first()

			} 

		if self.index < 50:
			self.index += 1
			yield response.follow(self.url_template % self.index, self.parse)

# scrapy runspider stackoverflow.py -o stackoverflow.csv -t csv