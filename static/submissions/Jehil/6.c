

#include<stdio.h>



void tower(int n, char source, char dest, char temp)

{

	if(n>0)

	{

		tower(n-1,source,temp,dest);

		printf("%d %c %c\n",n,source,dest);

		tower(n-1,temp,dest,source);

	}

	return;

}

    

int main()

{

    int t;

    scanf("%d",&t);

    while(t--)

    {

        int n;

        scanf("%d",&n);

        toh(n,'S','D','T');

        printf("\n");
    }

    return 0;

}








