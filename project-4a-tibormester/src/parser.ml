open MicroCamlTypes
open Utils
open TokenTypes

(* Provided functions - DO NOT MODIFY *)

(* Matches the next token in the list, throwing an error if it doesn't match the given token *)
let match_token (toks: token list) (tok: token) =
  match toks with
  | [] -> raise (InvalidInputException(string_of_token tok))
  | h::t when h = tok -> t
  | h::_ -> raise (InvalidInputException(
      Printf.sprintf "Expected %s from input %s, got %s"
        (string_of_token tok)
        (string_of_list string_of_token toks)
        (string_of_token h)))

(* Matches a sequence of tokens given as the second list in the order in which they appear, throwing an error if they don't match *)
let match_many (toks: token list) (to_match: token list) =
  List.fold_left match_token toks to_match

(* Return the next token in the token list as an option *)
let lookahead (toks: token list) = 
  match toks with
  | [] -> None
  | h::t -> Some h

(* Return the token at the nth index in the token list as an option*)
let rec lookahead_many (toks: token list) (n: int) = 
  match toks, n with
  | h::_, 0 -> Some h
  | _::t, n when n > 0 -> lookahead_many t (n-1)
  | _ -> None

(* Part 2: Parsing expressions *)

let rec parse_expr toks = 
 match toks with
  | [] -> raise(InvalidInputException("UnexpectedEndOfTokens Expected an Expression, but got no tokens"))
  (*Start of Let, first assumes recursive next doesn't
     let (rec|e) id = expr in expr*)
  | Tok_Let :: Tok_Rec :: Tok_ID id :: Tok_Equal :: rest -> (
    let (rest2, expr1) = parse_expr rest in
    match rest2 with
      |Tok_In :: rest3 -> let (rest4, expr2) = parse_expr rest3 in
        (rest4, Let(id,true, expr1, expr2 ))
      | _ -> raise(InvalidInputException("'Tok_In' expected")))
  | Tok_Let :: Tok_ID id :: Tok_Equal :: rest -> (
    let (rest2, expr1) = parse_expr rest in
    match rest2 with
      |Tok_In :: rest3 -> let (rest4, expr2) = parse_expr rest3 in
        (rest4, Let(id,false, expr1, expr2 ))
      | _ -> raise(InvalidInputException("'Tok_In' expected")))
  (*Start of Function, 
     fun id -> expr *)
  | Tok_Fun :: Tok_ID id :: Tok_Arrow :: rest -> (
    let (rest2, expr) = parse_expr rest in
    (rest2, Fun (id, expr)))
  (*Start of If
     If expr1 then expr2 else expr3*)
  | Tok_If :: rest -> (let (rest1, expr1) = parse_expr rest in
    match rest1 with
    | Tok_Then :: rest2 -> (let (rest3, expr2) = parse_expr rest2 in
      match rest3 with
      | Tok_Else :: rest4 -> (let (rest5, expr3) = parse_expr rest4 in
        (rest5, If (expr1,expr2,expr3)))
      | _ -> (raise(InvalidInputException("'Tok_Else' expected"))))
    | _ -> (raise(InvalidInputException("'Tok_Then' expected"))))
  | _ -> parse_or toks

and parse_primary toks =
  match toks with
  | Tok_Int x :: rest -> (rest, Value(Int(x)))
  | Tok_Bool x :: rest -> (rest, Value(Bool(x)))
  | Tok_String x :: rest -> (rest, Value(String(x)))
  | Tok_ID x :: rest -> (rest, ID(x))
  | Tok_LParen :: rest -> (
    let (rest1, expr) = parse_expr rest in
    match rest1 with
    | Tok_RParen :: rest2 -> 
      (rest2, expr)
    | _ -> raise(InvalidInputException("Unmatched Opening Parenthese, Missing ')'")))
  | _ -> raise(Division_by_zero) 
  
and parse_funcallexpr toks =
    try (let (rem, primary) = parse_primary toks in
      try let (remaing, primary2) = parse_primary rem in (remaing, FunctionCall(primary, primary2)) with
      | Division_by_zero ->  (rem, primary)) with 
    | Division_by_zero -> raise(InvalidInputException("function call expression first argument invalid"))


and parse_unary toks =
        match toks with
        | Tok_Not :: rest -> let (rem, expr) = parse_unary rest in
          (rem, Not(expr))
        | _ -> parse_funcallexpr toks

and parse_concat toks =
        let (remaining, multiexpr) = parse_unary toks in
        match remaining with
        | Tok_Concat :: rest -> let (remaining1, addexpr) = parse_concat rest in
          (remaining1, Binop(Concat, multiexpr, addexpr))
        |_ -> (remaining, multiexpr)
and parse_multi toks =
  let (remaining, multiexpr) = parse_concat toks in
        match remaining with
        | Tok_Mult :: rest -> let (remaining1, addexpr) = parse_multi rest in
          (remaining1, Binop(Mult, multiexpr, addexpr))
        |Tok_Div :: rest -> let (remaining1, addexpr) = parse_multi rest in
          (remaining1, Binop(Div, multiexpr, addexpr))
        |_ -> (remaining, multiexpr)

and parse_add toks =
        let (remaining, multiexpr) = parse_multi toks in
        match remaining with
        | Tok_Add :: rest -> let (remaining1, addexpr) = parse_add rest in
          (remaining1, Binop(Add, multiexpr, addexpr))
        |Tok_Sub :: rest -> let (remaining1, addexpr) = parse_add rest in
          (remaining1, Binop(Sub, multiexpr, addexpr))
        |_ -> (remaining, multiexpr)
and parse_relation toks =
    let (rem, addexpr) = parse_add toks in
    match rem with
    |Tok_Less :: rest -> let (remaining, relationexpr) = parse_relation rest in
      (remaining, Binop(Less, addexpr, relationexpr))
    |Tok_LessEqual :: rest -> let (remaining, relationexpr) = parse_relation rest in
      (remaining, Binop(LessEqual, addexpr, relationexpr))
    |Tok_Greater :: rest -> let (remaining, relationexpr) = parse_relation rest in
      (remaining, Binop(Greater, addexpr, relationexpr))
    |Tok_GreaterEqual :: rest -> let (remaining, relationexpr) = parse_relation rest in
      (remaining, Binop(GreaterEqual, addexpr, relationexpr))
    |_ -> (rem, addexpr)

and parse_equal toks =
  let (remaining, relationexpr) = parse_relation toks in
  match remaining with
  | Tok_Equal :: rest -> let (remaining1, equalexpr) = parse_equal rest in
    (remaining1, Binop(Equal, relationexpr, equalexpr))
  |Tok_NotEqual :: rest -> let (remaining1, equalexpr) = parse_equal rest in
    (remaining1, Binop(NotEqual, relationexpr, equalexpr))
  |_ -> (remaining, relationexpr)

and parse_and toks =
  let (remaining, equalexpr) = parse_equal toks in 
  match remaining with
  |Tok_And :: rest -> let (remaining1, andexpr) = parse_and rest in
    (remaining1, Binop(And, equalexpr, andexpr))
  |_ -> (remaining, equalexpr)

and parse_or toks =
  let (remaining, andexpr) = parse_and toks in
  match remaining with
  | Tok_Or :: rest -> let (remaining1, orexpr) = parse_or rest in
    (remaining1, Binop(Or, andexpr, orexpr))
  | _ -> (remaining, andexpr)




(* Part 3: Parsing mutop *)

let rec parse_mutop toks = 
  match toks with
  | Tok_Def :: Tok_ID id :: Tok_Equal :: rest -> (
    let (left, expr) = parse_expr rest in
    match left with
    | Tok_DoubleSemi :: rest -> (rest, Def(id, expr))
    | _ -> raise(InvalidInputException("Missing Semicolon after Expression")))
  | Tok_DoubleSemi :: rest -> (rest, NoOp) 
  | _ -> parse_expr_mutop toks
  
  
and parse_expr_mutop toks =
  let (left, expr) = parse_expr toks in 
  match left with
  | Tok_DoubleSemi :: rest -> (rest, Expr(expr)) 
  | _ -> raise(InvalidInputException("Missing Semicolon after Expression"))