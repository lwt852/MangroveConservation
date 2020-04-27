import datetime
import lxml.etree as etree
"""
Created on Sat Mar 21 20:43:58 2020
@author: Mimi Gong
A function to build networks into gexf file and explore in Gephi."""
def create_gexf(tweets, filename):
    """
    build the data into gexf file and load it into gephi for network analysis.
    reference: https://lucahammer.com/2019/11/05/creating-a-retweet-network-for-gephi-from-a-local-file-with-python/
    """
    attr_qname = etree.QName(
        "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")

    gexf = etree.Element('gexf',
                         {attr_qname: 'http://www.gexf.net/1.3draft  http://www.gexf.net/1.3draft/gexf.xsd'},
                         nsmap={
                             None: 'http://graphml.graphdrawing.org/xmlns/graphml'},
                         version='1.3')

    graph = etree.SubElement(gexf,
                             'graph',
                             defaultedgetype='directed',
                             mode='dynamic',
                             timeformat='datetime')
    attributes = etree.SubElement(
        graph, 'attributes', {'class': 'node', 'mode': 'static'})
    etree.SubElement(attributes, 'attribute', {
                     'id': 'user_location', 'title': 'user_location', 'type': 'string'})
    etree.SubElement(attributes, 'attribute', {
                     'id': 'user_bio', 'title': 'user_bio', 'type': 'string'})
    etree.SubElement(attributes, 'attribute', {
                     'id': 'year', 'title': 'year', 'type': 'integer'})
    etree.SubElement(attributes, 'attribute', {
                     'id': 'follower_count', 'title': 'follower_count', 'type': 'integer'})

    nodes = etree.SubElement(graph, 'nodes')
    edges = etree.SubElement(graph, 'edges')

    for tweet in reversed(tweets):
        node = etree.SubElement(nodes,
                                'node',
                                id=tweet['id'],
                                Label=tweet['username'],
                                start=datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y').isoformat(
                                    timespec='seconds'),  # Fri Jul 27 07:52:57 +0000 2018
                                end=(datetime.datetime.strptime(
                                    tweet['created_at'], '%a %b %d %X %z %Y') + datetime.timedelta(seconds=1)).isoformat(timespec='seconds')
                                )
        attvalues = etree.SubElement(node, 'attvalues')
        etree.SubElement(attvalues,
                         'attvalue',
                         {'for': 'year',
                          'value': tweet['user_joined']
                          }
                         )
#        if 'user_location' in tweet:
#            etree.SubElement(attvalues,
#                             'attvalue',
#                             {'for': 'user_location',
#                              'value': tweet['user_location']
#                              }
#                             ) 
        if 'user_bio' in tweet:
            etree.SubElement(attvalues,
                             'attvalue',
                             {'for': 'user_bio',
                              'value': tweet['user_bio']
                              }
                         )            
        if 'follower_count' in tweet:
            etree.SubElement(attvalues,
                             'attvalue',
                             {'for': 'follower_count',
                              'value': tweet['follower_count']
                              }
                             )

        if 'retweeted_user' in tweet:
            etree.SubElement(edges,
                             'edge',
                             {'id': tweet['id'],
                              'source': tweet['retweeted_user']['user_id'],
                              'target': tweet['user_id'],
                              # Fri Jul 27 07:52:57 +0000 2018
                              'start': datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y').isoformat(timespec='seconds'),
                              'end': (datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y') + datetime.timedelta(seconds=1)).isoformat(timespec='seconds')
                              }
                             )
            node = etree.SubElement(nodes,
                                    'node',
                                    id=tweet['retweeted_user']['user_id'],
                                    Label=tweet['retweeted_user']['username'],
                                    start=datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y').isoformat(
                                        timespec='seconds'),  # Fri Jul 27 07:52:57 +0000 2018
                                    end=(datetime.datetime.strptime(
                                        tweet['created_at'], '%a %b %d %X %z %Y') + datetime.timedelta(seconds=1)).isoformat(timespec='seconds')
                                    )
            attvalues = etree.SubElement(node, 'attvalues')
            etree.SubElement(attvalues,
                             'attvalue',
                             {'for': 'year',
                              'value': tweet['retweeted_user']['user_joined']
                              }
                             )
            if 'user_location' in tweet:
                etree.SubElement(attvalues,
                                 'attvalue',
                                 {'for': 'user_location',
                                  'value': tweet['user_location']
                                  }
                                 ) 
            if 'user_bio' in tweet:
                etree.SubElement(attvalues,
                                 'attvalue',
                                 {'for': 'user_bio',
                                  'value': tweet['user_bio']
                                  }
                                 )            
            if 'follower_count' in tweet:
                etree.SubElement(attvalues,
                                 'attvalue',
                                 {'for': 'follower_count',
                                  'value': tweet['follower_count']
                                  }
                                 )            

    with open(filename, 'w', encoding='utf-8')as f:
        f.write(etree.tostring(gexf, encoding='utf8',
                               method='xml').decode('utf-8'))
    print('Created gexf.')




