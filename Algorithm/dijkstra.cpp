//2018063218_ÃÖ¼ºÁø_12838

#include <list>
#include <vector>
#include <queue>
#include <stdio.h>
#pragma warning(disable:4996)

#define INF 9999999

using namespace std;
int N, M;

list<pair<int, int> >* adj;

void addEdge(int x, int y, int w);
int relax(int* v, int u, int w);
void Dijkstra();

int main()
{
    scanf("%d %d", &N, &M);
    adj = new list< pair<int, int> >[N];

    for (int i = 0; i < M; ++i) {
        int x, y, w;
        scanf("%d %d %d", &x, &y, &w);
        addEdge(x - 1, y - 1, w);
    }

    Dijkstra();
    
    delete[] adj;
}

void addEdge(int x, int y, int w)
{
    adj[x].push_back(make_pair(y, w));
}

int relax(int* v, int u, int w) {
    if (*v > u + w) {
        *v = u + w;
        return 1;
    }
    else 
        return 0;
}

void Dijkstra() {
    priority_queue< pair<int, int>, vector <pair<int, int> >, greater<pair<int, int> > > pq;
    vector<int> dist(N, INF);
    int source = 0;
    int ans = 0;
    dist[source] = 0;
    pq.push(make_pair(source, 0));

    while (!pq.empty())
    {
        int find = pq.top().first;
        pq.pop();

        for (list< pair<int, int> >::iterator i = adj[find].begin(); i != adj[find].end(); ++i)
        {
            int adjacency = (*i).first;
            int weight = (*i).second;

            if (relax(&dist[adjacency], dist[find], weight))
                pq.push(make_pair(adjacency, dist[adjacency]));
        }
    }
    for (int i = 0; i < N; ++i)
        ans = dist[i] > ans ? dist[i] : ans;
    printf("%d", ans);
}