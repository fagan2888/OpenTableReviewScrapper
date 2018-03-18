import scrapy

class ReviewsSpider(scrapy.Spider):
	name = "reviews"

	base_url = "https://www.opentable.com"

	start_urls = ['https://www.opentable.com/charlotte-north-carolina-restaurant-listings']

	restaurant_list = []

	index = 0

	page = 1

	def extract_data(self, response):

		restaurant_url = self.restaurant_list[self.index]

		for reviewContainer in response.css('div.reviewBodyContainer'):
			# print reviewContainer.css('p::text').extract_first()
			yield {
				'review': reviewContainer.css('p::text').extract_first()
			}

		next_page = response.css('div.reviewUpdateParameter[data-value="' + str(self.page + 1) + '"]').extract_first()

		if next_page and self.page <= 10:
			self.page += 1
			print "Page: " + str(self.page)
			yield scrapy.Request(response.urljoin(restaurant_url + "?page=" + str(self.page)), callback=self.extract_data)
		elif len(self.restaurant_list) > 0:
			self.index += 1
			self.page = 1
			restaurant_url = self.restaurant_list[self.index]
			print restaurant_url
			yield scrapy.Request(response.urljoin(restaurant_url), callback=self.extract_data)

	def parse(self, response):

		for restaurant in response.css('div.result.content-section-list-row'):
			# rest-row-name rest-name 

			restaurant_link = self.base_url + restaurant.css('a.rest-row-name.rest-name::attr(href)').extract_first()

			self.restaurant_list.append(restaurant_link)

		restaurant_url = self.restaurant_list[self.index]

		print restaurant_url

		yield scrapy.Request(response.urljoin(restaurant_url), callback=self.extract_data)