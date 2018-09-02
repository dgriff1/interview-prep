package main

import "fmt"
import "os"
import "reflect"

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

func inorder(curr *Node, agg []int) []int {
	if curr == nil {
		return agg
	}
	agg = inorder(curr.Left, agg)
	agg = append(agg, curr.Value)
	agg = inorder(curr.Right, agg)
	return agg
}

func preorder(curr *Node, agg []int) []int {
	if curr == nil {
		return agg
	}
	agg = append(agg, curr.Value)
	agg = preorder(curr.Left, agg)
	agg = preorder(curr.Right, agg)
	return agg
}

func postorder(curr *Node, agg []int) []int {
	if curr == nil {
		return agg
	}
	agg = postorder(curr.Left, agg)
	agg = postorder(curr.Right, agg)
	agg = append(agg, curr.Value)
	return agg
}

func main() {
	var head *Node = insert(nil, 5)
	insert(head, 3)
	insert(head, 7)
	insert(head, 11)
	insert(head, 1)
	insert(head, 4)
	insert(head, 20)
	var resp []int = inorder(head, []int{})
	var inorder_arr = []int{1, 3, 4, 5, 7, 11, 20}
	if !reflect.DeepEqual(resp, inorder_arr) {
		fmt.Println("Inorder %v ", resp)
		os.Exit(-1)
	}
	resp = preorder(head, []int{})
	var preorder_arr = []int{5, 3, 1, 4, 7, 11, 20}
	if !reflect.DeepEqual(resp, preorder_arr) {
		fmt.Println("Preorder %v ", resp)
		os.Exit(-1)
	}
	resp = postorder(head, []int{})
	var postorder_arr = []int{1, 4, 3, 20, 11, 7, 5}
	if !reflect.DeepEqual(resp, postorder_arr) {
		fmt.Println("Postorder %v ", resp)
		os.Exit(-1)
	}

	fmt.Println("everything worked")
}
