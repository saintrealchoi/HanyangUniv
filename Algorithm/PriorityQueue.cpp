//2018063218_ÃÖ¼ºÁø_12838
#include <stdio.h>
#include <stdlib.h>
int array[100001];
int size = 1;


void push(int num)
{
    int pos = size;
    array[size] = num;

    while (1)
    {
        if (pos == 1)
            break;
        if (array[pos] > array[pos / 2])
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
            if (array[2 * pos] > array[pos])
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
            if (array[2 * pos] > array[2 * pos + 1])
                pick = 2 * pos;
            else
                pick = 2 * pos + 1;

            if (array[pick] > array[pos])
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

void change(int index, int num)
{
    int pos = index;
    int direction = 0;
    array[pos] = num;

    if (pos == 1)
        direction = 1; //down
    else if (2 * pos > size - 1)
        direction = 2; //up
    else
    {
        if (array[pos / 2] < array[pos])
            direction = 2;
        else
            direction = 1;
    }

    if (direction == 1)
    {
        while (1)
        {
            if (2 * pos > size - 1)
                break;
            else if (2 * pos == size - 1)
            {
                if (array[2 * pos] > array[pos])
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
                if (array[2 * pos] > array[2 * pos + 1])
                    pick = 2 * pos;
                else
                    pick = 2 * pos + 1;

                if (array[pick] > array[pos])
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

    }
    else if (direction == 2)
    {
        while (1)
        {
            if (pos == 1)
                break;
            if (array[pos] > array[pos / 2])
            {
                int temp = array[pos];
                array[pos] = array[pos / 2];
                array[pos / 2] = temp;
                pos = pos / 2;
            }
            else
                break;
        }
    }



}

int main()
{
    while (1)
    {
        int opt;
        scanf("%d", &opt);
        if (opt == 0)
        {
            printf("\n");
            break;
        }
        else if (opt == 1)
        {
            int num;
            scanf("%d", &num);
            push(num);
        }
        else if (opt == 2)
            printf("%d ", pop());
        else if (opt == 3)
        {
            int index, num;
            scanf("%d %d", &index, &num);
            change(index, num);
        }
    }
    for (int i = 1; i < size; i++)
        printf("%d ", array[i]);
    printf("\n");


}