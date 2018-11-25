#include<stdio.h>
#include<string.h>
#include<math.h>
int	main()	
{		
	int num=0, n=0, i;	
	char binary[64];	
	//printf("Enter the binary number\n");	
	scanf("%s", binary);	
	n = strlen(binary);	
	for(i=1;i<=n;i++)	
	{
		if(binary[i-1]=='1')
		{	
			num += 1<<(n-i);	
		}	
	}
	printf("The binary equivalent is %d\n", num);	
	return 0;	
}		

