package main

import "fmt"

type Node struct {
	Value int
	Left  *Node
	Right *Node
}

func insert(curr *Node, val int) *Node {
	if curr == nil {
		return &Node{Value: val}
	}
	if val == curr.Value {
		return curr
	} else if val > curr.Value {
		curr.Right = insert(curr.Right, val)
	} else {
		curr.Left = insert(curr.Left, val)
	}

	return curr
}

func DepthFirst(curr *Node, label string) {
	if curr == nil {
		return
	}
	fmt.Println("Iterate %d -- %s", curr.Value, label)
	DepthFirst(curr.Left, "left")
	DepthFirst(curr.Right, "right")
}

func main() {
	var head *Node = insert(nil, 5)
	insert(head, 3)
	insert(head, 7)
	insert(head, 11)
	insert(head, 1)
	insert(head, 4)
	insert(head, 20)
	DepthFirst(head, "head")
}
