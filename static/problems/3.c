#include<stdio.h>

void insert_sort(int a[],int);

int main()
{
    int t;
    scanf("%d",&t);
    while(t--)
    {
        int n;
        scanf("%d",&n);
        int a[n];
        for(int i=0;i<n;i++)
        {
            scanf("%d",&a[i]);
        }
        insert_sort(a,n);
        for(int i=0;i<n;i++)
        {
            printf("%d ",a[i]);
        }
        printf("\n");
    }
    return 0;    
}
void insert_sort(int a[],int n)
{
    int i,j,num;
    for(i=0;i<n;i++)
    {
        num=a[i];
        for(j=i-1;j>=0&&num<a[j];j--)
        {
            a[j+1]=a[j];
        }
        a[j+1]=num;
    }
    return;
}