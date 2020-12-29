//2018063218_Choisungjin_12838
#include <stdio.h>

int min(int a, int b)
{
    if (a < b)
        return a;
    return b;
}

int arr[101];
int n;
int save[101][101];

int func(int start, int end)
{
    int pre_sum = 0;
    int ret = 1000000000;
    if (save[start][end] != -1)
        return save[start][end];
    if (start == end)
    {
        save[start][end] = 0;
        return 0;
    }
    pre_sum = arr[start - 1] * arr[end];
    for (int i = start; i < end; i++)
    {
        ret = min(ret, func(start, i) + func(i + 1, end) + pre_sum * arr[i]);
    }
    save[start][end] = ret;
    return ret;
}
void back_tracking(int start, int end)
{
    int pre_sum = 0;
    if (start == end)
    {
        printf("%d ", start);
        return;
    }
    printf("( ");
    pre_sum = arr[start - 1] * arr[end];
    for (int i = start; i < end; i++)
    {
        if (func(start, i) + func(i + 1, end) + pre_sum * arr[i] == save[start][end])
        {
            back_tracking(start, i);
            back_tracking(i + 1, end);
            break;
        }
    }
    printf(") ");

}
int main()
{
    scanf("%d", &n);
    for (int i = 0; i < n + 1; i++)
        scanf("%d", &arr[i]);
    for (int i = 0; i < n + 1; i++)
        for (int j = 0; j < n + 1; j++)
            save[i][j] = -1;
    printf("%d\n", func(1, n));
    back_tracking(1, n);
    printf("\n");
}