#include<stdio.h>
int main()
{
	int n, a[100], i, max, small,t;
	scanf("%d", &t);
	while(t--)
	{
		scanf("%d", &n);
		for(i=0; i<n; i++)
			scanf("%d", &a[i]);
		max=a[0];
		for(i=0; i<n; i++)
			if(a[i]>max)
				max=a[i];
		small=a[0];
		for(i=0; i<n; i++)
			if(a[i]<small)
				small=a[i];
		printf("%d %d\n", small,max);
	}
	return 0;
}

