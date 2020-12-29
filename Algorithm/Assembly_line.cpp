//2018063218_Choisungjin_12838
#include <stdio.h>
#pragma warning(disable:4996)

int c;
int d;
int num;
int e[2];
int x[2];
int arr1[101];
int arr2[101];
int time1[101];
int time2[101];
int line[2][101];
int line2[2][101];
int line3[101];
int result;

int main()
{
	scanf("%d", &num);
	scanf("%d %d", &e[0], &e[1]);
	scanf("%d %d", &x[0], &x[1]);
	for (int i = 0; i < num; i++) {
		scanf("%d", &arr1[i]);
	}
	for (int i = 0; i < num; i++) {
		scanf("%d", &arr2[i]);
	}
	for (int i = 0; i < num - 1; i++) {
		scanf("%d", &time1[i]);
	}
	for (int i = 0; i < num - 1; i++) {
		scanf("%d", &time2[i]);
	}

	line[0][0] = arr1[0] + e[0];
	line[1][0] = arr2[0] + e[1];


	if (num == 1) {
		if (line[0][0] + x[0] < line[1][0] + x[1]) {
			printf("%d\n", line[0][0] + x[0]);
			printf("1 1\n");
		}
		else {
			printf("%d\n", line[1][0] + x[1]);
			printf("2 1\n");
		}
	}
	else {
		for (int i = 1; i < num; i++)
		{
			if ((line[0][i - 1] + arr1[i] < line[1][i - 1] + time2[i - 1] + arr1[i])||
				(line[0][i - 1] + arr1[i] == line[1][i - 1] + time2[i - 1] + arr1[i])) {
				line[0][i] = line[0][i - 1] + arr1[i];
				line2[0][i] = 1;
			}
			else {
				line[0][i] = line[1][i - 1] + time2[i - 1] + arr1[i];
				line2[0][i] = 2;
			}
			if (line[1][i - 1] + arr2[i] < line[0][i - 1] + time1[i - 1] + arr2[i]) {
				line[1][i] = line[1][i - 1] + arr2[i];
				line2[1][i] = 2;
			}
			else {
				line[1][i] = line[0][i - 1] + time1[i - 1] + arr2[i];
				line2[1][i] = 1;
			}

		}
		d = num - 1;
		if ((line[0][d] + x[0] < line[1][d] + x[1]) || (line[0][d] + x[0] == line[1][d] + x[1])) {
			result = line[0][d] + x[0];
			line3[0] = 1;
		}
		else {
			result = line[1][d] + x[1];
			line3[0] = 2;
		}


		printf("%d\n", result);

		c = line3[0];
		for (int j = d; j > 0; j--)
		{
			c = line2[c - 1][j];
			line3[j] = c;
		}
		for (int i = 1; i < num; i++)
		{
			printf("%d %d\n", line3[i], i);
		}
		printf("%d %d\n", line3[0], num);
	}
}
