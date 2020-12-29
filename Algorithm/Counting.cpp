#include <stdio.h>


int array[100001];

int from[100001];

int to[100001];

int main()
{
    int n, m, k;
    int temp;
    scanf("%d %d %d", &n, &m, &k);

    for (int i = 0; i < k; i++)
        scanf("%d %d", &from[i], &to[i]);
    array[100001] = { 0 };
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &temp);
        array[temp] += 1;
    }
    array[0] = 0;
    for (int i = 1; i < m+1; i++)
        array[i] = array[i] + array[i - 1];

    for (int i = 0; i < k; i++)
        printf("%d\n", array[to[i]] - array[from[i] - 1]);


}