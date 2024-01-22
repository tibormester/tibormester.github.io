open MicroCamlTypes
open Utils

exception TypeError of string
exception DeclareError of string
exception DivByZeroError 

(* Provided functions
  Helpful for creating an environment. You can do this with references 
  (not taught) or without. 
  You do not have to use these and you can modify them if you want. 
  If you do not use references, you will need the following data type:
  
type values = Int of int|Bool of bool|String of string
*)
(* Adds mapping [x:v] to environment [env] *)
let ref_extend env x v = (x, ref v)::env

(* Returns [v] if [x:v] is a mapping in [env]; uses the
   most recent if multiple mappings for [x] are present *)
let rec ref_lookup env x =
  match env with
  | [] -> raise (DeclareError ("Unbound variable " ^ x))
  | (var, value)::t -> if x = var then !value else ref_lookup t x

(* Creates a placeholder mapping for [x] in [env]; needed
   for handling recursive definitions *)
let ref_extend_tmp env x = (x, ref (Int 0))::env

(* Updates the (most recent) mapping in [env] for [x] to [v] *)
let rec ref_update env x v =
  match env with
  | [] -> raise (DeclareError ("Unbound variable " ^ x))
  | (var, value)::t -> if x = var then (value := v) else ref_update t x v
        

(* Part 1: Evaluating expressions *)

(* Evaluates MicroCaml expression [e] in environment [env],
   returning a value, or throwing an exception on error *)
let rec eval_expr env e = 
  match e with
  | Value v -> (v)
  | ID v -> ref_lookup env v 
  | Not exp -> (let v = eval_expr env exp in 
    if v = Bool true then Bool false else if v = Bool false then Bool true else raise(TypeError("expected Boolean")))
  | Binop (op, e1, e2) -> (
    let v1 = eval_expr env e1 in
    let v2 = eval_expr env e2 in
    match (v1, v2 )with
      | (Int x, Int y) -> (
        match op with 
        | Mult -> Int (x * y)
        | Add -> Int (x + y)
        | Sub -> Int (x - y)
        | Div ->( try (Int (x / y)) with 
          |Division_by_zero -> raise(DivByZeroError))
        | Greater -> if x > y then Bool true else Bool false
        | GreaterEqual -> if x >= y then Bool true else Bool false
        | Less -> if x < y then Bool true else Bool false
        | LessEqual -> if x <= y then Bool true else Bool false
        | Equal -> if x = y then Bool true else Bool false
        | NotEqual -> if x = y then Bool false else Bool true
        | _ -> raise(TypeError("Type Error, wrong Operation for ints"))
      )
      | (String a, String b) -> (
        match op with
        | Concat -> String ( a ^ b)
        | Equal -> if a = b then Bool true else Bool false
        | NotEqual -> if a = b then Bool false else Bool true
        | _ -> raise(TypeError("Got strings but not right operation"))
      )
      | (Bool a, Bool b) -> (
        match op with
        | Equal -> if a = b then Bool true else Bool false
        | NotEqual -> if a = b then Bool false else Bool true
        | Or -> Bool (a || b)
        | And -> Bool (a && b)
        | _ -> raise(TypeError("Got Bools but not right operation"))
      )
      | _, _ ->raise(TypeError("Got mismatched types in binop")))
  | If (g, e1, e2) -> (
    let guard = eval_expr env g in
    match guard with
    |Bool y -> (
      if y then eval_expr env e1 else eval_expr env e2
      )
    | _ -> raise(TypeError("Expecting boolean in if statment got a diff val"))
  )
  | Let (name, re, init, body) -> (
    if not re then 
      let v = eval_expr env init in
      eval_expr (ref_extend env name v) body
    else
      let env1 = ref_extend_tmp env name in
      let _ = ref_update env1 name (eval_expr env1 init) in
      eval_expr env1 body 
  )
  | Fun (name, exp) -> Closure(env, name, exp)
  | FunctionCall (e1, e2) -> (
    match (eval_expr env e1) with
    | Closure (a, x, e) ->(
      let v = eval_expr env e2 in
      let new_env = ref_extend a x v in
      eval_expr new_env e 
    )
    | _ -> raise(TypeError("Function call param must be a closure!"))
  )
(* Part 2: Evaluating mutop directive *)

(* Evaluates MicroCaml mutop directive [m] in environment [env],
   returning a possibly updated environment paired with
   a value option; throws an exception on error *)
let eval_mutop env m = 
  match m with
  | Def (name, e) -> (
    let env_new = ref_extend_tmp env name in
    let value = eval_expr env_new e in
    let _ = ref_update env_new name value in
    (env_new, Some value)
  )
  | Expr e -> (
    let value = eval_expr env e in
    (env, Some value)
  )
  | NoOp -> (
    (env, None)
  )
  | _ -> raise(TypeError("Expecting a mutop type but got something else"))
