import requests
import http.cookiejar
from lxml import etree


class PixivLogin(object):
	def __init__(self):
		self.headers={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch, br',
		'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
		}
		self.get_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
		self.login_url='https://accounts.pixiv.net/api/login?lang=zh'
		self.bookmark_url='https://www.pixiv.net/bookmark.php'
		self.session = requests.Session()
		self.session.cookies = http.cookiejar.LWPCookieJar(filename='pixiv_cookies')

	def loadcookie(self):
		try:
			self.session.cookies.load(ignore_discard=True)
		except:
			print('cookie 保存失败')

	def get_key(self):
		reponse = self.session.get(self.get_url,headers=self.headers)
		selector = etree.HTML(reponse.text)
		post_key = selector.xpath('//form/input[1]/@value')
		print(post_key)
		return post_key

	def post_value(self,email,password):
		self.data ={
		'pixiv_id':email,
		'password':password,
		'captcha':'',
		'g_recaptcha_response':'',
		'post_key': self.get_key()[0],
		'source':'pc',
		'ref':'wwwtop_accounts_index',
		'return_to':'http://www.pixiv.net/'
		}
		reponse=self.session.post(self.login_url,data=self.data,headers=self.headers)
		print(reponse.status_code)
		self.session.cookies.save()

	def book(self):
		reponse = self.session.get(self.bookmark_url,headers=self.headers)
		print(reponse.status_code)
		selector = etree.HTML(reponse.text)
		photolist = selector.xpath('//li/a/@href')
		print(photolist)

if __name__ == "__main__":
	Pixiv = PixivLogin()
	Pixiv.post_value(email='example@mail.com',password='password')
	Pixiv.book()
