import oauth2client.client
import oauth2client.file
import oauth2client
import webbrowser
import apiclient
import httplib2
import os
import time

# what about api creation process?

# one Google account per blog
class BlogAccount:
    def __init__(self, name, blog_id):
        self.name = name
        self.blog_id = blog_id
        self.client_id = '/client_id_' + name + '.json'
        self.credntials = '/credentials_' + name + '.dat'
        self.service = self.get_service()

    # Return None if fail
    def post_content(self, content, title, labels):
        post_body =  {
            "content": content,
            "title": title,
            "labels": labels
        }
        response = self.service.posts().insert(blogId=self.blog_id,body=post_body).execute()
        return response['url']

    def get_credentials(self):
        """Gets google api credentials, or generates new credentials
        if they don't exist or are invalid."""
        scope = 'https://www.googleapis.com/auth/blogger'
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        flow = oauth2client.client.flow_from_clientsecrets(
            cur_dir + self.client_id,
            scope,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        storage = oauth2client.file.Storage(cur_dir + self.credntials)
        credentials = storage.get()
        if not credentials or credentials.invalid:
            auth_uri = flow.step1_get_authorize_url()
            print("open url")
            print(auth_uri)
            # webbrowser.open(auth_uri)
            auth_code = input('Enter the auth code: ')
            credentials = flow.step2_exchange(auth_code)
            storage.put(credentials)
        return credentials

    def get_service(self):
        """Returns an authorised blogger api service."""
        credentials = self.get_credentials()
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = apiclient.discovery.build('blogger', 'v3', http=http, cache_discovery=False)
        return service

class BlogManager:
    def __init__(self):
        self.topic_map = {}

    def post_content(self, topic, video_object):
        content = video_object.generate_blog_content()
        title = video_object.title
        labels = video_object.tags
        return self.post_content_raw(topic, content, title, labels)

    # post this content in one of the account under this topic
    def post_content_raw(self, topic, content, title, labels):
        blog_accounts = self.topic_map[topic]
        for blog_account in blog_accounts:
            try:
                blog_url = blog_account.post_content(content, title, labels)
                return blog_url
            except Exception as e:
                print(e)
        print("all accounts run out of quota for topic:")
        print(topic)
        return None

blog_manager = BlogManager()
us_problem = BlogAccount("editorialengmm", "6677149013207556017")
blog_manager.topic_map['us_problem'] = [us_problem]

