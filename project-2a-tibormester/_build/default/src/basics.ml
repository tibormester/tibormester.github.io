open Funs

(***********************************)
(* Part 1: Non-Recursive Functions *)
(***********************************)

let rev_tup (a, b, c) = (c, b, a);;

let is_even x = x mod 2 = 0;;

let area (a, b) (x, y) = abs( x - a) * abs( y - b);;

(*******************************)
(* Part 2: Recursive Functions *)
(*******************************)

let rec fibonacci n = 
  if n < 2 then n
  else fibonacci (n - 1) + fibonacci (n - 2);;

let rec pow x p = 
  if p = 0 then 1
  else if x = 0 then 0
  else x * pow x (p - 1);;

let rec is_prime_h x i =
  if i = 1 then true
  else 
    if x mod i = 0 then false
    else is_prime_h x (i - 1);;

let is_prime x = 
  if x <= 1 then false
  else is_prime_h x (x - 1);;

let maxFuncChain init funcs =
  let rec maxFuncChainR init funcs = 
    match funcs with
    | [] -> [init]
    | f :: rest ->
      let option1 = maxFuncChainR init rest in
      let option2 = maxFuncChainR (f init) rest in
        option1 @ option2
    in 
  let rec maximum max lst =
    match lst with
    | [] -> max
    | x :: rest ->
      if x > max then maximum x rest
      else maximum max rest
    in
  maximum init (maxFuncChainR init funcs);;

(*****************)
(* Part 3: Lists *)
(*****************)

let rec reverse lst = 
  match lst with
  | [] -> []
  | x :: rest -> reverse rest @ [x];;

let rec tail lst =
    match lst with
    | [] -> []
    | [x] -> x
    | _::rest -> tail rest

let rec merge lst1 lst2 = 
  match lst1, lst2 with
  | [], l -> l
  | l, [] -> l
  | x :: rest1, y :: rest2 ->
    if x < y then x :: merge rest1 lst2
    else y :: merge lst1 rest2;;

let is_palindrome lst =
  lst = reverse lst;;      

let jumping_tuples lst1 lst2 = 
  let rec helper lst1 lst2 acc i =
    match lst1, lst2 with
    | [],_ | _,[] -> reverse acc
    | (a,_)::rest1, (_,b)::rest2 -> 
      if i mod 2 = 0 then
        helper rest1 rest2 (b::acc) (i + 1)
      else
        helper rest1 rest2 (a::acc) (i + 1)
  in
  helper lst1 lst2 [] 0;;

let rec flatten lst =
  match lst with
  | [] -> []
  | head :: rest ->
    match head with
    | [] -> flatten rest
    | x :: remaining -> x :: flatten (remaining :: rest);;

let rec square_primes lst =
  match lst with
  | [] -> []
  | x :: rest ->
    if is_prime x then
      (x, x * x) :: square_primes rest
    else
      square_primes rest;;

let rec partition p lst = 
  match lst with
  | [] -> ([],[])
  | x::rest ->
    let (trues, falses) = partition p rest in
    if p x then 
      (x::trues, falses)
    else
      (trues, x::falses);;

(*****************)
(* Part 4: HOF *)
(*****************)

let is_present lst x = 
  let present v =
    if v = x then
      1
    else 
      0
  in
  map present lst;;

let count_occ lst target = 
  let present count v =
    if v = target then
      count + 1
    else
      count
  in
  fold present 0 lst;; 

let uniq lst = 
  let f acc x =
    let present a v = 
      if v = x then 
        a + 1
      else 
        a
    in
    if ((fold present 0 acc) = 1 ) then acc
    else x :: acc
  in
  fold f [] lst;;
