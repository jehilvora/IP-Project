#include <stdio.h>

const long long INF = 1e18 + 42;

int main() {
	int T;
	scanf("%d", &T);
	while (T--) {
		int n, q;
		scanf("%d %d", &n, &q);
		
		long long p = 1, x;
		while (n--) {
			scanf("%lld", &x);
			if (x > INF / p) p = INF;
			else p *= x;
		}
		
		while (q--) {
			scanf("%lld", &x);
			printf("%lld ", x / p);
		}
		printf("\n");
	}
	return 0;
}