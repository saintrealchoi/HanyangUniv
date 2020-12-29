//2018063218_ÃÖ¼ºÁø_12838
#include <stdio.h>
int array[100002];
int size = 1;


void push(int num)
{
    int pos = size;
    array[size] = num;

    while (1)
    {
        if (pos == 1)
            break;
        if (array[pos] < array[pos / 2])
        {
            int temp = array[pos];
            array[pos] = array[pos / 2];
            array[pos / 2] = temp;
            pos = pos / 2;
        }
        else
            break;
    }
    size++;

}

int pop()
{
    int pos = 1;
    int ret = array[1];

    size--;
    array[1] = array[size];

    while (1)
    {
        if (2 * pos > size - 1)
            break;
        else if (2 * pos == size - 1)
        {
            if (array[2 * pos] < array[pos])
            {
                int temp = array[2 * pos];
                array[2 * pos] = array[pos];
                array[pos] = temp;
            }
            break;
        }
        else
        {
            int pick = 0;
            if (array[2 * pos] < array[2 * pos + 1])
                pick = 2 * pos;
            else
                pick = 2 * pos + 1;

            if (array[pick] < array[pos])
            {
                int temp = array[pick];
                array[pick] = array[pos];
                array[pos] = temp;
                pos = pick;
            }
            else
                break;
        }

    }
    return ret;
}


int main()
{
    int n, k;
    scanf("%d %d", &n, &k);
    int num = 0;
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &num);
        push(num);
    }
    //for (int i = 0; i < k; i++)
    //    printf("%d ", pop());
    printf("\n");
    for (int i = 1; i < size; i++)
        printf("%d ", array[i]);
    printf("\n");
}