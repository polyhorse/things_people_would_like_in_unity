import scrapy


class MySpider(scrapy.Spider):
	name='myspider'
	url_prefix = 'https://feedback.unity3d.com'
	start_urls = ['https://feedback.unity3d.com/forums/unity/suggestions?utf8=%E2%9C%93&status=&category=&view=most_voted']
	index = 1
	results = []
	def parse(self, response):
		for question in response.css('div.g12.nest.idea.rel'):
			yield {
			'title':question.css('h4.mb0 a::text').extract_first(),
			'excerpt':question.css('p.bulk.mb0.clear::text').extract_first(),
			'start_date':question.css('div.meta p.left.mr5.cl::text').extract()[1],
			'votes':question.css('div.count.b::text').extract_first(),
			'status':question.css('div.status div::text').extract_first(),
			'url':self.url_prefix + question.css('h4.mb0 a::attr(href)').extract_first()

			} 

		if self.index < 100:
			for next_page in response.css('div.pagination a.next_page'):
				self.index += 1
				yield response.follow(next_page, self.parse)


# scrapy runspider feedback_unity.py -o feedback.csv -t csv