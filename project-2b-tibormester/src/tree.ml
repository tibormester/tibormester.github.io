type 'a tree =
  | Node of 'a tree * 'a * 'a tree
  | Leaf

let rec tree_fold f init tree = 
  match tree with
  | Node (l, x, r) -> f (tree_fold f init l) x (tree_fold f init r)
  | Leaf -> init

let map tree f  = 
  let folder accl x accr =
    Node (accl, f x, accr)
  in tree_fold folder Leaf tree 

let mirror tree = 
  let mirring accl x accr = 
    Node (accr, x, accl)
  in tree_fold mirring Leaf tree

let in_order tree = 
  let f left_subtree value right_subtree = 
    left_subtree @ [value] @right_subtree
  in tree_fold f [] tree

let pre_order tree =  
  let ordering accl value accr = 
    [value] @ accl @ accr
  in tree_fold ordering [] tree

let compose tree = 
  let f left_sub func right_sub =
    fun x -> right_sub (func (left_sub x ))
  in tree_fold f (fun x -> x) tree

let depth tree = 
  let depth left uselessinfo right =
    (max left right) + 1
  in tree_fold depth 0 tree 

(* Assume complete tree *)
let trim tree n = 
  let d = (depth tree) - n in
  let snipper left currentNode right = 
    if snd left >= d then 
      (Node (fst left, currentNode, fst right), (snd left) + 1)
    else 
      (Leaf, (snd left) + 1) 
    in
  fst (tree_fold snipper (Leaf, 0) tree ) 
      
let rec tree_init f v =
  match f v with
  | None -> Leaf
  | Some (v1, v2, v3) -> Node (tree_init f v1, v2, tree_init f v3)

let rec split lst v =
  match lst with
  | [] -> ([], [])
  | hd :: tl ->
    if hd = v then 
      ([], tl)
    else 
      let (l, r) = split tl v in (hd :: l, r)

let rec from_pre_in pre in_ord =
  match pre with
  | [] -> Leaf
  | hd :: tl ->
    let (l, r) = split in_ord hd in
    let lp = List.filter (fun x -> List.mem x l) tl in
    let rp = List.filter (fun x -> List.mem x r) tl in
    let lt = from_pre_in lp l in
    let rt = from_pre_in rp r in
    Node (lt, hd, rt)
