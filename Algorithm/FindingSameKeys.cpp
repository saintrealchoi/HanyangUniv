//2018063218_ÃÖ¼ºÁø_12838
#include <stdio.h>
#pragma warning(disable : 4996)

int array[100001];
int main()
{
	int n, m;
	int num;
	int max = 0;
	int count = 0;
	scanf("%d %d", &n, &m);
	for (int i = 0; i < n; i++) {
		scanf("%d", &num);
		array[num]++;
		if (max < num)
			max = num;
	}
	for (int i = 0; i < m; i++) {
		scanf("%d", &num);
		array[num]++;
	}
	for (int i = 1; i < max + 1; i++) {
		if (array[i] > 1)
			count++;
	}
	printf("%d", count);

}