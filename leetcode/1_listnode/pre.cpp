#include <stdio.h>

struct ListNode
{
    int value;    // data
    ListNode *next; // 
};

int main()
{

    ListNode a;
    ListNode b;
    ListNode c;
    ListNode d;
    ListNode e;

    a.value = 10;
    b.value = 20;
    c.value = 30;
    d.value = 40;
    e.value = 50;

    a.next = &b;
    b.next = &c;
    c.next = &d;
    d.next = &e;
    e.next = NULL;
    
    ListNode *head = &a;

    while(head)
    {
        printf("%d\n", head->value);
        head = head->next;
    }
    
    return 0;
}
