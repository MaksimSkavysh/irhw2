import json
import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(G):
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


def add_nodes_to_graph(G, data):
    for node in data:
        G.add_node(node['url'], name=node['name'], description=node['description'])


def add_links_to_graph(G, data):
    for node in data:
        outgoing_urls = node['outgoing_urls']
        for outgoing_url in outgoing_urls:
            if outgoing_url.startswith('/wiki/'):
                if G.has_node(outgoing_url):
                    G.add_edge(node['url'], outgoing_url)
                    # print('link:', node['url'], ' ->->-> ', outgoing_url)


def plot_graph_degree_hist(G):
    plt.figure(1)
    data = nx.degree_histogram(G)
    plt.hist(data, bins=50, log=True,  density=True, histtype='bar')
    plt.title("Histogram of nodes degrees")
    plt.xlabel("Degree")
    plt.ylabel("Frequency (log)")


def get_top_10(G, alpha=0.85):
    pr = nx.pagerank(G, alpha)
    pr_list = []
    for key in pr:
        pr_list.append((key, pr[key]))
    sorted_pr_list = sorted(pr_list, key=lambda tup: -tup[1])
    return sorted_pr_list[:11]


def get_HITS_top_10(G):
    h, a = nx.hits(G, max_iter=49, tol=1e-06)
    ha_list = []
    for key in h:
        ha_list.append((key, h[key], a[key]))

    sorted_h = sorted(ha_list, key=lambda tup: -tup[1])
    sorted_a = sorted(ha_list, key=lambda tup: -tup[2])
    sorted_ha = sorted(ha_list, key=lambda tup: (-tup[2]-tup[1])/2)
    return sorted_h[:11], sorted_a[:11], sorted_ha[:11]


def main():
    G = nx.DiGraph()
    data = json.load(open('./wiki.json'))
    print('Number of pages:', len(data))
    for node in data:
        node['url'] = node['url'].replace('https://en.wikipedia.org', '')

    add_nodes_to_graph(G, data)
    add_links_to_graph(G, data)

    top10 = get_top_10(G)

    print('\nTop 10 default page rank pages:')
    titles = nx.get_node_attributes(G, 'name')
    descriptions = nx.get_node_attributes(G, 'description')
    for i in range(1, 11):
        print('\n', i)
        print(titles[top10[i][0]], top10[i][1])
        print('https://en.wikipedia.org' + top10[i][0])
        print(descriptions[top10[i][0]])

    for alpha in [0.95, 0.85, 0.5, 0.3]:
        print('\nPageRank with alpha =', alpha)
        top_10 = [tup[0] for tup in get_top_10(G, alpha)]
        print(top_10)

    top_h, top_a, top_ha = get_HITS_top_10(G)
    print('\nTop HIST with hubs sort:')
    print(top_h)
    print([top[0] for top in top_h])
    print('\nTop HIST with authorities sort:')
    print([top[0] for top in top_a])
    print('\nTop HIST with mean sort:')
    print([top[0] for top in top_ha])


    plot_graph_degree_hist(G)
    plt.show()

main()
