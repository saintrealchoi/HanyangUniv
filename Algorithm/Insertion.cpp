// 2018063218_ÃÖ¼ºÁø_12838
#include <stdio.h>
#include <stdlib.h>
#define SWAP(x,y,temp) ((temp) = (x), (x) = (y), (y)=(temp))

void insertionSort(int* array, int number);

int main()
{
	int num, temp;
	scanf("%d", &num);
	int* array = (int*)malloc(sizeof(int) * num);
	for (int i = 0; i < num; i++)
	{
		scanf("%d", &array[i]);
	}
	insertionSort(array, num);
	free(array);
	return 0;
}

void insertionSort(int* array, int number) {
	int i, j, key, temp;
	for (i = 1; i < number; i++)
	{
		key = array[i];
		for (j = i - 1; j >= 0 && array[j] < key; j--) {
			SWAP(array[j + 1], array[j], temp);
		}
		SWAP(array[j + 1], key, temp);
	}
	for (int i = 0; i < number; i++)
	{
		printf("%d\n", array[i]);
	}
}