package main

import "fmt"

type Node struct {
	val  int
	next *Node
}

func insert(head *Node, val int) {
	if head.next == nil {
		head.next = &Node{val: val}
	} else {
		insert(head.next, val)
	}
}

type visitor func(int)

func print_visitor(val int) {
	fmt.Println("Val is %v", val)
}

func visit(node *Node, v visitor) {
	if node != nil {
		v(node.val)
		visit(node.next, v)
	}
}

func main() {
	fmt.Println("Hello, 世界")
	var head *Node = &Node{val: 1}
	insert(head, 5)
	insert(head, 7)
	insert(head, 5)
	insert(head, 12)
	insert(head, 7)
	insert(head, 7)

	visit(head, print_visitor)
}
