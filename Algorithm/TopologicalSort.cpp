//2018063218_ÃÖ¼ºÁø_12838

#include <stdio.h>
#include <stdlib.h>
#include <list>
#include <stack>

#define WHITE 0
#define BLACK 1

#pragma warning(disable:4996)
using namespace std;

int N, M;
list<int>* ver;
stack<int> Stack;
bool visit[1000];

void makeGraph(int n);
void makeEdge(int from, int to);
bool DAG();
void Topological();
void TopoIter(int i, bool visit[]);
bool DAGIter(int i, bool visit[], bool* fin);

int main()
{
    scanf("%d %d", &N, &M);
    makeGraph(N);
    for (int i = 0; i < M; ++i) {
        int from, to;
        scanf("%d %d", &from, &to);
        from--; to--;
        makeEdge(from, to);
    }

    if (DAG()) {
        printf("1\n");
        Topological();
    }
    else {
        printf("0\n");
    }
}

void makeGraph(int n) {
    ver = new list<int>[N];
}

void makeEdge(int from, int to) {
    ver[from].push_back(to);
}

void Topological() {
    for (int i = 0; i < N; ++i)
        visit[i] = WHITE;

    for (int i = 0; i < N; ++i)
        if (visit[i] == WHITE)
            TopoIter(i, visit);

    while (Stack.empty() == WHITE) {
        printf("%d ", Stack.top() + 1);
        Stack.pop();
    }
}
void TopoIter(int i, bool visit[]) {
    visit[i] = BLACK;
    ver[i].sort();

    list<int>::iterator j;
    for (j = ver[i].begin(); j != ver[i].end(); ++j)
        if (!visit[*j])
            TopoIter(*j, visit);
    Stack.push(i);
}

bool DAG() {
    bool* visit = new bool[N];
    bool* fin = new bool[N];
    for (int i = 0; i < N; ++i)
    {
        visit[i] = WHITE;
        fin[i] = WHITE;
    }
    for (int i = 0; i < N; ++i)
        if (DAGIter(i, visit, fin))
            return WHITE;
    
    delete[] visit;
    delete[] fin;
    
    return BLACK;
}

bool DAGIter(int i, bool visit[], bool* fin) {
    if (visit[i] == WHITE)
    {
        visit[i] = BLACK;
        fin[i] = BLACK;
        list<int>::iterator j;
        for (j = ver[i].begin(); j != ver[i].end(); ++j)
        {
            if (!visit[*j] && DAGIter(*j, visit, fin))
                return BLACK;
            else if (fin[*j])
                return BLACK;
        }
    }
    fin[i] = WHITE;
    return WHITE;
}