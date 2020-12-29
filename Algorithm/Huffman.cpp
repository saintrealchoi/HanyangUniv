//2018063218_ÃÖ¼ºÁø_12838
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#pragma warning(disable:4996)

int size;
int ans;
int n;

typedef struct node {
	int freq;
	node* left_child;
	node* right_child;
} node;

void swap(node*& a, node*& b) {
	node* tmp = a;
	a = b;
	b = tmp;
}

node* min_heap[30010];

node* make_node(int a) {
	node* n = (node*)malloc(sizeof(node));
	n->freq = a;
	n->left_child = NULL;
	n->right_child = NULL;
	return n;
}

int fixed_len(int total, int num) {
	if (num == 1) return total;

	num = num - 1;
	int cnt = 0;
	while (num > 0) {
		num /= 2;
		cnt++;
	}
	return cnt * total;
}


void heapify(int i) {
	int left_child = 2 * i;
	int right_child = 2 * i + 1;

	if (left_child > size) {
		return;
	}

	if (right_child > size) {
		if (min_heap[left_child]->freq < min_heap[i]->freq) {
			swap(min_heap[left_child], min_heap[i]);
			heapify(left_child);
		}
	}
	else {
		int l = min_heap[left_child]->freq;
		int r = min_heap[right_child]->freq;
		int f = min_heap[i]->freq;

		if (l < f && l <= r) {
			swap(min_heap[left_child], min_heap[i]);
			heapify(left_child);
		}
		else if (r < f && r <= l) {
			swap(min_heap[right_child], min_heap[i]);
			heapify(right_child);
		}
	}
}

void insert(node* node) {
	min_heap[++size] = node;
	if (size == 1) return;

	int tmp = size;
	while (tmp > 1) {
		heapify(tmp /= 2);
	}
}

void build() {
	size = n;
	for (int i = size / 2; i >= 1; i--)
		heapify(i);
}

node* extract_min() {
	if (size == 1) {
		size = 0;
		return min_heap[1];
	}

	swap(min_heap[1], min_heap[size--]);
	heapify(1);
	return min_heap[size + 1];
}

bool isleaf(node* n) {
	return (n->left_child == NULL && n->right_child == NULL ? true : false);
}


void traversal(node* n, int cnt) {
	if (isleaf(n)) {
		ans += n->freq * cnt;
		return;
	}
	traversal(n->left_child, cnt + 1);
	traversal(n->right_child, cnt + 1);
}


int main() {
	int total;
	scanf("%d", &n);
	for (int i = 1; i <= n; i++) {
		char c[5];
		scanf("%s", c);

		int a;
		scanf("%d", &a);

		node* newN = make_node(a);

		min_heap[i] = newN;
	}
	scanf("%d", &total);

	printf("%d\n", fixed_len(total, n));
	build();

	node* root;
	while (true) {
		node* L = extract_min();

		if (size == 0) {
			root = L;
			break;
		}

		node* R = extract_min();
		node* Z = make_node(L->freq + R->freq);
		Z->left_child = L;
		Z->right_child = R;
		insert(Z);

	}

	traversal(root, 0);
	printf("%d\n", ans);

	return 0;
}