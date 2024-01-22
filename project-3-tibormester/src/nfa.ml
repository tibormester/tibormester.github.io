open List
open Sets

(*********)
(* Types *)
(*********)

type ('q, 's) transition = 'q * 's option * 'q

type ('q, 's) nfa_t = {
  sigma: 's list;
  qs: 'q list;
  q0: 'q;
  fs: 'q list;
  delta: ('q, 's) transition list;
}

(***********)
(* Utility *)
(***********)

(* explode converts a string to a character list *)
let explode (s: string) : char list =
  let rec exp i l =
    if i < 0 then l else exp (i - 1) (s.[i] :: l)
  in
  exp (String.length s - 1) []

(****************)
(* Part 1: NFAs *)
(****************)

let remove_duplicates lst =
  insert_all lst []

let move (nfa: ('q,'s) nfa_t) (qs: 'q list) (s: 's option) : 'q list =
  match s with
  | None -> remove_duplicates (List.fold_left (fun acc trans -> match trans with | (state, Some sym, out) -> acc
    | (state, None, out) -> if elem state qs then out :: acc else acc) [] nfa.delta)
  | Some symbol -> 
    if elem symbol nfa.sigma then 
      remove_duplicates (List.fold_left (fun acc trans -> match trans with | (state, None, out) -> acc
    | (state, Some sym, out) -> if elem state qs && sym = symbol then out :: acc else acc) [] nfa.delta)
    else  []
  

let e_closure (nfa: ('q,'s) nfa_t) (qs: 'q list) : 'q list =
  let rec e_closured qs transitions =
    remove_duplicates (qs @ (List.fold_left (fun acc d -> match d with
      | (qi, Some sym , qo) -> acc
      | (qi, None, qo) -> if elem qi qs then (e_closured [qo] transitions) @ acc else acc) [] transitions)) 
    in e_closured qs nfa.delta

let accept (nfa: ('q,char) nfa_t) (s: string) : bool =
  let states = e_closure nfa [nfa.q0] in 
  let str = explode s in 
  let rec end_states qs stri = match stri with 
    | x :: tail -> end_states (e_closure nfa (move nfa qs (Some x))) tail
    | [] -> qs
  in List.fold_left (fun acc state -> if elem state nfa.fs then true else acc) false (end_states states str)



(*******************************)
(* Part 2: Subset Construction *)
(*******************************)

let new_states (nfa: ('q,'s) nfa_t) (qs: 'q list) : 'q list list =
  let get_new_states s states = 
    e_closure nfa ( move nfa states (Some s))
  in remove_duplicates (List.map (fun sym -> get_new_states sym qs) nfa.sigma)

let new_trans (nfa: ('q,'s) nfa_t) (qs: 'q list) : ('q list, 's) transition list =
  let newStates = new_states nfa qs in
  let get_new_trans s states = 
    (states, Some s, e_closure nfa ( move nfa states (Some s)))
  in List.filter (fun (_, _, q') -> elem q' newStates) (List.map (fun sym -> get_new_trans sym qs) nfa.sigma)

let new_finals (nfa: ('q,'s) nfa_t) (qs: 'q list) : 'q list list =
  if List.fold_left (fun acc state -> if elem state qs then true else acc) false nfa.fs then [qs] else []

let rec nfa_to_dfa_step (nfa: ('q,'s) nfa_t) (dfa: ('q list, 's) nfa_t)
    (work: 'q list list) : ('q list, 's) nfa_t =
    match work with 
    | q :: tail -> let state = e_closure nfa q in 
      let dfa = {dfa with 
        qs =  state :: dfa.qs;
        fs = (union (new_finals nfa state)  dfa.fs);
        delta = (union (new_trans nfa state) dfa.delta);}
      in nfa_to_dfa_step nfa dfa (union tail (diff (new_states nfa state) dfa.qs))
    | [] -> dfa
    


let nfa_to_dfa (nfa: ('q,'s) nfa_t) : ('q list, 's) nfa_t =
  let startState = e_closure nfa [nfa.q0] in
  let dfa = {sigma = nfa.sigma; qs = [startState]; q0 = startState; fs = []; delta = [] }
  in nfa_to_dfa_step nfa dfa [startState]