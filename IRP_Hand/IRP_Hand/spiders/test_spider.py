
# coding: utf-8

# In[7]:


from scrapy.selector import Selector
from scrapy import http
import scrapy
import re


# = Note For Other Readers
### = Note For Me 

#Every Class in this file represents a Spider
#Every Spider must subclass 'scrapy.Spider'
class NewspaperSpider(scrapy.Spider):
    
    #import to give each spider a name because you run spiders by calling them by name.
    name = 'newspapers_tt'
    
    #Important thing I noticed: (See Below)
    def start_requests(self):
        
        start_url = "https://en.wikipedia.org/wiki/List_of_newspapers_in_the_United_States"
        #Only yielded pages are downloaded (i.e. parseable)
        yield scrapy.Request(url=start_url, callback=self.parse1)
    
    #Parse the base wiki page for links to wiki of top 25 national papers 
    def parse1(self, response):
        to_links = response.xpath('//*[@id="mw-content-text"]/div//table[3]/tr//td[2]//a/@href').extract()
        top_urls = [ response.urljoin(link) for link in to_links]
        
        ### Relative Links: response.xpath('//*[@id="mw-content-text"]/div//table[3]/tr//td[2]//a/@href').extract()
        ### Titles: response.xpath('//*[@id="mw-content-text"]/div//table[3]/tr//td[2]//a/@title').extract()
        
        for url in top_urls:
            yield scrapy.Request(url=url, callback=self.parse2)
    
    def parse2(self, response):
        h = response.xpath('//*[@id="firstHeading"]/i/text()').extract()[0]
        
        ###TO-DO: Check to see if there is more than one  website link.
        sup_link1 = response.xpath('//table[@class="infobox vcard"]/tr[last() -1]//a/@href').extract()[0]
        sup_link2 = response.xpath('//table[@class="infobox vcard"]/tr[last()]//a/@href').extract()[0]
        
        if '.com' not in sup_link1:
            site = sup_link2
        
        else:
            site = sup_link1
        
        yield scrapy.Request(url=site, callback=self.parse3)
        
    
    def parse3(self, response):
        all_links = response.xpath('/html/body//a/@href').extract()
        sports_pages = [link for link in all_links if re.search('[Ss]ports', link) is not None]
        p_title = response.xpath('//title/text()').extract()[0]
        #Not Necessarily true, but is a pretty safe assumption.
        sports_home = sports_pages[0]
        
        
        yield {
            
            p_title : sports_home
        
        }
        
        

                


# In[ ]:


#wiw = [link for link in p_links if re.search('[Ss]ports', link) is not None]
#p_links = response.xpath('/html/body//a/@href').extract()



        ### g_url = 'https://www.google.com/search?q=' +  +'&num=100&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a&channel=fflb
###         yield {
            
###             h : site
            
###         }



# <figure id="media-100000005332419" class="media photo lede layout-large-horizontal" data-media-action="modal" itemprop="associatedMedia" itemscope="" itemid="https://static01.nyt.com/images/2017/08/02/sports/02yankees1/02yankees1-master768.jpg" itemtype="http://schema.org/ImageObject" aria-label="media" role="group">
#     <span class="visually-hidden">Photo</span>
#     <div class="image">
#             <img src="https://static01.nyt.com/images/2017/08/02/sports/02yankees1/02yankees1-master768.jpg" alt="" class="media-viewer-candidate" data-mediaviewer-src="https://static01.nyt.com/images/2017/08/02/sports/02yankees1/02yankees1-superJumbo.jpg" data-mediaviewer-caption="Starting pitcher Jaime Garcia, at a news conference Tuesday, said that growing up, he was a Yankees fan." data-mediaviewer-credit="Kathy Willens/Associated Press" itemprop="url" itemid="https://static01.nyt.com/images/2017/08/02/sports/02yankees1/02yankees1-master768.jpg"><div class="media-action-overlay">
# <i class="icon sprite-icon"></i>
# </div>
#             <meta itemprop="height" content="512">
#             <meta itemprop="width" content="768">
#     </div>
#         <figcaption class="caption" itemprop="caption description">
#                 <span class="caption-text">Starting pitcher Jaime Garcia, at a news conference Tuesday, said that growing up, he was a Yankees fan.</span>
#                         <span class="credit" itemprop="copyrightHolder">
#             <span class="visually-hidden">Credit</span>
#             Kathy Willens/Associated Press        </span>
#             </figcaption>
#     </figure>

# <span class="credit" itemprop="copyrightHolder">
#             <span class="visually-hidden">Credit</span>
#             Kathy Willens/Associated Press        </span>


# In[8]:





# In[ ]:



