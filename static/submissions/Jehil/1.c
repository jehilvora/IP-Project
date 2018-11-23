#include<stdio.h>

tower(int n, char source, char dest, char temp)
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
int n;
scanf("%d",&n);
tower(n,'S','D','T');
return 0;
}
