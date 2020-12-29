// 2018063218_ÃÖ¼ºÁø_12838
#include <stdio.h>
#include <stdlib.h>
#define SWAP(x,y,temp) ((temp) = (x), (x) = (y), (y)=(temp))

void merge(int* array, int left, int mid, int right);
void mergeSort(int* array, int left, int right);

int main()
{
	int num;
	scanf("%d", &num);
	int* array = (int*)malloc(sizeof(int) * num);
	for (int i = 0; i < num; i++)
	{
		scanf("%d", &array[i]);
	}
	mergeSort(array,0,num-1);
	for (int i = 0; i < num; i++)
	{
		printf("%d\n", array[i]);
	}
	free(array);
	return 0;
}

void merge(int *array, int left, int mid, int right)
{
	int* temp = (int*)malloc(sizeof(int) * (right - left + 1));
	int i = left;
	int j = mid + 1;
	int k = 0;

	while (i <= mid && j <= right)
	{
		if (array[i] >= array[j])
			temp[k++] = array[i++];
		else
			temp[k++] = array[j++];
	}
	while (i <= mid)
		temp[k++] = array[i++];
	while (j <= right)
		temp[k++] = array[j++];

	i = left;
	k = 0;

	while (i<=right)
	{
		array[i++] = temp[k++];
	}
	free(temp);
}
void mergeSort(int* array, int left, int right)
{
	int mid;
	if (left < right)
	{
		mid = (left + right) / 2;
		mergeSort(array, left, mid);
		mergeSort(array, mid + 1, right);
		merge(array, left, mid, right);
	}
}
