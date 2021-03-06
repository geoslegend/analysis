'''
summarise url (s) and other web resources
'''
from newspaper import Article, Config
import sys
CURR_PLATFORM = sys.platform
if CURR_PLATFORM == 'linux':
    pass # fixme: for linux
else:
    sys.path.insert(0, 'U:\Documents\Project\demoapptwitter')
import config

def get_top_img(url):
    '''
    Get just the top img from a URL 
    '''
    article = Article(url)
    
    # configuration for Newspaper to minimize processing time
    configure = Config()
    
    try:
        article.download()

        article.parse()

    except:
        print(url)
        return False
        
    
    return article.top_image
   


def summarise_one(url, title=True, keywords=True, summary=False, \
    top_img_src=False):
    '''
    Get url and return summary 
    '''
    article = Article(url)

    # configuration for Newspaper to minimize processing time
    configure = Config()
    configure.fetch_images = False
    configure.MAX_SUMMARY = 300
    configure.MAX_SUMMARY_SENT = 3
    
    try:
        article.download()
        article.parse()
    except:
        print(url) 

    title = article.title
    if keywords or summary:
        try:
            article.nlp()
            if keywords:
                keywords = article.keywords
            if summary:
                summary = article.summary
        except :
            print('NEwspaper error with nlp() call')
        
    if top_img_src:
        top_img_src = article.top_image
   
    return title, keywords, summary, top_img_src


def summarise_watson_img(src, options=False):
    '''
    IBM Bluemix service
    intersted in default clasifier: images.classifiers.classes 
    '''
    import json
    from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition
    
    classifier = VisualRecognition( '2016-05-20', \
    api_key=config.IBM['credentials']['api_key'])

    result = classifier.classify(images_url=src)
    # debug
    print(json.dumps(result, indent=2))

    return result


def summarise_img(src, options=False):
    '''
    Retrieve meta-data for an image web resource.
    Use algorithmia, openshift or similar cloud service. 
    '''
    import Algorithmia
    client = Algorithmia.client(config.ALGORITHMIA['api_key'])
    algo = client.algo('deeplearning/IllustrationTagger/0.2.3')

    input = {"image":src}
    if options:
        # tags (optional) required probs
        for opt, value in options.items():
            input[opt] = value

        # e.g. threshold  0.3 etc
        
    result = algo.pipe(input)

    return result
    

def get_vec_img():
    # keywords = db.rawtweets.find_one({'img':{'$exists':True}},
    # {'img.keywords':1, '_id':0})

    # retrieves in this format: 
    # { "img" : { "keywords" : [ { "photo" : 0.8888001441955565 }, 
    # { "formal" : 0.651865303516388 }, 
    #keywords
    pass

# for testing use:
if __name__ == '__main__':    
    url = input('Enter URL: ')
    if(url[-3:]) not in ['jpg','png','gif']:
        output = summarise_one(url, False, False, True, True)
        title, keywords, summary, top_img_src = output
        print('title', title)
        print('keywords', keywords)
        if type(summary) is not bool:
            print('summary', summary.encode('utf-8'))
        print('top_img_src', top_img_src)
    else:
        #'threshold':0.1,
        # options = {'tags':[]}
        # options = { 'tags':['tree','window','face','lips', 'sky']}
        output = summarise_watson_img(url)
        #print(output.result)

    

