import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import style
import gensim
from pymystem3 import Mystem
from networkx.algorithms import community
import random

def loadModel():
    f = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
    model = gensim.models.KeyedVectors.load_word2vec_format(f, binary=True)
    return model

def getWord(word):
    m = Mystem()
    l = m.analyze(word.strip())
    gr = l[0]['analysis'][0]['gr']
    return l[0]['analysis'][0]['lex'] + "_" + gr.split('=')[0].split(',')[0]

def searchInModel(model, word):
    neib = []
    if word in model:
        for i in model.most_similar(positive=[word], topn=10):
            if i[1] >= 0.5:
                neib.append(i)
    else:
        pass
    return neib

def visualize(G, d):
    global headkeys
    style.use('ggplot')
    plt.figure(figsize=(10, 10))
    plt.tight_layout()
    # для начала надо выбрать способ "укладки" графа. Их много, возьмём для начала такой:
    pos=nx.spring_layout(G)
    #nx.draw_networkx_nodes(G, pos, nodelist=res, node_color='green', node_size=400)
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=100)
    nx.draw_networkx_edges(G, pos, edge_color='#c2d7f9')
    nx.draw_networkx_nodes(G, pos, nodelist=d.keys(), node_color=d.values(), node_size = 100)
    nx.draw_networkx_nodes(G, pos, nodelist=headkeys, node_color='red', node_size=300)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='Arial')
    plt.axis('off') # по умолчанию график будет снабжён осями с координатами, здесь они бессмысленны, так что отключаем
    plt.savefig("./static/figure.png")

def analyzeGraph(G):
    s = ""
    s += "Радиус графа: " + str(nx.radius(G)) + "<br/>"
    s += "Диаметр графа: " + str(nx.diameter(G)) + "<br/>"
    s += "Коэффициент ассортативности: " + str(nx.degree_pearson_correlation_coefficient(G)) + "<br/>"
    s += "Плотность графа: " + str(nx.density(G)) + "<br/>"
    s += "Коэффициент кластеризации: " + str(nx.average_clustering(G)) + "<br/>"
    return s

def getCenrality(G):
    # Центральность узлов (важность узлов)
    deg = nx.degree_centrality(G)
    s = "Degree centrality: "
    for nodeid in sorted(deg, key=deg.get, reverse=True)[:5]:
        s += nodeid + "; "
    return s + "<br/>"

def getBetweenness(G):
    btw = nx.betweenness_centrality(G)
    s = "Betweenness centrality: "
    for nodeid in sorted(btw, key=btw.get, reverse=True)[:5]:
        s += nodeid + "; "
    return s + "<br/>"

def getCloseness(G):
    global headkeys
    headkeys = []
    gls = nx.closeness_centrality(G)
    s = "Closeness centrality: "
    for nodeid in sorted(gls, key=gls.get, reverse=True)[:5]:
        s += nodeid + "; "
        headkeys.append(nodeid)
    return s + "<br/>"

def getEigenvector(G):
    eig = nx.eigenvector_centrality(G)
    s = "Eigenvector centrality: "
    for nodeid in sorted(eig, key=eig.get, reverse=True)[:5]:
        s += nodeid + "; "
    return s + "<br/>"

def getCommunities(G):
    colors = ['#ef743e', '#efd43e', '#c7ef3e', '#89ef3e', '#3eefb3', '#3ea2ef','#FDFDB0','#DE1A93',\
              '#2A4E73','#60C7C0','#9F2877','#B64A30','#B1ECC7','#0E25CA']
    d = {}
    com = community.greedy_modularity_communities(G)
    for c in com:
        color = colors[random.randint(0, 13)]
        for el in list(c):
            d[el] = color
    return d

def mainFunc(res):
    global model, G
    model = loadModel()
    G = nx.Graph()
    txt = ""
    for w in res:
        txt += w + "<br>" + processGraph(w) + "<br>"
    txt += "Цветами выделены сообщества, крупными точками - узлы, выбранные по характеристике Closeness centrality." + "<br><br>"
    return txt

def processGraph(w):
    global model, G
    word = getWord(w.strip())
    l = searchInModel(model, word)
    #G = nx.Graph()
    G.add_node(word)
    #sizes = [400]
    for n, w in l:
        G.add_node(n)
        #sizes.append(200)
        G.add_edge(word, n, weight=w)
        l1 = searchInModel(model, n)
        for n1, w1 in l1:
            G.add_node(n1)
            #sizes.append(50)
            G.add_edge(n, n1, weight=w1)
    nx.write_gexf(G, 'graph_file.gexf')
    s = analyzeGraph(G)
    s += getCenrality(G)
    s += getBetweenness(G)
    s += getCloseness(G)
    s += getEigenvector(G)
    d = getCommunities(G)
    visualize(G, d)
    return s
