#include<stdio.h>

int main()
{
	int n, num, sum=0, i;
	scanf("%d", &n);
	for(i=0; i<n; i++) 	
	{
		scanf("%d", &num);
		sum = sum + num*num; 
	}

	//shortcut method use direct formula sum(n*n) = (n*(n+1)*(2*n+1))/6 
	printf("Sum of squares of the given numbers is %d\n", sum);
	return 0;  
}

