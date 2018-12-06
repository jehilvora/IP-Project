#include<stdio.h>
#include<string.h>
#include<math.h>
int	main()	
{		
	int num=0, n=0, i,t;	
	char binary[64];	
	scanf("%d",&t);	
	while(t--)
	{
		scanf("%s", binary);	
		n = strlen(binary);	
		num=0;
		for(i=1;i<=n;i++)	
		{
			if(binary[i-1]=='1')
			{	
				num += 1<<(n-i);	
			}	
		}
		printf("%d\n", num);	
	}
	return 0;	
}		

