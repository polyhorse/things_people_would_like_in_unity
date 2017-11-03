import scrapy


class MySpider(scrapy.Spider):
	name='myspider'
	url_prefix = 'https://answers.unity3d.com'
	start_urls = ['http://answers.unity3d.com/index.html?sort=votes&customPageSize=true&filters=all']
	index = 1
	results = []
	def parse(self, response):
		for question in response.css('div.node-list-item.question-list-item'):
			yield {
			'title':question.css('h4.title a::text').extract_first(),
			'start_date':question.css('div.info p.last-active-user span::attr(title)').extract_first(),
			'votes':question.css('div.counts p.votes span::text').extract_first(),
			'replies':question.css('div.counts p.answers span::text').extract_first(),
			'url':self.url_prefix + question.css('h4.title a::attr(href)').extract_first()

			} 

		if self.index < 100:
			for next_page in response.css('div.pagination ul li.next a'):
				self.index += 1
				yield response.follow(next_page, self.parse)


# scrapy runspider answers_unity.py -o answers.csv -t csv