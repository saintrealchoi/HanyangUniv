//2018063218_ÃÖ¼ºÁø_12838

#include <stdio.h>
#include <stdlib.h>
#include <list>
#pragma warning(disable:4996)
using namespace std;

int N, M;
int ans = 0;

list<int>* ver;

void makeGraph(int n);
void makeEdge(int from, int to);
void dfs(int v, bool visit[]);
void findComp();

int main()
{
    scanf("%d %d", &N, &M);
    makeGraph(N);

    for (int i = 0; i < M; ++i) {
        int from, to;
        scanf("%d %d", &from, &to);
        from--;
        to--;
        makeEdge(from, to);
    }

    findComp();
    printf("%d", ans);
}


void makeGraph(int n) {
    ver = new list<int>[N];
}

void makeEdge(int from, int to) {
    ver[from].push_back(to);
    ver[to].push_back(from);
}

void dfs(int v, bool visit[]) {

    visit[v] = true;
    list<int>::iterator i;
    for (i = ver[v].begin(); i != ver[v].end(); ++i)
        if (!visit[*i])
            dfs(*i, visit);
}

void findComp() {
    bool* visit = new bool[N];
    for (int i = 0; i < N; ++i)
        visit[i] = false;

    for (int i = 0; i < N; ++i) {
        if (visit[i] == false) {
            dfs(i, visit);
            ans++;
        }
    }
    delete[] visit;
}
