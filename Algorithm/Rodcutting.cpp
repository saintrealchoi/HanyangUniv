//2018063218_Choisungjin_12838
#include <stdio.h>
#pragma warning(disable:4996)

int len;
int prof;
int p[100];
int r[100];
int s[100];
int sort[100];


int main()
{
	p[0] = 0;
	r[0] = 0;
	s[0] = 0;

	int max = 0;
	int test = 0;
	scanf("%d", &len);
	for (int i = 1; i < len + 1; i++) {
		scanf("%d", &prof);
		p[i] = prof;
	}
	for (int i = 1; i < len + 1; i++) { // i = 2
		max = 0;
		for (int j = 1; j < i + 1; j++) {  // j = 1
			test = p[j] + r[i - j];
			if (max < test) {
				max = test;
				r[i] = max;
				s[i] = j;
			}
		}
	}
	printf("%d\n", max);
	prof = 0;

	while (len > 0)
	{
		sort[prof] = s[len];
		printf("%d ", sort[prof]);
		prof += 1;
		len = len - s[len];
	}
}