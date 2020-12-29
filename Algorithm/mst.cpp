//2018063218_ÃÖ¼ºÁø_12838

#include <stdio.h>
#include <stdlib.h>
#pragma warning(disable:4996)

typedef struct Edge {
    int f, t, w;
}Edge;

typedef struct vertice {
    int parent, rank;
}vertice;

int N, M;
Edge* edge;
Edge result[1001];
vertice ver[1001];

void makeGraph(int E);
void swap(Edge* a, Edge* b);
void Union(int p, int q);
int find(int i);
void sort(int low, int high);
int partition(int low, int high);
void MST_KRUSKAL();

int main()
{
    scanf("%d %d", &N, &M);

    makeGraph(M);

    for (int i = 0; i < M; i++) {
        int from, to, weight;
        scanf("%d %d %d", &from, &to, &weight);
        edge[i].f = from - 1;
        edge[i].t = to - 1;
        edge[i].w = weight;
    }

    sort(0, M - 1);

    MST_KRUSKAL();

    delete edge;
}

void makeGraph(int E) {
    edge = new Edge[E];
}

void swap(Edge* a, Edge* b)
{
    Edge temp = *a;
    *a = *b;
    *b = temp;
}

void Union(int p, int q)
{
    int proot = find(p);
    int qroot = find(q);

    if (ver[proot].rank < ver[qroot].rank)
        ver[proot].parent = qroot;
    else if (ver[proot].rank > ver[qroot].rank)
        ver[qroot].parent = proot;
    else
    {
        ver[qroot].parent = proot;
        ver[proot].rank++;
    }
}

int find(int i)
{
    if (ver[i].parent != i)
        ver[i].parent = find(ver[i].parent);
    return ver[i].parent;
}

void sort(int low, int high)
{
    if (low < high)
    {
        int pi = partition(low, high);
        sort(low, pi - 1);
        sort(pi + 1, high);
    }
}

int partition(int low, int high)
{
    int i = low - 1;
    Edge pivot = edge[high];

    for (int j = low; j <= high - 1; j++)
    {
        if (edge[j].w < pivot.w || (edge[j].w == pivot.w && edge[j].f < pivot.f) ||
            (edge[j].w == pivot.w && edge[j].f == pivot.f && edge[j].t < pivot.t))
        {
            i++;
            swap(&edge[i], &edge[j]);
        }
    }
    swap(&edge[i + 1], &edge[high]);
    return (i + 1);
}

void MST_KRUSKAL()
{
    int e = 0;
    int i = 0;

    for (int v = 0; v < N; ++v) {
        ver[v].parent = v;
        ver[v].rank = 0;
    }

    while (e < N - 1 && i < M) {
        Edge resEdge = edge[i++];
        int p = find(resEdge.f);
        int q = find(resEdge.t);

        if (p != q) {
            result[e++] = resEdge;
            Union(p, q);
        }
    }
    printf("%d\n", e);

    for (i = 0; i < e; ++i)
    {
        printf("%d %d %d\n", result[i].f + 1, result[i].t + 1, result[i].w);
    }
    return;
}